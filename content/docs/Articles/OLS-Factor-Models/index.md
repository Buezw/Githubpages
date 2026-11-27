---
title: "OLS Factor Models: CAPM and Fama–French Three-Factor"
lang: en
date: "2026-09-14"
tags: ["Factor Models", "Regression"]
summary: "Hand-calculated OLS examples for CAPM and FF3, then a real-data application to AAPL (2021-08 to 2026-07)."
---

> Last Edit: 11/26/26

*Hand-Calculated Worked Examples, and a Real-Data Application to AAPL*

**Purpose of this document.** This report has three parts. Part I derives the OLS factor-loading estimator from first principles and walks a fully hand-computed CAPM example with a small, illustrative dataset. Part II does the same for the Fama–French three-factor model. Part III applies both models to real historical market data for Apple Inc. (AAPL), fetched from Yahoo! Finance and Kenneth R. French's Data Library, with every regression cross-checked against statsmodels. Parts I–II use small, clearly labeled illustrative datasets chosen so the arithmetic is easy to verify by hand; they are not real market data. Part III uses only real data.

# Part I — CAPM: Worked Example

## 1. Model and setup

The Capital Asset Pricing Model (CAPM) regression is

$$
R_i - R_f = \alpha + \beta(R_m - R_f) + \varepsilon,
$$

where $R_i - R_f$ is the stock's excess return and $R_m - R_f$ is the market's excess return. Stacking $T$ months of data,

$$
y \in \mathbb{R}^T, \qquad X \in \mathbb{R}^{T\times 2} = [\mathbf{1} \mid x],
$$

and OLS solves the normal equations $X^\top X\hat\beta = X^\top y$, giving

$$
\boxed{\hat\beta = (X^\top X)^{-1}X^\top y.}
$$

> *Illustrative data below (Table 1) — not real market data. Chosen with round numbers so every step can be verified by hand.*

## 2. Data

*Table 1: Illustrative monthly data ($T=6$)*

| Month | Stock excess return $y$ (%) | Market excess return $x$ (%) |
|:---:|:---:|:---:|
| 1 | 5 | 3 |
| 2 | −2 | −1 |
| 3 | 8 | 4 |
| 4 | 1 | 2 |
| 5 | −3 | −2 |
| 6 | 6 | 3 |

## 3. Computation

$$
X^\top X = \begin{bmatrix} 6 & 9 \\ 9 & 43 \end{bmatrix}, \qquad X^\top y = \begin{bmatrix} 15 \\ 75 \end{bmatrix}, \qquad \det(X^\top X) = 6(43) - 9(9) = 177.
$$

$$
(X^\top X)^{-1} = \frac{1}{177}\begin{bmatrix} 43 & -9 \\ -9 & 6 \end{bmatrix} \implies \hat\beta = \frac{1}{177}\begin{bmatrix} 43(15) - 9(75) \\ -9(15) + 6(75) \end{bmatrix} = \begin{bmatrix} -0.169 \\ 1.780 \end{bmatrix}.
$$

So $\hat\alpha \approx -0.17\%$ and $\hat\beta \approx 1.78$.

## 4. Fit diagnostics: $R^2$ and $t$-statistics

With fitted values $\hat y = -0.169 + 1.780x$, the residuals are $(-0.17, -0.05, 1.05, -2.39, 0.73, 0.83)$, giving

$$
SSR = 8.068, \qquad SST = 101.5, \qquad R^2 = 1 - \frac{SSR}{SST} \approx 0.9205.
$$

With $T-2=4$ degrees of freedom, $\hat\sigma^2 = SSR/4 = 2.017$. Using $\sum(x_i - \bar x)^2 = 29.5$ and $\bar x = 1.5$:

$$
SE(\hat\beta) = \sqrt{\hat\sigma^2/29.5} \approx 0.2615, \qquad SE(\hat\alpha) = \sqrt{\hat\sigma^2\left(\frac{1}{6} + \frac{1.5^2}{29.5}\right)} \approx 0.700.
$$

*Table 2: CAPM results (illustrative data)*

| Parameter | Estimate | Std. Error | $t$-statistic |
|:---|:---:|:---:|:---:|
| $\hat\alpha$ | −0.17% | 0.70 | −0.24 |
| $\hat\beta$ | 1.78 | 0.26 | **6.81** |

