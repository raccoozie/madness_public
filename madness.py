"""
This module provides a convenient way to use the JSON encoding and decoding functions in Python.

Usage:
    import json

The module exposes the following functions:
    - json.dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True,
        - cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)
    - json.dump(obj, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True,
        - cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)
    - json.loads(s, *, cls=None, object_hook=None, parse_float=None, parse_int=None,
        - parse_constant=None, object_pairs_hook=None, **kw)
    - json.load(fp, *, cls=None, object_hook=None, parse_float=None, parse_int=None,
        - parse_constant=None, object_pairs_hook=None, **kw)
"""
import json
import random
from datetime import datetime

# TODO: format the output nicely


def simulate_game(low_score_bound, high_score_bound):
    """
    Simulates a game between two teams and returns the scores.

    Parameters:
    None

    Returns:
    A tuple containing two integers: the scores of the two teams.

    Raises:
    None
    """
    team1_score = 0
    team2_score = 0
    while team1_score == team2_score:
        team1_score = random.randint(low_score_bound, high_score_bound)
        team2_score = random.randint(low_score_bound, high_score_bound)

    return (team1_score, team2_score)


def simulate_tournament(teams, matchups, low_score_bound=50, high_score_bound=98):
    """
    Function to simulate a single elimination tournament

    Parameters:
    None

    Returns:
    The champ

    Raises:
    None
    """

    # Initialize the bracket with the matchups
    bracket = [(matchup["team1_rank"], matchup["team2_rank"])
               for matchup in matchups]

    # Simulate each round of the tournament
    for _ in range(len(bracket)):
        new_bracket = []
        new_team1 = ''
        new_team2 = ''
        team_count = 0

        if bracket[0][1] is None:
            # The final team left in the bracket is the champion
            return [team for team in teams if team.get('rank') == bracket[0][0]]

        for matchup in bracket:

            team1, team2 = matchup
            team1_score, team2_score = simulate_game(
                low_score_bound, high_score_bound)
            # The team with the higher score advances to the next round
            if team1_score > team2_score:

                if team_count == 0:
                    new_team1 = team1
                else:
                    new_team2 = team1

                winner = [
                    ([team for team in teams if team.get('rank')
                      == team1][0].get('name'), team1_score)]
                loser = [
                    ([team for team in teams if team.get('rank')
                      == team2][0].get('name'), team2_score)]
            else:

                if team_count == 0:
                    new_team1 = team2
                else:
                    new_team2 = team2

                winner = [
                    ([team for team in teams if team.get('rank')
                      == team2][0].get('name'), team2_score)]
                loser = [
                    ([team for team in teams if team.get('rank')
                      == team1][0].get('name'), team1_score)]

            team_count += 1

            if len(bracket) == 1:
                # final round
                new_bracket.append((new_team1, None))
            elif team_count > 1:
                # if we have the two teams that we need then set the matchup
                new_bracket.append((new_team1, new_team2))
                team_count = 0

            print(winner[0][0] + " defeats " + loser[0][0] + " with a score of "
                  + str(winner[0][1]) + " to " + str(loser[0][1]))
        bracket = new_bracket
    return [team for team in teams if team.get('rank') == bracket[0][0]]


current_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
print("Madness Model started at " + str(current_date) + "\n")

# Load 16 team bracket matchups
with open("datasets/matchups.json", 'r', encoding='utf-8') as f:
    matchup_data = json.load(f)

# South Region
# Load teams and matchups from JSON file
with open("datasets/south_region.json", 'r', encoding='utf-8') as f:
    south_data = json.load(f)

# Simulate the tournament and print the results
south_champ = simulate_tournament(
    south_data["teams"], matchup_data["matchups"])
print("\nThe south region champion is:", south_champ[0].get('name'))
print("\n")

# East Region
# Load teams and matchups from JSON file
with open("datasets/east_region.json", 'r', encoding='utf-8') as f:
    east_data = json.load(f)

# Simulate the tournament and print the results
east_champ = simulate_tournament(east_data["teams"], matchup_data["matchups"])
print("\nThe east region champion is: " + east_champ[0].get('name') + "\n")

# West Region
# Load teams and matchups from JSON file
with open("datasets/west_region.json", 'r', encoding='utf-8') as f:
    west_data = json.load(f)

# Simulate the tournament and print the results
west_champ = simulate_tournament(west_data["teams"], matchup_data["matchups"])
print("\nThe west region champion is: " + west_champ[0].get('name') + "\n")

# Midwest Region
# Load teams and matchups from JSON file
with open("datasets/midwest_region.json", 'r', encoding='utf-8') as f:
    midwest_data = json.load(f)

# Simulate the tournament and print the results
midwest_champ = simulate_tournament(
    midwest_data["teams"], matchup_data["matchups"])
print("\nThe midwest region champion is: " +
      midwest_champ[0].get('name') + "\n")

# south-east semifinals
# regional ranks are not unique
south_champ[0]["rank"] = south_champ[0]["seed"]
east_champ[0]["rank"] = east_champ[0]["seed"]
semi_final_matchup = [{'matchup_id': 1, 'team1_rank': south_champ[0].get(
    'seed'), 'team2_rank': east_champ[0].get('seed')}]

south_east_champ = simulate_tournament(
    south_champ + east_champ, semi_final_matchup, 41, 87)

print("\nThe south-east region champion is: " +
      south_east_champ[0].get('name') + "\n")

# midwest-west semifinals
# regional ranks are not unique
midwest_champ[0]["rank"] = midwest_champ[0]["seed"]
west_champ[0]["rank"] = west_champ[0]["seed"]
semi_final_matchup = [{'matchup_id': 1, 'team1_rank': midwest_champ[0].get(
    'seed'), 'team2_rank': west_champ[0].get('seed')}]

midwest_west_champ = simulate_tournament(
    midwest_champ + west_champ, semi_final_matchup, 41, 87)

print("\nThe midwest-west region champion is: " +
      midwest_west_champ[0].get('name') + "\n")

# championship
# regional ranks are not unique
south_east_champ[0]["rank"] = south_east_champ[0]["seed"]
midwest_west_champ[0]["rank"] = midwest_west_champ[0]["seed"]
championship_matchup = [{'matchup_id': 1, 'team1_rank': south_east_champ[0].get(
    'seed'), 'team2_rank': midwest_west_champ[0].get('seed')}]

final_champ = simulate_tournament(
    south_east_champ + midwest_west_champ, championship_matchup, 41, 87)

print("\nThe final champion is: " +
      final_champ[0].get('name'))
