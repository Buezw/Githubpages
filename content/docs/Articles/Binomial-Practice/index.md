---
title: "Binomial Probability Law: Practice Problems"
lang: en
date: "2026-09-21"
tags: ["Probability"]
summary: "20 practice questions on Bernoulli trials and the binomial law, easiest to hardest, with answer key and full worked solutions."
---

> Last Edit: 11/26/26

Based on Lecture Notes 4 (Bernoulli Trials, Sequential Experiments & the Binomial Probability Law). All 20 questions are ordered from easiest to hardest. Choose the best answer. The answer key and full worked solutions follow the questions.

Throughout, $X$ denotes the number of successes in $n$ independent Bernoulli trials, each with success probability $p$, so that

$$
P[X=k] = \binom{n}{k}p^k(1-p)^{n-k}, \qquad k = 0, 1, \dots, n.
$$

**Coverage map:**

| Concept | Question(s) |
|:---|:---|
| Recognizing a valid Bernoulli-trial / binomial setup | Q1, Q2 |
| Exactly $k$ successes, direct use of the formula | Q3, Q4 |
| Where $\binom{n}{k}$ comes from: counting sequences | Q5 |
| "At least one" via complementary events | Q6, Q7 |
| Cumulative probabilities $P[X \le k]$, $P[X \ge k]$ | Q8, Q9 |
| Normalization and the binomial theorem | Q10 |
| Solving for $n$ (design / sizing problems) | Q11, Q12 |
| Binomial law combined with conditional probability | Q13, Q14 |
| Most probable number of successes (the mode) | Q15 |
| Repetition coding and majority-vote decoding | Q16 |
| Error-correcting codes, $P[X>t]$ | Q17 |
| When the binomial law fails (sampling without replacement) | Q18 |
| Binomial law inside the law of total probability | Q19 |
| Bayes' theorem with a binomial likelihood (capstone) | Q20 |

## Questions

### Question 1 — Difficulty: Easy

Which of the following experiments is a valid sequence of Bernoulli trials, so that the binomial probability law may be applied directly?

- (A) A fair die is rolled 10 times and the face value of each roll is recorded.
- (B) A fair die is rolled 10 times and each roll is recorded only as "6" or "not 6".
- (C) Five cards are drawn without replacement from a 52-card deck and the number of hearts is counted.
- (D) The voltage across a resistor is measured 10 times and the average is recorded.

### Question 2 — Difficulty: Easy

A fair die is rolled 10 times. Let $X$ be the number of 6s obtained. Find $P[X=2]$.

(A) $\approx 0.2907$　(B) $\approx 0.0278$　(C) $\approx 0.1938$　(D) $\approx 0.3333$

### Question 3 — Difficulty: Easy

A binary channel has bit error rate $p=0.01$, and bit errors occur independently. An 8-bit word is transmitted. Find the probability that exactly one bit is received in error.

(A) $\approx 0.0100$　(B) $\approx 0.0746$　(C) $\approx 0.0800$　(D) $\approx 0.9227$

### Question 4 — Difficulty: Easy–Medium

Six independent Bernoulli trials are performed, each with success probability $p=0.2$. Find the probability of exactly 2 successes.

(A) $\approx 0.0400$　(B) $\approx 0.2458$　(C) $\approx 0.0164$　(D) $\approx 0.3333$

### Question 5 — Difficulty: Easy–Medium

Consider $n=5$ independent Bernoulli trials with $p=0.3$. How many distinct outcome sequences contain exactly 2 successes, and what is the probability of each *individual* such sequence?

- (A) 10 sequences, each with probability 0.0309
- (B) 20 sequences, each with probability 0.0309
- (C) 10 sequences, each with probability 0.3087
- (D) 25 sequences, each with probability 0.0900

### Question 6 — Difficulty: Medium

Ten independent Bernoulli trials are performed with $p=0.1$. Find the probability of at least one success.

(A) $\approx 0.1000$　(B) $\approx 0.3487$　(C) $\approx 0.6513$　(D) $1.0000$

### Question 7 — Difficulty: Medium

A system contains 20 components that fail independently, each with probability 0.02 during a mission. Find the probability that at least one component fails.

(A) $\approx 0.0200$　(B) $\approx 0.4000$　(C) $\approx 0.6676$　(D) $\approx 0.3324$

