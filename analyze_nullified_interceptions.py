# Re-load the dataset after execution state reset
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Reload the file
file_path = "/mnt/data/nullified_interceptions_with_attempts_2018_2023.csv"
df = pd.read_csv(file_path)

# Ensure the data has relevant columns
required_columns = {"passer_player_name", "nullified_interceptions", "pass_attempts"}
if not required_columns.issubset(df.columns):
    missing_columns = required_columns - set(df.columns)
    raise ValueError(f"Missing required columns: {missing_columns}")

# Drop missing values
df = df.dropna(subset=["passer_player_name", "nullified_interceptions", "pass_attempts"])

# Calculate nullified INT rate (nullified INTs per pass attempt)
df["nullified_int_rate"] = df["nullified_interceptions"] / df["pass_attempts"]

# Separate Mahomes' data
mahomes_rate = df[df["passer_player_name"] == "P.Mahomes"]["nullified_int_rate"].values
other_qbs_rate = df[df["passer_player_name"] != "P.Mahomes"]["nullified_int_rate"].values

# Perform Mann-Whitney U test (to check if Mahomes is statistically different)
if len(mahomes_rate) > 0 and len(other_qbs_rate) > 0:
    u_stat, p_value = stats.mannwhitneyu(mahomes_rate, other_qbs_rate, alternative="two-sided")
else:
    u_stat, p_value = np.nan, np.nan

# Bootstrapping to estimate confidence interval
bootstrap_samples = 10000
if len(other_qbs_rate) > 0:
    bootstrap_means = np.random.choice(other_qbs_rate, size=(bootstrap_samples, len(mahomes_rate)), replace=True).mean(axis=1)
    ci_95 = np.percentile(bootstrap_means, [2.5, 97.5])
else:
    bootstrap_means, ci_95 = np.array([]), [np.nan, np.nan]

# Visualization
plt.hist(bootstrap_means, bins=30, alpha=0.7, color='blue', label="Bootstrapped QB INT Means")
if len(mahomes_rate) > 0:
    plt.axvline(mahomes_rate.mean(), color='red', linestyle='dashed', linewidth=2, label="Mahomes' INT Rate")
plt.axvline(ci_95[1], color='green', linestyle='dashed', linewidth=2, label="95% Upper Bound")
plt.xlabel("Nullified INT Rate")
plt.ylabel("Frequency")
plt.legend()
plt.title("Bootstrapping Nullified INT Rate: Mahomes vs. Other QBs")
plt.show()

# Print results
results = {
    "U-Statistic": u_stat,
    "P-Value": p_value,
    "95% Confidence Interval": ci_95,
    "Mahomes' Nullified INT Rate": mahomes_rate.mean() if len(mahomes_rate) > 0 else np.nan
}

results
