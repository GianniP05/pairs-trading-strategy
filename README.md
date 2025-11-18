# pairs-trading-strategy
📘 Pairs Trading Strategy — QuantConnect Competition

This repository contains the full research, implementation, and documentation of a market-neutral pairs trading strategy built for the QuantConnect competition.
It combines classical statistical arbitrage techniques with modern engineering practices.

🔍 Overview

Pairs trading is a mean-reversion strategy that exploits temporary mispricings between two historically related assets.
This project focuses on:

Identifying cointegrated pairs

Estimating hedge ratios (OLS, with Kalman Filter planned)

Constructing a stationary spread

Generating trading signals using Z-scores

Executing a market-neutral long/short portfolio

Backtesting inside QuantConnect’s LEAN engine

📂 Project Structure
pairs-trading-strategy/
│
├── notebooks/                # Research notebooks (cointegration tests, Z-scores, plots)
├── src/                      # LEAN algorithm code
│     ├── main.py             # Core QCAlgorithm implementation
│     ├── pairs_alpha.py      # Signal logic / alpha model
│     └── utils.py            # Helper functions (hedge ratio, rolling regression, etc.)
├── results/                  # Backtest results, plots, metrics
├── docs/                     # Documentation of methodology, notes, enhancements
│
├── .gitignore
└── README.md

🧠 Strategy Logic
1. Pair Selection

Pairs are chosen based on:

Strong historical correlation

Cointegration (Engle–Granger / ADF tests)

Economic similarity (e.g., KO–PEP, XOM–CVX)

2. Hedge Ratio

Calculated via:

Ordinary Least Squares (OLS)

Kalman Filter hedge ratio (coming soon)

3. Spread Construction

St​=Xt​−βYt​

4. Signal Generation

Use Z-score of spread:

Long spread (long X, short Y) when Z < –2

Short spread (short X, long Y) when Z > 2

Close positions when |Z| < 0.5

5. Execution

Equal-dollar long/short exposure

Market-neutral

Daily resolution

Risk controls (stop-loss, max holding time) planned