### Question 8 — Difficulty: Medium

A fair coin is tossed 6 times. Find the probability of at most 2 heads.

(A) $\approx 0.3438$　(B) $\approx 0.2344$　(C) $\approx 0.6563$　(D) $\approx 0.5000$

### Question 9 — Difficulty: Medium

Five independent Bernoulli trials are performed with $p=0.2$. Find the probability of at least 2 successes.

(A) $\approx 0.2627$　(B) $\approx 0.6723$　(C) $\approx 0.7373$　(D) $\approx 0.2048$

### Question 10 — Difficulty: Medium

Let $q = 1-p$. For every $n \ge 1$ and every $p \in [0,1]$, the quantity $\sum_{k=0}^{n}\binom{n}{k}p^kq^{n-k}$ has the same value. What is that value, and what guarantees it?

- (A) $2^n$, since there are $2^n$ possible outcome sequences.
- (B) $np$, since that is the expected number of successes.
- (C) $1$, since the sum equals $(p+q)^n$ by the binomial theorem.
- (D) $p^n$, since the trials are independent.

### Question 11 — Difficulty: Medium–Hard

Each transmission attempt succeeds with probability 0.3, independently of all others. What is the minimum number of attempts needed so that the probability of at least one success is at least 0.99?

(A) 4　(B) 10　(C) 13　(D) 12

### Question 12 — Difficulty: Medium–Hard

A packet is retransmitted repeatedly over a link; each transmission succeeds independently with probability 0.8. What is the minimum number of transmissions needed so that the probability of at least one success is at least 0.9999?

(A) 4　(B) 5　(C) 6　(D) 9

### Question 13 — Difficulty: Medium–Hard

Ten independent Bernoulli trials are performed with $p=0.1$. Given that at least one success occurred, find the probability that exactly one success occurred.

(A) $\approx 0.3874$　(B) $\approx 0.5948$　(C) $\approx 0.1000$　(D) $\approx 0.6513$

### Question 14 — Difficulty: Hard

A fair coin is tossed 4 times. Given that at least 2 heads occurred, find the probability that exactly 3 heads occurred.

(A) $0.2500$　(B) $\approx 0.3636$　(C) $\approx 0.6875$　(D) $0.5000$

### Question 15 — Difficulty: Hard

Let $X$ be the number of successes in $n=10$ independent Bernoulli trials with $p=0.25$. Which value of $k$ maximizes $P[X=k]$?

(A) $k=2$　(B) $k=3$　(C) $k=5$　(D) All values of $k$ are equally likely.

### Question 16 — Difficulty: Hard

A $(5,1)$ repetition code sends each information bit five times over a binary symmetric channel with crossover probability $p=0.1$; bit errors are independent. The receiver decodes by majority vote. Find the probability of a decoding error.

(A) $\approx 0.0086$　(B) $\approx 0.0081$　(C) $\approx 0.0280$　(D) $\approx 0.5000$

### Question 17 — Difficulty: Hardest

A packet contains 100 bits. Each bit is received in error independently with probability $p=0.001$. The error-correcting code in use can correct up to 2 bit errors per packet, and fails otherwise. Find the probability of a decoding failure.

(A) $\approx 1.5\times10^{-4}$　(B) $\approx 4.5\times10^{-3}$　(C) $\approx 9.5\times10^{-2}$　(D) $\approx 1.0\times10^{-3}$

### Question 18 — Difficulty: Hardest

A box contains 10 chips, of which 3 are defective. Four chips are drawn *without replacement*. Find the probability that exactly one of the four is defective, and state whether the binomial probability law applies.

- (A) $\approx 0.4116$; the binomial law applies with $n=4$, $p=0.3$.
- (B) $0.5000$; the binomial law does not apply, because the trials are neither independent nor identical.
- (C) $0.5000$; the binomial law applies with $n=4$, $p=0.3$.
- (D) $0.3000$; the binomial law does not apply, so no numerical answer can be obtained.

### Question 19 — Difficulty: Hardest

A channel is in a *good* state with probability 0.7 (bit error rate 0.001) or in a *bad* state with probability 0.3 (bit error rate 0.05). The state is selected once, before transmission, and remains fixed for an entire packet; given the state, bit errors are independent. A 10-bit packet is transmitted. Find the probability that the packet contains no bit errors.

