---
title: "Options Market-Making Simulator: Project Report (English Summary)"
date: "2026-09-16"
tags: ["Market Making", "Options", "Project"]
summary: "A backtesting system from raw Deribit BTC options data to a full market-maker loop: SVI surface, quoting, fills, hedging and PnL attribution."
---

> Last Edit: 11/26/26

*Project Report: From Raw Deribit BTC Options Data to PnL Attribution*

<aside>
💡

**One-line summary.** This is a backtesting system that turns **raw Deribit BTC options/futures market data** into a **complete market-maker decision loop**: record data → fit a volatility surface → quote → match fills → hedge → attribute every dollar of PnL to a specific risk source — replaying history strictly in time order, with no look-ahead. The underlying is currently fixed to BTC; `load_range()` keeps a currency-switch hook for extending to ETH and others later.

</aside>

## 1. The six steps end to end

The six steps below are the system's main pipeline; the core method used in each step is written directly into that step.

1. **Record data:** `record_deribit.py` connects to Deribit's public API and continuously logs order-book snapshots, tickers (mark price and index price included), and trade prints for BTC options/futures, partitioned by date into `parquet` files.
2. **Load & align:** `load_range()` reads BTC data for a given date range, parses instrument names, filters out illiquid contracts by minimum open interest, and merges everything into a single timestamp-sorted event stream.
3. **Initial surface fit (pricing):** implied volatility is backed out from tickers using the **Black-76** futures-options pricing formula; contracts are grouped by expiry and fit with vega-weighted **SVI** (Stochastic Volatility Inspired) parameterization to produce a complete volatility surface — see Section 2.
4. **Assemble the market-making/risk/hedging components:** quoting, position bookkeeping, limits, hedging, and fill matching — see Sections 3–7. Three of these stages each have a dedicated method:
    - **Quoting:** the **Avellaneda-Stoikov** inventory-aware market-making framework — half-spread widens with vega/gamma, and quotes are adjusted by inventory skew;
    - **Fill matching:** either **Poisson** theoretical matching (fill intensity decays exponentially with spread) or **trade-replay** (a fill is only recorded if a real historical trade crosses the quote);
    - **Hedging:** one of interval hedging / fixed-band hedging / **Whalley–Wilmott** optimal-band hedging.
5. **Event-driven backtest:** periodic surface-refit events and hedge-check events are inserted into the event stream and processed strictly in time order with no look-ahead; at every hedge-check point, the hedging rule chosen in Step 4 is executed.
6. **Output & PnL attribution:** the PnL series is produced and decomposed term by term into delta/gamma/theta/vega via a multivariate **Taylor** expansion, with the residual tracked separately (see Section 8); Sharpe ratio, maximum drawdown, and other metrics are then computed and plotted.

## 2. The foundation of pricing: from market data to a volatility surface

### 2.1 The Black-Scholes formula

The most basic option-pricing model is the Black-Scholes formula. For a European call on a spot underlying with strike $K$ and time to expiry $\tau$, the theoretical price is:

$$
C = S\,N(d_1) - Ke^{-r\tau}N(d_2), \qquad d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)\tau}{\sigma\sqrt{\tau}}, \qquad d_2 = d_1 - \sigma\sqrt{\tau} \tag{1}
$$

where $S$ is the current underlying price, $K$ is the strike, $r$ is the risk-free rate, $\tau$ is time to expiry, $\sigma$ is volatility, and $N(\cdot)$ is the standard normal CDF. Every variable in Eq. (1) except $\sigma$ ($S$, $K$, $r$, $\tau$) is directly observable in the market.

### 2.2 Backing out implied volatility

Implied volatility (IV) is computed by running Eq. (1) in reverse: given the option's real market price or mid quote $C_{\text{market}}$, substitute it into the left-hand side of Eq. (1) and solve for the unique $\sigma$ that makes the equation hold:

$$
\sigma_{\text{IV}} = \sigma \ \text{ such that } \ C(\sigma) = C_{\text{market}} \tag{2}
$$

Eq. (2) has no closed-form solution, since $\sigma$ sits inside $N(\cdot)$; it is typically solved numerically (e.g. Newton-Raphson). This is what "backing out implied vol from market data" actually means in practice: rather than computing a price from a model, it reads the market's own price and infers what volatility expectation the market is currently pricing in.

### 2.3 Why IV differs across strikes

One of Black-Scholes' core assumptions is that the underlying price follows geometric Brownian motion with a **constant volatility** $\sigma$ — in theory, the IV backed out should be the same regardless of strike. In real markets this is almost never true, for three main reasons:

- **Tail-risk pricing:** real underlying price distributions have fatter tails than the normal distribution, with a higher probability of extreme moves than the model assumes. Deep out-of-the-money and deep in-the-money options are effectively pricing this tail risk, so the market assigns them a higher IV as a risk premium rather than pricing everything off the at-the-money IV.
- **Supply-and-demand imbalance:** demand differs by strike. In crypto markets, for instance, investors routinely buy out-of-the-money puts as tail hedges; this demand pushes up the price — and hence the backed-out IV — at that strike, independent of the underlying's true volatility expectation and driven purely by order flow pressure.
- **Leverage effect and the price-dependence of volatility:** when the underlying falls, leverage rises (or market panic rises), and realized volatility tends to rise with it. This negative correlation between price and volatility — "price down, vol up" — systematically produces higher backed-out IV at lower strikes (the put side).

Plotting the string of IVs backed out across strikes at a single expiry — strike (or log-moneyness) on the x-axis, IV on the y-axis — typically produces a curve that is low in the middle and higher on both sides, resembling a smile: the **volatility smile**. It is not an artifact of the model; it is the market telling you that Black-Scholes' constant-volatility assumption is wrong, and that the true implied risk expectation genuinely differs across strikes.

The project actually uses **Black-76** to back out IV (see the note following Eq. (1)), a variant of Black-Scholes for options on a futures underlying: $Se^{r\tau}$ in Eq. (1) is replaced directly with the futures price $F$, so interest rates and dividends need not be handled separately (these carry costs are already embedded in the futures price); the formula structure and the logic of "solving for $\sigma$ from a price" are otherwise identical to Black-Scholes. Because BTC options on Deribit are written on perpetuals/futures rather than spot, using Black-76 rather than plain Black-Scholes is what avoids a systematic bias in the backed-out implied volatility.

### 2.4 From curve to surface: SVI fitting

For a single expiry, plotting IV against strike gives a curved line (the volatility smile) rather than a flat one. Stacking these curves across all expiries produces a three-dimensional **volatility surface**: strike on one axis, time to expiry on the other, and implied volatility as the height.

The project fits each expiry's curve with the **SVI** (Stochastic Volatility Inspired) parameterization, which describes total variance as a function of strike using five parameters:

$$
w(k) = a + b\left(\rho(k-m) + \sqrt{(k-m)^2 + \sigma^2}\right) \tag{3}
$$

where $k$ is log-moneyness, $a$ controls the overall level of the curve, $b$ controls how steep the two wings are, $\rho$ controls the direction of left-right skew, $m$ controls the location of the curve's minimum, and $\sigma$ controls how rounded that minimum is. Fitting is **vega-weighted** per contract — liquid, high-vega contracts get more weight, so illiquid, noisy deep-OTM quotes don't drag the whole curve off.

Figure 1 plots the curve produced by a representative parameter set ($a=0.04$, $b=0.4$, $\rho=-0.3$, $m=0$, $\sigma=0.15$, corresponding to a 7-day expiry) substituted into Eq. (3): $\rho<0$ skews the curve to the left, meaning IV on the low-strike (put) side is steeper than on the high-strike side — exactly the leverage-effect-driven left skew discussed in Section 2.3, now expressed in SVI parameters.

*Figure 1: Three SVI curves at different expiries (parameters evolve with time to expiry: larger $a$ reflects more accumulated total variance over a longer horizon, larger $\sigma$ flattens the minimum, and the strength of the left skew $\rho$ eases slightly). Stacking this family of curves along the expiry axis is exactly what the volatility surface is. (Plot of total variance $w(k)$ vs. log-moneyness $k$ for 7-, 30- and 90-day expiries — see the PDF version.)*

The differences among the three curves illustrate how the surface behaves along the expiry axis: the longer the expiry, the higher the overall level of total variance (larger $a$, since variance accumulates over time), the flatter the minimum (larger $\sigma$, since the market disagrees less about long-run volatility than short-run), and typically a somewhat weaker left skew (short-dated options are more exposed to near-term price shocks and the leverage effect). SVI fitting in the project is done independently for each expiry; in practice one still has to check that adjacent expiries don't create **calendar arbitrage** (i.e. near-month total variance must not exceed far-month) before the stitched-together surface can be trusted.

If too few data points are available in a given window, the fit degrades to an uncalibrated **flat 50% volatility surface** and prints a warning — this is an engineering fallback, not a theoretically correct surface; it only exists to keep downstream modules from crashing on a failed fit.

