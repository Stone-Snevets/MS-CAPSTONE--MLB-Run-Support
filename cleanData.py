"""
File to clean MLB Run-Support data

Author: Solomon Stevens
Date: July 14, 2024

"""

# ===== Preliminary Stuff =====================================================
# Imports
import pandas as pd

# Constants
CORRELATION_THRESHOLD:float = 0.05

# Read in the data
df = pd.read_csv('stats.csv')

# ===== Cleaning ==============================================================
# Remove player_id
df = df.drop(columns='player_id')

# Create the win/loss percentage column
# Link: https://datagy.io/pandas-conditional-column/
df['win_loss_pct'] = df.p_win/df.p_loss
df.loc[df['p_loss']==0, 'win_loss_pct'] = df['p_win']

# Calculate the average ERA
avg_ERA = (df.mean(axis=0, numeric_only=True)).iloc[14] # = 4.055635635635635

# Calculate the average win/loss percentage
avg_win_loss_pct = (df.mean(axis=0, numeric_only=True)).iloc[-1] # = 1.3655418654171663

# Create lack-of-run-support column
#-> Better (lower) ERA than average, but also a lower winning percentage than average
low_win_pct = df.win_loss_pct.apply(lambda x: True if x < avg_win_loss_pct else False)
low_era = df.p_era.apply(lambda x: True if x < avg_ERA else False)

df['lack_of_run_support'] = low_win_pct & low_era


# Calculate the correlation between each numeric column and the lack-of-run-support column
#-> Remove columns with hardly any correlation (positive or negative)
for i in range((len(df.columns)-2), 1, -1):
    # Calculate the correlation between the statistic and run-support column
    correlation = df.lack_of_run_support.corr(df.iloc[:,i])

    #print(i, df.columns[i], correlation)

    # If the correlation is closer to zero than our given number, get rid of the column
    if (correlation < CORRELATION_THRESHOLD and correlation > -CORRELATION_THRESHOLD):
        df = df.drop(columns=df.columns[i])


# Print the data set
#with pd.option_context('display.max_rows', None,
#                       'display.max_columns', None,
#                        ):
#    print('Win%:', low_win_pct, "ERA:",low_era, "Support:",df.lack_of_run_support)


# Write to a file
df.to_csv('stats_cleaned.csv')