(A) $\approx 0.8727$　(B) $\approx 0.8536$　(C) $\approx 0.9900$　(D) $\approx 0.5987$

### Question 20 — Difficulty: Hardest

Using the same channel as Question 19, suppose a 10-bit packet arrives with no bit errors. Find the probability that the channel was in the good state.

(A) $0.7000$　(B) $\approx 0.7942$　(C) $\approx 0.6930$　(D) $\approx 0.9900$

## Answer Key

| Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Ans** | B | A | B | B | A | C | D | A | A | C |

| Q | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Ans** | C | C | B | B | A | A | A | B | A | B |

## Solutions

### Solution 1 — (B)

The binomial law requires four things: a fixed number of trials $n$; exactly two outcomes per trial; the same success probability $p$ on every trial; and independence between trials.

(A) and (D) fail the two-outcome requirement — the recorded quantity is not binary. (C) fails independence and identical distribution: after a heart is removed, the fraction of hearts remaining changes, so $p$ is not constant. Only (B) satisfies all four, with $n=10$ and $p=1/6$.

### Solution 2 — (A)

Here $n=10$, $p=1/6$, $k=2$:

$$
P[X=2] = \binom{10}{2}\left(\frac{1}{6}\right)^2\left(\frac{5}{6}\right)^8 = 45 \times 0.02778 \times 0.23257 \approx 0.2907.
$$

Choice (B) is $(1/6)^2$ alone — the probability of one specific sequence with the wrong tail factor. Choice (D) is $2/6$, which is not a probability of anything here.

### Solution 3 — (B)

$n=8$, $p=0.01$, $k=1$:

$$
P[X=1] = \binom{8}{1}(0.01)^1(0.99)^7 = 8 \times 0.01 \times 0.93207 \approx 0.0746.
$$

Choice (C), 0.0800, is what you get by dropping the $(0.99)^7$ factor; choice (D), $(0.99)^8 = 0.9227$, is $P[X=0]$.

### Solution 4 — (B)

$$
P[X=2] = \binom{6}{2}(0.2)^2(0.8)^4 = 15 \times 0.04 \times 0.4096 \approx 0.2458.
$$

Choice (C) is $(0.2)^2(0.8)^4 = 0.0164$, the probability of one specific sequence — it is missing the factor $\binom{6}{2} = 15$ that counts how many such sequences exist.

### Solution 5 — (A)

This question isolates the two halves of the formula.

**How many sequences:** choosing which 2 of the 5 positions are successes gives $\binom{5}{2} = 10$. (Choice (B), $20 = 5!/3!$, is the count you get if you forget to divide by $2!$, i.e. if you treat the two successes as distinguishable.)

**Probability of each one:** by independence, any specific sequence with 2 successes and 3 failures has probability $p^2(1-p)^3 = (0.3)^2(0.7)^3 = 0.0309$, regardless of the order in which they appear.

Multiplying gives $P[X=2] = 10 \times 0.0309 = 0.3087$, which is choice (C) — the value of the *total*, not of each individual sequence.

### Solution 6 — (C)

Use the complementary event: "at least one success" is the complement of "zero successes," which is a single term instead of ten.

$$
P[X \ge 1] = 1 - P[X=0] = 1 - (0.9)^{10} = 1 - 0.3487 \approx 0.6513.
$$

### Solution 7 — (D)

$n=20$, $p=0.02$, and again "at least one" calls for the complement:

$$
P[X \ge 1] = 1 - (0.98)^{20} = 1 - 0.6676 \approx 0.3324.
$$

Choice (B), $20 \times 0.02 = 0.4$, is the classic error of adding the individual failure probabilities. That sum overcounts the outcomes in which two or more components fail, and it is only a usable approximation (an upper bound, by the union bound) when $np$ is small. Note also $E[X] = np = 0.4$: the expected number of failures and the probability of at least one failure are different quantities.

### Solution 8 — (A)

With $p=0.5$ every one of the $2^6 = 64$ sequences is equally likely, so the calculation reduces to counting:

$$
P[X \le 2] = \frac{\binom{6}{0} + \binom{6}{1} + \binom{6}{2}}{2^6} = \frac{1+6+15}{64} = \frac{22}{64} \approx 0.3438.
$$

Choice (B), $15/64$, is $P[X=2]$ only; "at most 2" must include $k=0$ and $k=1$.

