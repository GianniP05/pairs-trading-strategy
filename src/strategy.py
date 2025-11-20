import pandas as pd

def strategy(z_scores, betas, spreads, entry_threshold = 2, exit_threshold = 0.5, stop_loss = 4):
    """
    Generate a long/short/flat position series for a pairs trading strategy 
    based solely on z-score threshold rules.

    This function implements a simple state-machine logic:
    - Position is carried forward from the previous timestep.
    - A trade is opened only when the system is flat.
    - A trade is closed only when an exit or stop-loss condition is triggered.

    Parameters
    ----------
    z_scores : pd.Series
        Time series of z-scores for the spread between two assets.
        The direction of the position is determined by the sign and size of z.

    betas : pd.Series or float
        Hedge ratio series (dynamic or static). Not used directly in this simple 
        strategy version, but included for interface compatibility with future extensions.

    spreads : pd.Series
        Spread series (x - beta*y). Not used in this simple strategy version, but 
        included for extensibility (e.g., future spread-based exits).

    entry_threshold : float, default=2
        Enter a position when |z| exceeds this level.
        z > entry_threshold  → enter short spread
        z < -entry_threshold → enter long spread

    exit_threshold : float, default=0.5
        Exit a position when |z| falls back below this level (mean reversion).

    stop_loss : float, default=4
        Emergency exit if the spread diverges too far in either direction.

    Returns
    -------
    positions : pd.Series
        Time series of integer positions:
        +1 : long spread
        -1 : short spread
         0 : flat position

        The series maintains the same index as `z_scores`.
    """

    T = len(z_scores)
    positions = pd.Series(0, index=z_scores.index)

    for t in range(1, T):

        # 1. Carry forward previous position since the position stays the same unless something triggers the change
        positions.iloc[t] = positions.iloc[t-1]

        z = z_scores.iloc[t]

        # 2. If flat, check entry signals
        if positions.iloc[t] == 0:
            if z > entry_threshold:
                positions.iloc[t] = -1    # short spread
            elif z < -entry_threshold:
                positions.iloc[t] = 1     # long spread

        # 3. If in a trade, check exit conditions
        else:
            # Mean reversion exit
            if abs(z) < exit_threshold:
                positions.iloc[t] = 0

            # Stop-loss exit
            elif abs(z) > stop_loss:
                positions.iloc[t] = 0

    return positions