**Interpretation.** $\beta$'s $t$-statistic (6.81) is large, so the market loading is reliably different from zero; $\alpha$'s $t$-statistic (−0.24) is not, so the small negative intercept is indistinguishable from noise. $R^2 \approx 0.92$ means the market factor explains about 92% of this (illustrative) stock's return variance — deliberately high here so the arithmetic is clean; real single-stock CAPM $R^2$ is typically much lower (see Part III).

# Part II — Fama–French Three-Factor: Worked Example

## 5. Model and setup

The three-factor model adds size (SMB) and value (HML) to the market factor:

$$
R_i - R_f = \alpha + \beta_{\text{MKT}}(R_m - R_f) + \beta_{\text{SMB}}\,SMB + \beta_{\text{HML}}\,HML + \varepsilon.
$$

Now $X \in \mathbb{R}^{T\times 4}$ (a column of ones plus three factor columns), and the same estimator applies: $\hat\beta = (X^\top X)^{-1}X^\top y$.

> *Illustrative data below (Table 4) — not real market data, chosen so the market loading is clearly significant while SMB and HML are deliberately weak, to demonstrate how the t-statistic separates real exposures from noise.*

## 6. Data

*Table 3: Illustrative monthly data ($T=12$)*

| Month | MKT | SMB | HML | $y$ |
|:---:|:---:|:---:|:---:|:---:|
| 1 | 3 | 1 | −1 | 6 |
| 2 | −1 | 2 | 0 | −1 |
| 3 | 4 | −1 | 2 | 9 |
| 4 | 2 | 0 | 1 | 4 |
| 5 | −2 | 1 | −1 | −3 |
| 6 | 3 | −2 | 1 | 4 |
| 7 | 1 | 2 | 0 | 3 |
| 8 | −3 | 1 | 2 | −2 |
| 9 | 5 | −1 | −2 | 9 |
| 10 | 0 | 0 | 1 | 1 |
| 11 | 2 | 1 | 0 | 4 |
| 12 | −1 | 2 | 1 | 0 |

## 7. Computation

$$
X^\top X = \begin{bmatrix} 12 & 13 & 6 & 4 \\ 13 & 83 & -17 & -5 \\ 6 & -17 & 22 & 0 \\ 4 & -5 & 0 & 18 \end{bmatrix}, \qquad X^\top y = \begin{bmatrix} 34 \\ 143 \\ -17 \\ 2 \end{bmatrix}.
$$

$$
(X^\top X)^{-1} \approx \begin{bmatrix} 0.2303 & -0.0631 & -0.1115 & -0.0687 \\ -0.0631 & 0.0319 & 0.0418 & 0.0229 \\ -0.1115 & 0.0418 & 0.1082 & 0.0364 \\ -0.0687 & 0.0229 & 0.0364 & 0.0772 \end{bmatrix}
$$

$$
\hat\beta = (X^\top X)^{-1}X^\top y = \begin{bmatrix} \hat\alpha \\ \hat\beta_{\text{MKT}} \\ \hat\beta_{\text{SMB}} \\ \hat\beta_{\text{HML}} \end{bmatrix} = \begin{bmatrix} 0.5723 \\ 1.7479 \\ 0.4219 \\ 0.4695 \end{bmatrix}.
$$

## 8. Fit diagnostics

$$
SSR = 6.82, \qquad SST = 173.67, \qquad R^2 = 1 - \frac{6.82}{173.67} \approx 0.961.
$$

With $T-4=8$ degrees of freedom, $\hat\sigma^2 = 6.82/8 = 0.852$, and standard errors from $\sqrt{\hat\sigma^2 \cdot \operatorname{diag}[(X^\top X)^{-1}]}$:

*Table 4: Fama–French three-factor results (illustrative data)*

| Parameter | Estimate | Std. Error | $t$-statistic |
|:---|:---:|:---:|:---:|
| $\hat\alpha$ | 0.572 | 0.443 | 1.29 |
| $\hat\beta_{\text{MKT}}$ | 1.748 | 0.165 | **10.61** |
| $\hat\beta_{\text{SMB}}$ | 0.422 | 0.304 | 1.39 |
| $\hat\beta_{\text{HML}}$ | 0.470 | 0.257 | 1.83 |

