# Load required packages
library(nflfastR)
library(tidyverse)

# Define years to analyze
years <- 2018:2023

# Load play-by-play (PBP) data
pbp_data <- map_df(years, load_pbp)

# Identify the starting QB for each team in each game
starting_qbs <- pbp_data %>%
  filter(!is.na(passer_player_name)) %>%
  group_by(game_id, posteam) %>%
  summarise(starting_qb = first(passer_player_name), .groups = "drop")

# Collect **nullified interceptions** (interceptions negated by penalties)
nullified_ints <- pbp_data %>%
  filter(str_detect(desc, "INTERCEPTED"), penalty == 1) %>%
  select(season, game_id, week, posteam, defteam, passer_player_name, desc, penalty_team, penalty_type)

# Join with starting QB data to fill in missing QB names
nullified_ints_fixed <- nullified_ints %>%
  left_join(starting_qbs, by = c("game_id", "posteam")) %>%
  mutate(passer_player_name = coalesce(passer_player_name, starting_qb)) %>%
  select(-starting_qb)

# Collect **total pass attempts** per QB over the same period
pass_attempts <- pbp_data %>%
  filter(pass_attempt == 1) %>% # Filter only passing plays
  group_by(season, passer_player_name) %>%
  summarise(pass_attempts = n(), .groups = "drop")

# Merge **nullified interceptions** with **pass attempts**
final_data <- nullified_ints_fixed %>%
  group_by(season, passer_player_name) %>%
  summarise(nullified_interceptions = n(), .groups = "drop") %>%
  left_join(pass_attempts, by = c("season", "passer_player_name")) %>%
  mutate(nullified_int_rate = nullified_interceptions / pass_attempts) %>% # Calculate rate
  arrange(desc(nullified_int_rate)) # Sort by highest nullified INT rate

# Save cleaned dataset
write_csv(final_data, "nullified_interceptions_with_attempts_2018_2023.csv")
write_csv(final_data, "~/Desktop/nullified_interceptions_with_attempts_2018_2023.csv")

# Print confirmation
print("CSV file saved: nullified_interceptions_with_attempts_2018_2023.csv")