## 3. Quoter: pricing and quoting

The backtest's core is four modules with clearly separated responsibilities, tied together into a closed loop through a single ledger (`Inventory`) — the four sections starting here work through `Quoter`, `Inventory` & `RiskLimits`, `Hedger`, and `FillModel` in turn, and the final section shows how they close the loop via `Inventory`.

`Quoter`'s output, given a contract, is a pair of directly postable (bid, ask) quotes, computed in three steps.

### 3.1 Computing fair value

Look up the implied volatility $\sigma$ that the surface assigns to this contract (a specific strike and expiry), and substitute it along with the underlying price $F$, strike $K$, and time to expiry $\tau$ into Black-76 to get the contract's theoretical value:

$$
\text{fair} = \text{Black76}(F, K, \tau, \sigma) \tag{4}
$$

The `greeks` module simultaneously computes this contract's delta, gamma, vega, and theta, which feed into the next two steps.

### 3.2 Widening the half-spread with vega/gamma

Rather than adding or subtracting a fixed dollar amount, the half-spread itself scales up with vega and gamma:

$$
\text{half-spread} = \text{base} + k_1|\text{vega}| + k_2|\text{gamma}| \tag{5}
$$

where base is a floor spread covering fees and model error, and $k_1$, $k_2$ are two calibrated coefficients. The intuition: high vega means the contract is sensitive to shifts in the volatility outlook, so a bad move there can hurt more; high gamma means delta drifts quickly with the underlying price, and a hedge that can't keep up risks losing control of the exposure. Both of these "harder to manage later" risks get priced into the spread right at quote time.

### 3.3 Inventory skew: shifting the whole quote band

Read the current net position direction from `Inventory`; if the desk is already substantially net short (delta already very negative), shift the entire quote band upward by a skew amount:

$$
\text{bid} = \text{fair} - \text{half-spread} + \text{skew}, \qquad \text{ask} = \text{fair} + \text{half-spread} + \text{skew} \tag{6}
$$

Skew moves opposite to the current net position — the more skewed the position, the larger the shift — so the bid moves closer to fair (more willing to buy back) and the ask is pushed higher (less willing to sell more), using the asymmetry of the quote to encourage the market to work off the inventory rather than paying to hedge it out actively every time.

Putting it together: the surface supplies $\sigma$ → Eq. (4) produces fair value and the Greeks → Eq. (5) uses vega/gamma to size the spread → Eq. (6) uses current inventory to decide which way to shift the band — the resulting (bid, ask) pair is exactly the input that `FillModel` checks next to decide whether it gets hit.

## 4. Inventory and RiskLimits: bookkeeping and the brake

Together these two manage whether an already-taken position is healthy: `Inventory` keeps the books, and `RiskLimits` applies the brake when the books go out of bounds.

### 4.1 Inventory: aggregating net position and net Greeks

Every time a trade fills, `FillModel` feeds the result back to `Inventory`, which updates the holding $q_i$ (net contracts held in instrument $i$; a market-maker short position is recorded as negative). What `Inventory` maintains in real time is not each contract's individual Greeks, but the **net exposure** aggregated by holding size:

$$
\Delta_{\text{net}} = \sum_i q_i\delta_i, \qquad \Gamma_{\text{net}} = \sum_i q_i\gamma_i, \qquad \nu_{\text{net}} = \sum_i q_i\nu_i, \qquad \Theta_{\text{net}} = \sum_i q_i\theta_i \tag{7}
$$

where $\delta_i$, $\gamma_i$, $\nu_i$, $\theta_i$ are contract $i$'s current Greeks (computed live from the surface and Black-76). These four net values in Eq. (7) are the book's "vital signs": `Quoter` uses the sign and magnitude of $\Delta_{\text{net}}$ to set the direction and size of the inventory skew in Section 3.3, `Hedger` uses $\Delta_{\text{net}}$ to decide whether to trigger a hedge, and `RiskLimits` checks all four net values against their respective thresholds.

### 4.2 RiskLimits: pausing one side of the quote once a limit is breached

`RiskLimits` sets an upper and lower bound on each net value in Eq. (7) — for example $|\Delta_{\text{net}}| \le \Delta_{\max}$, $|\Gamma_{\text{net}}| \le \Gamma_{\max}$, $|\nu_{\text{net}}| \le \nu_{\max}$ — and separately caps the holding $|q_i|$ of any single contract, to keep an illiquid, rarely-traded contract from passively building an outsized exposure. The check fires every time `Inventory` updates; once a net value crosses its threshold, `RiskLimits` **does not force-close existing positions** — instead it pauses taking on more risk in that same direction. For instance, if $\nu_{\text{net}}$ is already too positive (net long volatility), quoting on the sell-options side is paused while the buy side stays open, until $\nu_{\text{net}}$ is pulled back within bounds by subsequent hedging or offsetting fills, at which point two-sided quoting resumes.

