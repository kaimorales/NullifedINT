# Nullified Interceptions Analysis
![image](https://github.com/kaimorales/NullifedINT/blob/main/mohomie.png)
## Overview
This project analyzes nullified interceptions (interceptions negated by penalties) in the NFL from 2018 to 2023. The goal is to determine whether certain quarterbacks, particularly Patrick Mahomes, have a statistically significant number of nullified interceptions compared to their peers.

## Data Collection
Data was obtained using the `nflfastR` package in R, which provides play-by-play data for all NFL games. The R script:
- Extracts play-by-play data for seasons 2018–2023.
- Identifies nullified interceptions by searching for relevant play descriptions.
- Matches interceptions with starting quarterbacks when necessary.
- Merges pass attempt data to normalize interception rates.
- Outputs a cleaned dataset as `nullified_interceptions_with_attempts_2018_2023.csv`.

## Analysis
The dataset was analyzed using Python to identify statistical outliers and differences in nullified interception rates among quarterbacks. The analysis includes:
- **Mann-Whitney U Test**: Checks if Mahomes' nullified interception rate is statistically different from other quarterbacks.
- **Bootstrapping**: Estimates confidence intervals for nullified interception rates to determine if Mahomes is an outlier.
- **Visualization**: A histogram compares Mahomes’ nullified interception rate against other quarterbacks.

## Results
- Patrick Mahomes was identified as an outlier in nullified interceptions.
- Statistical tests were used to determine if Mahomes' rate significantly deviates from the league average.
- The results provide insights into how often Mahomes benefits from nullified interceptions compared to other QBs.

## Project Structure
- `get_nullified_interceptions.R` – Collects and processes NFL play-by-play data.
- `analyze_nullified_interceptions.py` – Performs statistical analysis on the dataset.
- `nullified_interceptions_with_attempts_2018_2023.csv` – Processed dataset used for analysis.

## Requirements
### R Dependencies:
- `nflfastR`
- `tidyverse`

### Python Dependencies:
- `pandas`
- `numpy`
- `scipy`
- `matplotlib`

## Usage
1. Run `get_nullified_interceptions.R` in R to generate the dataset.
2. Run `analyze_nullified_interceptions.py` in Python to analyze the data and visualize results.

## Future Improvements
- Expanding analysis to include the impact of nullified interceptions on game outcomes.
- Comparing nullified interception rates across different eras of the NFL.
- Refining methods to distinguish intentional penalties vs. incidental fouls leading to nullified interceptions.