### Solution 9 — (A)

"At least 2" has 4 terms; its complement has 2, so complement the event:

$$
P[X \ge 2] = 1 - P[X=0] - P[X=1] = 1 - (0.8)^5 - \binom{5}{1}(0.2)(0.8)^4 = 1 - 0.3277 - 0.4096 \approx 0.2627.
$$

Choice (B), 0.6723, subtracts only $P[X=0]$ — a reflex carried over from "at least one" problems. The complement of $\{X \ge 2\}$ is $\{X \le 1\}$, not $\{X=0\}$.

### Solution 10 — (C)

The terms $\binom{n}{k}p^kq^{n-k}$ are exactly the terms of the binomial expansion of $(p+q)^n$, so

$$
\sum_{k=0}^{n}\binom{n}{k}p^kq^{n-k} = (p+q)^n = 1^n = 1,
$$

since $q = 1-p$. This is both the source of the name "binomial law" and a useful sanity check: if your computed probabilities do not sum to 1, something is wrong.

### Solution 11 — (C)

$$
1 - (0.7)^n \ge 0.99 \iff (0.7)^n \le 0.01 \iff n \ge \frac{\ln 0.01}{\ln 0.7} = \frac{-4.6052}{-0.3567} = 12.91.
$$

Since $n$ must be an integer, $n=13$. Verify: $(0.7)^{12} = 0.0138 > 0.01$, while $(0.7)^{13} = 0.0097 \le 0.01$.

Two things to watch. First, dividing both sides by $\ln 0.7 < 0$ *reverses* the inequality — this is the most common error on this type of question. Second, always round *up*: $n=12$ does not meet the requirement.

### Solution 12 — (C)

Failure probability per attempt is 0.2:

$$
(0.2)^n \le 10^{-4} \iff n \ge \frac{\ln 10^{-4}}{\ln 0.2} = \frac{-9.2103}{-1.6094} = 5.72 \implies n = 6.
$$

Check: $(0.2)^5 = 3.2\times10^{-4} > 10^{-4}$, and $(0.2)^6 = 6.4\times10^{-5} \le 10^{-4}$.

### Solution 13 — (B)

Since $\{X=1\} \subset \{X \ge 1\}$, the intersection in the numerator is just $\{X=1\}$:

$$
P[X=1 \mid X \ge 1] = \frac{P[X=1]}{P[X \ge 1]} = \frac{\binom{10}{1}(0.1)(0.9)^9}{1-(0.9)^{10}} = \frac{0.3874}{0.6513} \approx 0.5948.
$$

Conditioning on $\{X \ge 1\}$ removes the 34.9% of outcomes with no successes and renormalizes what remains, which is why 0.3874 rises to 0.5948.

### Solution 14 — (B)

With $p=0.5$ and $n=4$, all 16 sequences are equally likely:

$$
P[X=3] = \frac{\binom{4}{3}}{16} = \frac{4}{16}, \qquad P[X \ge 2] = \frac{\binom{4}{2} + \binom{4}{3} + \binom{4}{4}}{16} = \frac{6+4+1}{16} = \frac{11}{16}.
$$

$$
P[X=3 \mid X \ge 2] = \frac{4/16}{11/16} = \frac{4}{11} \approx 0.3636.
$$

### Solution 15 — (A)

Take the ratio of consecutive terms:

$$
\frac{P[X=k]}{P[X=k-1]} = \frac{n-k+1}{k} \cdot \frac{p}{1-p}.
$$

The probabilities increase while this ratio exceeds 1 and decrease once it drops below 1, so the maximizing $k$ (the *mode*) is $k^* = \lfloor (n+1)p \rfloor$. Here $(n+1)p = 11 \times 0.25 = 2.75$, giving $k^* = 2$.

Direct check: $P[X=1] = 0.1877$, $P[X=2] = 0.2816$, $P[X=3] = 0.2503$.

The trap is choice (B): $E[X] = np = 2.5$, and the mean is *not* in general the most probable value. The mode is near $np$, but it is obtained by flooring $(n+1)p$, not by rounding $np$.

### Solution 16 — (A)

Majority vote over 5 received bits decodes incorrectly exactly when 3, 4, or 5 of the bits are in error:

$$
\begin{aligned}
P_{\text{err}} &= \binom{5}{3}(0.1)^3(0.9)^2 + \binom{5}{4}(0.1)^4(0.9) + \binom{5}{5}(0.1)^5 \\
&= 10(0.001)(0.81) + 5(0.0001)(0.9) + 0.00001 \\
&= 0.00810 + 0.00045 + 0.00001 \approx 0.0086.
\end{aligned}
$$

Choice (B) keeps only the $k=3$ term; choice (C), 0.028, is the answer for a $(3,1)$ repetition code. Note the trade-off: the error probability drops from 0.1 to 0.0086, but the code rate drops to $1/5$.

### Solution 17 — (A)

A decoding failure means 3 or more errors, so complement the event:

$$
P[X \ge 3] = 1 - P[X=0] - P[X=1] - P[X=2].
$$

$$
\begin{aligned}
P[X=0] &= (0.999)^{100} = 0.90479, \\
P[X=1] &= \binom{100}{1}(0.001)(0.999)^{99} = 0.09057, \\
P[X=2] &= \binom{100}{2}(0.001)^2(0.999)^{98} = 4950 \times 10^{-6} \times 0.90660 = 0.00449.
\end{aligned}
$$

$$
P[X \ge 3] = 1 - 0.99985 \approx 1.5\times10^{-4}.
$$

Sanity check: with $n$ large, $p$ small and $\lambda = np = 0.1$, the Poisson approximation gives $1 - e^{-0.1}(1 + 0.1 + 0.005) = 1.55\times10^{-4}$ — close enough to confirm the arithmetic. Choice (C), $9.5\times10^{-2}$, is $1 - P[X=0] = P[X \ge 1]$, the probability that the packet has *any* error, which is not the same as a decoding failure for a code that corrects up to 2.

### Solution 18 — (B)

The binomial law does **not** apply. Drawing without replacement makes the trials dependent and non-identical: the probability that the second chip is defective depends on what the first chip was. The correct model is the *hypergeometric law*:

$$
P[\text{exactly 1 defective}] = \frac{\binom{3}{1}\binom{7}{3}}{\binom{10}{4}} = \frac{3 \times 35}{210} = 0.5.
$$

Choice (A) is the binomial answer $\binom{4}{1}(0.3)(0.7)^3 = 0.4116$, which is what you would get *with* replacement.

The decision rule: sampling with replacement (or from an effectively infinite population) ⇒ binomial; sampling without replacement from a finite population ⇒ hypergeometric.

### Solution 19 — (A)

Condition on the channel state and apply the law of total probability. Given a state, the 10 bits are independent Bernoulli trials, so $P[0 \text{ errors} \mid \text{state}] = (1 - p_{\text{state}})^{10}$:

$$
\begin{aligned}
P[0 \text{ errors}] &= P[0 \text{ errors} \mid G]\,P[G] + P[0 \text{ errors} \mid B]\,P[B] \\
&= (0.999)^{10}(0.7) + (0.95)^{10}(0.3) \\
&= (0.99004)(0.7) + (0.59874)(0.3) \\
&= 0.69303 + 0.17962 \approx 0.8727.
\end{aligned}
$$

Choice (B), 0.8536, is the tempting shortcut: average the two error rates into $\bar p = 0.7(0.001) + 0.3(0.05) = 0.0157$ and compute $(1-\bar p)^{10}$. That is wrong, because the unconditional bit errors are *not* independent — they share the common state. Knowing that bit 1 was in error makes the bad state more likely, which makes bit 2 more likely to be in error too. Averaging $p$ first destroys exactly that correlation.

### Solution 20 — (B)

Bayes' theorem, with the binomial (here, $k=0$) probability as the likelihood. The denominator is the total probability already computed in Question 19:

$$
P[G \mid 0 \text{ errors}] = \frac{P[0 \text{ errors} \mid G]\,P[G]}{P[0 \text{ errors}]} = \frac{(0.999)^{10}(0.7)}{0.8727} = \frac{0.69303}{0.87265} \approx 0.7942.
$$

The prior $P[G] = 0.7$ is updated to a posterior of 0.794: an error-free packet is evidence in favour of the good state, since the good state produces one with probability 0.990 versus only 0.599 for the bad state. This is the standard structure of a channel state estimator — a binomial likelihood driving a Bayesian update.