The division of labor: `Inventory` is the system's single source of truth for net exposure, and `RiskLimits` reads that ledger to decide "should we take on any more position" — the gate on inflow. It does not actively work down existing exposure; that responsibility belongs to `Hedger`, covered next.

## 5. Hedger: actively working down existing risk

At every hedge-check point, `Hedger` uses futures/perpetual contracts to offset part of the $\Delta_{\text{net}}$ (Eq. (7)) that `Inventory` has aggregated, using one of three rules, from simplest to most refined:

### 5.1 Interval hedging

Triggered at a fixed time interval (e.g. every 5 minutes), flattening $\Delta_{\text{net}}$ to zero. The simplest logic, but no adjustment happens between triggers regardless of how the market moves, so the response to a sudden move is slow and exposure can already be substantial by the time the next trigger fires.

### 5.2 Fixed-band hedging

Set a band $H$; a hedge only triggers when $|\Delta_{\text{net}}| > H$, and it pulls $\Delta_{\text{net}}$ back only to the band edge $\pm H$ rather than to zero:

$$
\text{Trigger condition: } |\Delta_{\text{net}}| > H \;\Rightarrow\; \text{hedge size} = \Delta_{\text{net}} - \operatorname{sign}(\Delta_{\text{net}})\cdot H \tag{8}
$$

No hedge fires when moves are small, saving on hedging fees, while a large move is caught promptly enough to keep exposure from running away. The band $H$ is typically a fixed number set by hand, not adapted to market conditions.

The hedge trade incurs a fee and half the bid-ask spread — a real transaction-cost drag that shows up in the final PnL attribution. `Hedger` and `RiskLimits` are complementary: one works down the stock of risk, the other limits the flow into it.

### 5.3 Future work: Whalley–Wilmott optimal band

`Hedger` currently implements only the two rules in 5.1 and 5.2, both with a fixed, hand-set band $H$. The planned third rule lets the band itself be computed dynamically, following Whalley & Wilmott (1997): trading off transaction cost against exposure risk yields a theoretically optimal band

$$
H^*(t) \propto \left(\frac{\Gamma_{\text{net}}^2 F^2 \kappa}{\lambda}\right)^{1/3} \tag{9}
$$

where $\Gamma_{\text{net}}$ is the current net gamma (Eq. (7)), $F$ is the underlying price, $\kappa$ is the per-unit transaction cost of hedging, and $\lambda$ is a risk-aversion coefficient. The intuition: larger gamma means delta drifts faster, so the band should narrow and hedging should happen more often; higher transaction cost means the band should widen to trade less often; higher risk aversion (less tolerance for exposure swings) should also narrow the band. In production this would mean recomputing $H^*(t)$ at every hedge-check point and substituting it for the fixed $H$ in the trigger logic of Eq. (8).

What remains unimplemented is mainly calibrating the two parameters $\kappa$ and $\lambda$ — the current data volume isn't yet enough to reliably estimate per-unit hedging cost and risk aversion, which is itself a direct consequence of the "insufficient data" bottleneck noted in Section 9.

## 6. FillModel: deciding when a quote gets hit

`FillModel` decides when a posted quote counts as filled, offering two modes.

### 6.1 Poisson theoretical matching

Assumes fills follow a Poisson process whose intensity decays with spread: the smaller the distance $\delta$ between the quote and fair value, the higher the fill intensity, commonly modeled as exponential decay:

$$
\lambda(\delta) = Ae^{-k\delta} \tag{10}
$$

where $A$ is the base fill intensity when quoting right at fair value, and $k$ controls how quickly intensity decays with spread. Over a time slice of length $dt$, the probability of this quote being hit is approximately $\lambda(\delta)\,dt$. This mode requires no real trade data at all, only calibrating the two parameters $A$, $k$, so it can keep a backtest running even when data — or trade-replay samples in particular — is sparse; the tradeoff is that fill behavior is assumed rather than observed, and may diverge from the market's actual fill dynamics.

### 6.2 Trade-replay

Replays real trades that actually happened on Deribit: walking through historical trades in time order, whenever a real trade price $p_{\text{trade}}$ appears, check whether it crosses the quote standing at that moment —

