---
name: quant-strategy-research
description: Guides Claude through structured quantitative investment research — factor design, backtesting methodology, and model evaluation for trading strategies — and should be used when a user wants to research, build, or critique a systematic trading or investment strategy using historical market data.
---

# Quant Strategy Research

This skill helps Claude act as a disciplined quantitative research partner when a user wants to explore, design, backtest, or evaluate systematic investment strategies (factor-based, ML-driven, or rule-based). It brings structure to a domain where it's easy to produce strategies that look great in a backtest but fail in practice due to overfitting, lookahead bias, or unrealistic assumptions.

## When to apply this skill

Apply this skill when the user:
- Wants to design or refine a trading/investment signal ("alpha factor")
- Asks Claude to backtest a strategy against historical price/fundamental data
- Wants to evaluate whether a strategy or model is statistically sound
- Is comparing multiple modeling approaches (rule-based, regression, tree-based, RL) for market prediction
- Needs help structuring a research pipeline: data → features → model → backtest → evaluation
- Asks "does this strategy actually work" or "why does my backtest look too good"

Do not apply this skill for general personal finance questions, single-stock fundamental analysis with no systematic/backtesting component, or requests for real-time trade execution — those are out of scope.

## Core workflow

Walk the user through these phases in order, adapting depth to what they actually need. Skip phases they've already completed, but flag if a later phase reveals a gap in an earlier one.

### 1. Define the research question precisely
Before touching data, pin down:
- What universe of instruments (e.g., US large-cap equities, a specific futures set)?
- What prediction horizon (next day, next week, next quarter)?
- What is the label/target (raw return, risk-adjusted return, relative rank vs. peers)?
- What decision does the signal drive (long-only ranking, long/short, position sizing)?

Vague questions produce untestable strategies — push for specificity here.

### 2. Data and feature design
- Distinguish point-in-time data (what was actually knowable at decision time) from data that includes hindsight (restated financials, survivorship-biased universes). Flag any data source the user describes that isn't clearly point-in-time.
- Encourage features grounded in an economic or behavioral rationale (momentum, value, quality, liquidity, sentiment) rather than pure data-mined correlations. Ask "why would this signal work" before "does this signal work."
- Watch for lookahead bias: features computed using information not available at the time of the trading decision (e.g., using a day's closing price to trade at that day's open).

### 3. Modeling approach
Help the user pick an approach proportional to their data and question:
- Simple rule-based or linear factor models when data is limited or interpretability matters.
- Tree-based/ensemble models (gradient boosting, random forests) for tabular feature sets with nonlinear interactions.
- Sequence models only when there's a genuine temporal-dependency story, not by default.
- Reinforcement learning only when the problem is genuinely sequential-decision-with-feedback (e.g., portfolio rebalancing with transaction costs), not as a first choice — it's the hardest to validate correctly.

Always ask what the simplest baseline is (e.g., equal-weight, buy-and-hold, a single factor) so any added complexity can be justified by out-of-performance over that baseline.

### 4. Backtesting methodology
This is where most strategies quietly fail. Insist on:
- **Walk-forward / out-of-sample splits**, not a single train/test split on shuffled data — market data is time-ordered, and shuffling leaks future information into training.
- **Realistic transaction costs and slippage** — a strategy that only works with zero costs isn't a strategy.
- **Position sizing and risk limits** stated explicitly, not implied.
- **Multiple testing awareness** — if the user tried dozens of factor variants before finding "the one that works," that strategy is likely overfit to noise; ask how many variants were tried.
- Reporting both return and risk metrics together (Sharpe ratio, max drawdown, turnover) — a high return with unbounded drawdown isn't a usable strategy.

### 5. Evaluation and skepticism
When reviewing backtest results the user presents:
- Check whether the out-of-sample period is long enough and distinct enough (different market regime) to be meaningful — a strategy validated only in a single bull market tells you little.
- Ask whether performance is concentrated in a few outlier trades/periods, which suggests fragility.
- Compare against the baseline from step 3 — "beats a coin flip" is not the bar; "beats the simple baseline after costs" is.
- If a strategy looks unusually good, actively look for the likely bug (lookahead bias, survivorship bias, data leakage) before accepting it at face value.

## How to communicate results

Present findings as: the hypothesis tested, the methodology used, the result, and the specific threats to validity that remain — not just a headline number. When a strategy fails validation, explain which specific assumption broke it, so the user can iterate rather than discard the whole idea.