**Interpretation.** Only the market loading clears the usual $\vert t\vert > 2$ threshold. Despite $R^2$ rising to 0.961 from the single-factor case, the SMB and HML loadings themselves are not individually reliable in this illustrative sample — a reminder that $R^2$ and per-coefficient significance answer different questions.

# Part III — Real-Data Application: AAPL

## 9. Data sources and sample

This part uses **real, historical monthly market data** — no simulated or synthetic returns.

- **Stock return data:** Monthly adjusted-close prices for AAPL, downloaded from Yahoo! Finance via the `yfinance` Python package. Monthly simple returns (%) computed as $R_t = 100 \times (P_t/P_{t-1} - 1)$ using adjusted close (dividend- and split-adjusted).
- **Factor data:** Market excess return (Mkt–RF), size (SMB), value (HML), and the risk-free rate (RF), all monthly percent, from Kenneth R. French's Data Library (<https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip>), using only the monthly section of the file.
- **Sample period:** 2021-08 through 2026-07, $T=60$ monthly observations — the last 60 months for which both AAPL price data and Fama–French factor data are jointly available.
- AAPL's excess return each month, $R_t^{AAPL} - RF_t$, is the dependent variable $y$ in both regressions below.

Every regression was computed two independent ways: (1) manually via the OLS normal equations in NumPy, and (2) cross-checked against `statsmodels.api.OLS` and `numpy.linalg.lstsq`. All three methods agreed to within numerical machine precision ($<10^{-12}$).

## 10. Model 1: CAPM

$$
R_t^{AAPL} - RF_t = \alpha + \beta(Mkt_t - RF_t) + \varepsilon_t, \qquad t = 1,\dots,60.
$$

$$
\hat\beta = \begin{bmatrix} \hat\alpha \\ \hat\beta_{\text{MKT}} \end{bmatrix} = \begin{bmatrix} 0.4799 \\ 1.0478 \end{bmatrix}.
$$

*Table 5: CAPM regression, AAPL excess returns, 2021-08 to 2026-07 ($T=60$, real data)*

| Parameter | Estimate | Std. Error | $t$-statistic |
|:---|:---:|:---:|:---:|
| $\alpha$ (intercept) | 0.4799 | 0.7011 | 0.6846 |
| $\beta_{\text{MKT}}$ | 1.0478 | 0.1504 | **6.9646**\* |

\* $\vert t\vert > 2$, significant at approximately the 5% level.

$R^2 = 0.4554$, Adjusted $R^2 = 0.4460$.

**Interpretation.** $\hat\beta_{\text{MKT}} \approx 1.05$ is highly significant ($t \approx 6.96$): AAPL moves essentially one-for-one with the market, with slightly above-average systematic risk. $\hat\alpha \approx 0.48\%$/month is not statistically distinguishable from zero ($t \approx 0.68$) — no reliable evidence of CAPM-abnormal return over this sample. $R^2 \approx 45.5\%$: the market factor alone explains under half of AAPL's month-to-month variance; the remaining $\approx 54.5\%$ is idiosyncratic, firm-specific risk.

## 11. Model 2: Fama–French three-factor

$$
R_t^{AAPL} - RF_t = \alpha + \beta_{\text{MKT}}(Mkt_t - RF_t) + \beta_{\text{SMB}}\,SMB_t + \beta_{\text{HML}}\,HML_t + \varepsilon_t.
$$

$$
\hat\beta = \begin{bmatrix} \hat\alpha \\ \hat\beta_{\text{MKT}} \\ \hat\beta_{\text{SMB}} \\ \hat\beta_{\text{HML}} \end{bmatrix} = \begin{bmatrix} 0.6080 \\ 1.0179 \\ -0.0941 \\ -0.2347 \end{bmatrix}.
$$

*Table 6: Fama–French three-factor regression, AAPL excess returns, 2021-08 to 2026-07 ($T=60$, real data)*