$$
p_{\text{trade}} \ge \text{ask} \;\Rightarrow\; \text{deemed a sell}, \qquad p_{\text{trade}} \le \text{bid} \;\Rightarrow\; \text{deemed a buy} \tag{11}
$$

If it crosses, a fill is recorded — at the posted bid/ask (not at $p_{\text{trade}}$ itself), on the logic that a counterparty would have traded against the quote itself had it really been resting there. This mode is grounded entirely in trading activity that actually happened, requiring no assumed distribution and staying closer to reality, but it depends on the density of historical trades: illiquid expiries and deep out-of-the-money contracts see real fills only rarely, and a trigger may not occur for a long stretch, leaving too few samples.

Once filled, `FillModel` feeds the result back to `Inventory` to update the position, and records an **edge** (the difference between the fill price and fair value at that moment) — money earned purely from the quoted spread, tracked separately as its own line item in PnL attribution.

## 7. Data flow across the four modules

An analogy helps organize the four roles: think of the whole market-making system as a small factory. `Quoter` is the "pricer," deciding only what price each order should be quoted at; `FillModel` is the "receiving clerk," deciding whether an order was actually taken; `Inventory` is the "ledger," recording how much stock the factory currently owes or is holding; `RiskLimits` is the "gatekeeper," deciding whether new orders can still be accepted; `Hedger` is the "stock clearer," periodically working down accumulated inventory. Each role operates independently, but all of them report to — or read from — the same ledger, which is what keeps the whole factory from falling into chaos.

The data flow is shown in Figure 2.

*Figure 2: Vol surface (`Surface`) → `Quoter` (post quote) → `FillModel` (check fill) → `RiskLimits` (pause on breach) / `Hedger` (hedge with futures) → `Inventory` (update net position). Solid lines are the main decision chain; the two dashed lines are feedback loops, carrying the latest results from `RiskLimits` and `Hedger` back to `Quoter`, used on the next cycle to pause one side of quoting or adjust the inventory skew. (Diagram — see the PDF version.)*

## 8. PnL attribution: where the money actually comes from

Position value $V$ is a function of the underlying price $F$, implied volatility $\sigma$, and time $t$. A multivariate Taylor expansion decomposes the change in position value $dV$ over some interval into several terms:

$$
\text{PnL} \approx \text{edge} + \Delta\cdot dF + \tfrac{1}{2}\Gamma\cdot dF^2 + \Theta\cdot dt + \nu\cdot d\sigma - \text{hedging cost} \tag{12}
$$

where edge is the only term in Eq. (12) that doesn't come from a Greek — it is the difference between fill price and fair value (see Section 6); $\Delta$, $\Gamma$, $\Theta$, $\nu$ are the position's net delta, gamma, theta, and vega at the start of the interval (aggregated by `Inventory`); $dF$, $d\sigma$, $dt$ are the changes in underlying price, implied volatility, and time over the interval; and hedging cost in Eq. (12) is the sum of fees and half-spread incurred by `Hedger`.

Substituting the starting Greeks into each term gives a theoretical contribution, which is then compared against the account's actual realized PnL; the difference is recorded as the **residual**:

$$
\text{residual} = \text{actual PnL} - \left(\text{edge} + \Delta\,dF + \tfrac{1}{2}\Gamma\,dF^2 + \Theta\,dt + \nu\,d\sigma - \text{hedging cost}\right) \tag{13}
$$

The residual in Eq. (13) mainly comes from three sources: the Taylor expansion is truncated at second order, dropping third-order and higher terms; second-order cross Greeks such as vanna and volga aren't broken out separately; and there is discretization error between hedge-check points. A smaller residual share means the attribution framework is more trustworthy, and that hedging frequency and Greek computation are on solid ground.

Summing every interval's attribution over a full backtest run answers the question of where this market-making system's money actually comes from: edge and theta are typically relatively stable income terms, while gamma's negative contribution and hedging costs are the unavoidable price of discrete hedging; what's left after netting the two is what the system genuinely earns — not the single, uninformative number of total account PnL.

## 9. Current bottleneck

The full chain — Deribit → recording → parquet → loading → implied vol/SVI surface → quoting + inventory + fill matching → event loop (hedging included) → PnL attribution → metrics/plots — is completely wired up at the code level. The one remaining bottleneck is **Step 3**: when the data volume is too small, the surface fit degrades to an uncalibrated flat 50% surface, and every downstream number — quotes, hedges, attribution — is then built on that placeholder surface and carries no real meaning. This isn't a logic bug; it's an inevitable waiting period until enough data has accumulated to support a genuine fit.
