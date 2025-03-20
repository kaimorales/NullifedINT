## Project Structure
# - get_nullified_interceptions.R  -> Pulls NFL data using R
# - analyze_nullified_interceptions.py -> Analyzes the data in Python
# - nullified_interceptions_with_attempts_2018_2023.csv -> Data file

# R script: get_nullified_interceptions.R
library(nflfastR)
library(tidyverse)

# Define years we want to analyze
years <- 2018:2023

# Load play-by-play (PBP) data
pbp_data <- map_df(years, load_pbp)

# Identify the starting QB for each team in each game
starting_qbs <- pbp_data %>%
  filter(!is.na(passer_player_name)) %>%
  group_by(game_id, posteam) %>%
  summarise(starting_qb = first(passer_player_name), .groups = "drop")

# Calculate pass attempts per QB per season
pass_attempts <- pbp_data %>%
  filter(!is.na(passer_player_name)) %>%
  group_by(season, passer_player_name) %>%
  summarise(pass_attempts = n(), .groups = "drop")

# Filter for Nullified Interceptions (INTs negated by penalties)
nullified_ints <- pbp_data %>%
  filter(str_detect(desc, "INTERCEPTED"), penalty == 1) %>% 
  select(season, game_id, week, posteam, defteam, passer_player_name, desc, penalty_team, penalty_type)

# Join with the starting QB data to fill in missing values
nullified_ints_fixed <- nullified_ints %>%
  left_join(starting_qbs, by = c("game_id", "posteam")) %>%
  mutate(passer_player_name = coalesce(passer_player_name, starting_qb)) %>%
  select(-starting_qb)

# Join with pass attempts data
nullified_ints_fixed <- nullified_ints_fixed %>%
  left_join(pass_attempts, by = c("season", "passer_player_name"))

# Save the cleaned data to a CSV file
write_csv(nullified_ints_fixed, "nullified_interceptions_with_attempts_2018_2023.csv")
print("CSV file saved: nullified_interceptions_with_attempts_2018_2023.csv")