| Parameter | Estimate | Std. Error | $t$-statistic |
|:---|:---:|:---:|:---:|
| $\alpha$ (intercept) | 0.6080 | 0.7352 | 0.8270 |
| $\beta_{\text{MKT}}$ | 1.0179 | 0.1605 | **6.3415**\* |
| $\beta_{\text{SMB}}$ | −0.0941 | 0.2652 | −0.3547 |
| $\beta_{\text{HML}}$ | −0.2347 | 0.1855 | −1.2656 |

\* $\vert t\vert > 2$, significant at approximately the 5% level.

$R^2 = 0.4726$, Adjusted $R^2 = 0.4443$.

**Interpretation.** The market loading remains large and highly significant ($\hat\beta_{\text{MKT}} \approx 1.02$, $t \approx 6.34$). Neither SMB ($t \approx -0.35$) nor HML ($t \approx -1.27$) is significant at the 5% level — consistent with AAPL behaving like a large, growth-oriented stock with no meaningful size or value tilt. The intercept remains statistically indistinguishable from zero. Adding SMB and HML raises $R^2$ only marginally (45.54% → 47.26%), and adjusted $R^2$ actually edges down slightly (44.60% → 44.43%) — the two extra factors add essentially no genuine explanatory power once the market factor is included; roughly 53% of AAPL's return variance remains firm-specific.

## 12. Data verification

Table 7 reproduces the first and last five rows of the 60-row merged dataset (all figures in percent except the date column); the full CSV (`aapl_ff_merged.csv`) is available on request for independent verification.

*Table 7: Merged monthly dataset (excerpt: first and last 5 of 60 rows)*

| Date | AAPL Ret. | Mkt–RF | SMB | HML | RF | AAPL Excess |
|:---|---:|---:|---:|---:|---:|---:|
| 2021-08 | 4.25 | 2.94 | −0.32 | −0.23 | 0.00 | 4.25 |
| 2021-09 | −6.80 | −4.40 | 0.66 | 5.12 | 0.00 | −6.80 |
| 2021-10 | 5.87 | 6.63 | −2.26 | −0.53 | 0.00 | 5.87 |
| 2021-11 | 10.51 | −1.58 | −1.31 | −0.37 | 0.00 | 10.51 |
| 2021-12 | 7.42 | 3.23 | −1.63 | 3.25 | 0.01 | 7.41 |
| ⋮ | | | (50 rows omitted — see attached CSV) | | | ⋮ |
| 2026-03 | −3.93 | −5.18 | 0.44 | 3.29 | 0.29 | −4.22 |
| 2026-04 | 6.92 | 9.95 | 0.19 | −1.37 | 0.29 | 6.63 |
| 2026-05 | 15.11 | 4.91 | −1.59 | −2.31 | 0.31 | 14.80 |
| 2026-06 | −7.27 | −1.07 | 3.39 | 3.58 | 0.29 | −7.56 |
| 2026-07 | 6.76 | −0.60 | −1.96 | 2.11 | 0.33 | 6.43 |

## 13. Summary: illustrative examples vs. real data

*Table 8: Side-by-side comparison*

| | Illustrative (Parts I–II) | Real AAPL data (Part III) |
|:---|:---:|:---:|
| CAPM $R^2$ | 0.92 | 0.46 |
| CAPM $\beta$, $t$-stat | 1.78, $t=6.81$ | 1.05, $t=6.96$ |
| FF3 $R^2$ | 0.96 | 0.47 |
| FF3 $\beta_{\text{MKT}}$, $t$-stat | 1.75, $t=10.61$ | 1.02, $t=6.34$ |
| FF3 SMB/HML significant? | No (illustrative, by design) | No |

**Why the real $R^2$ is so much lower.** The illustrative datasets in Parts I–II were constructed with small, clean residuals purely to make the OLS arithmetic easy to verify by hand. Real single-stock monthly returns are dominated by firm-specific news — earnings surprises, product announcements, litigation, supply-chain events — that have nothing to do with market-wide, size, or value factors. An AAPL CAPM/FF3 $R^2$ in the 45–47% range is, in fact, on the high end for an individual large-cap stock; many mid- and small-cap names see single-factor $R^2$ in the 10–20% range. This is precisely the idiosyncratic-risk share that diversification is designed to remove.
