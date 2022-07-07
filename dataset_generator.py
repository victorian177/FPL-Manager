import numpy as np
import pandas as pd

from player_data import PlayerData


def column_creator(df: pd.DataFrame, expression: str):
    """
    Creates columns based on formula specified

    df: pandas dataframe(PlayerData player_stats)
    expression: str(expects the format 'name_of_new_column = existing column op existing columns ...')
        - op could be any of the four basic arithmetic operations: + - / *

    NB:- PEMDAS or BODMAS is not followed, rather the equation is solved from left to right
    """

    # Splitting of expression into its constituent components
    column_name, formula = expression.split(" = ")
    formula = formula.split(' ')
    df[column_name] = df[formula[0]]
    is_operation = True
    operation = ''

    # Loop through formula and perform operations
    for string in formula[1:]:
        if is_operation:
            operation = string

        else:
            if operation == '+':
                df[column_name] += df[string]

            elif operation == '-':
                df[column_name] -= df[string]

            elif operation == '/':
                df[column_name] /= df[string]

            elif operation == '*':
                df[column_name] *= df[string]

        is_operation = not is_operation

    # Replaces NaN, inf with 0
    df[column_name].replace([np.nan, np.inf], 0, inplace=True)


# Dataset columns
columns = {'player_stats': [
    # Player stats
    'appearances',
    'age',
    'place',
    'value',
    'value_change',
    'minutes_per_goal',
    'minutes_per_assist',
    'goals_xg_diff',
    'assists_xa_diff',
    'minutes_per_sca',
    'minutes_per_gca',
    'goals_to_shot_ratio',
    'target_to_shot_ratio',
    'dribbles_per_app',
    'blocks_per_app',
    'clearances_per_app',
    'errors_per_app',
    'points_per_app',
    'tackles_pct',
    'interceptions_per_app',
    'touches_per_app',
    'minutes_per_cross',
    'minutes_per_fouled',
    'minutes_per_foul',
    'minutes_per_offside',
    'ball_recoveries_per_app',
    'through_pass_ratio',
    'dist_per_carry',
    'prog_dist_per_carry',
    'prog_to_total_ratio',
    'sub_outs_per_start',
    'sub_ins_per_app',
    'minutes_per_yellow',
    'fouls_per_yellow',
    'miscontrols_per_app',
    'dispossessed_per_app',
    'played_60_per_app',
    'oob_per_pass',
    'intercepted_per_pass',
    'blocked_per_pass',
    'prog_per_pass_recieved',
    'bonus_per_app',
    'transfers_ratio',
    'carries_into_final_third_pct',
    'carries_into_pen_area_pct',
    'touches_att_pen_area_pct',
    'touches_att_3rd_pct',
    'touches_mid_3rd_pct',
    'touches_def_3rd_pct',
    'touches_def_pen_area_pct',
    'influence',
    'creativity',
    'threat'],

    # Team stats
    'teams_stats': [
    'xG',
    'pts_per_game',
    'home_pts_ratio',
    'away_pts_ratio',
    'wins_ratio',
    'draws_ratio',
    'losses_ratio',
    'cleansheets_ratio',
    'h_cleansheets_ratio',
    'a_cleansheets_ratio',
    'goal_ratio',
    'home_goal_ratio',
    'away_goal_ratio',
    'home_win_ratio',
    'away_win_ratio',
    'home_draw_ratio',
    'away_draw_ratio',
    'home_loss_ratio',
    'away_loss_ratio',
    'pct_possession',
    'team_position']
}

# Extra player related stats
extra_player_columns = [
    'minutes_per_goal = minutes / goals',
    'minutes_per_assist = minutes / assists',
    'goals_xg_diff = goals - xg',
    'assists_xa_diff = assists - xa',
    'minutes_per_sca = minutes / sca',
    'minutes_per_gca = minutes / gca',
    'goals_to_shot_ratio = goals / shots_total',
    'target_to_shot_ratio = shots_on_target / shots_total',
    'dribbles_per_app = dribbles / appearances',
    'blocks_per_app = blocks / appearances',
    'clearances_per_app = clearances / appearances',
    'errors_per_app = errors / appearances',
    'points_per_app = total_points / appearances',
    'tackles_pct = tackles_won / tackles',
    'interceptions_per_app = interceptions / appearances',
    'touches_per_app = touches / appearances',
    'minutes_per_cross = minutes / crosses',
    'minutes_per_fouled = minutes / fouled',
    'minutes_per_foul = minutes / fouls',
    'minutes_per_offside = minutes / offsides',
    'ball_recoveries_per_app = ball_recoveries / appearances',
    'through_pass_ratio = through_balls / passes',
    'dist_per_carry = carry_distance / carries',
    'prog_dist_per_carry = carry_progressive_distance / progressive_carries',
    'prog_to_total_ratio = passes_progressive_distance / passes_total_distance',
    'sub_outs_per_start = sub_outs / starts',
    'sub_ins_per_app = sub_ins / appearances',
    'minutes_per_yellow = cards_yellow / minutes',
    'fouls_per_yellow = fouls / cards_yellow',
    'miscontrols_per_app = miscontrols / appearances',
    'dispossessed_per_app = dispossessed / appearances',
    'played_60_per_app = played_60 / appearances',
    'oob_per_pass = passes_oob / passes',
    'intercepted_per_pass = passes_intercepted / passes',
    'blocked_per_pass = passes_blocked / passes',
    'prog_per_pass_recieved = progressive_passes_received / passes_received',
    'bonus_per_app = bonus / appearances',
    'transfers_ratio = transfers_in / transfers_out',

    'carries_into_final_third_pct = carries_into_final_third / carries',
    'carries_into_pen_area_pct = carries_into_penalty_area / carries',

    'passes_pct_short = passes_completed_short / passes_short',
    'passes_pct_long = passes_completed_long / passes_long',
    'passes_pct_medium = passes_completed_medium / passes_medium',

    'touches_att_pen_area_pct = touches_att_pen_area / touches',
    'touches_att_3rd_pct = touches_att_3rd / touches',
    'touches_mid_3rd_pct = touches_mid_3rd / touches',
    'touches_def_3rd_pct = touches_def_3rd / touches',
    'touches_def_pen_area_pct = touches_def_pen_area / touches'
]

# Extra team related columns
extra_team_columns = [
    'pts_per_game = pts / matches_played',
    'cleansheets_ratio = cleansheets / matches_played',
    'home_pts_ratio = home_pts / pts',
    'away_pts_ratio = away_pts / pts',
    'wins_ratio = wins / matches_played',
    'draws_ratio = draws / matches_played',
    'losses_ratio = losses / matches_played',
    'h_cleansheets_ratio = home_cleansheets / cleansheets',
    'a_cleansheets_ratio = away_cleansheets / cleansheets',
    'pct_possession = pct_possession / matches_played',
    'goal_ratio = goals_for / goals_against',
    'home_goal_ratio = home_goals_for / home_goals_against',
    'away_goal_ratio = away_goals_for / away_goals_against',
    'home_win_ratio = home_wins / wins',
    'away_win_ratio = away_wins / wins',
    'home_draw_ratio = home_draws / draws',
    'away_draw_ratio = away_draws / draws',
    'home_loss_ratio = home_losses / losses',
    'away_loss_ratio = away_losses / losses'
]

# Outcomes being predicted for
outfield_outcomes = [
    'APPS', 'STARTS', 'PLAYED_60+',
    'GOALS', 'ASSISTS',
    'CLEANSHEETS', 'CONCEDED_2_GOALS+'
]

goalkeep_outcomes = [
    'CLEANSHEETS', 'THREE_SAVES+', 'PENALTY_SAVES'
]

discipline_outcomes = [
    'YELLOW_CARDS',
    'RED_CARDS'
]


def dataset_generator(gameweek_range, threshold, target):
    """
    Generates a dataset having X having columns specified in 'Dataset columns' and y having columns specified in 'Outcomes'

    :param 
        gameweek_range: int | list -> matches with gameweek(s) to be considered
        threshold: int -> any player with minutes less than threshold is dropped
        target: int -> specifies number of matches over which we are predicting

    Dataset is stored in a .csv file from the pandas DataFrame
    """

    # Seasons is set from 17/18 to 20/21, 21/22 is left for simulation
    seasons = [f'{i}/{i + 1}' for i in range(17, 21)]

    # Initialisiton of PlayerData classes
    all_data = {season: PlayerData(
        int(season.split('/')[0])) for season in seasons}

    # Column names specified in 'headers' attribute from PlayerData class
    categories = all_data[seasons[0]].headers['header']
    headers = [value for value in categories.values()]
    headers += ['transfers_balance', 'creativity', 'transfers_in', 'sub_ins', 'ict_index', 'sub_outs', 'played_60', 'bonus',
                'appearances', 'total_points', 'transfers_out', 'bps', 'starts', 'threat', 'influence', 'value', 'value_change']

    # team names specified in 'players' attribure from PlayerData class
    teams = {key: sorted(value.players.keys())
             for key, value in all_data.items()}

    # Generating X part of dataset

    # Dataset containing DFs from PlayerData 'data_lister' method
    X_prep = {key: value.data_lister(gameweek_range=gameweek_range)
              for key, value in all_data.items()}

    # Appending of extra columns from 'player related' columns
    for season in seasons:
        for team in teams[season]:
            for exprssn in extra_player_columns:
                column_creator(df=X_prep[season][team]
                               ['player_stats'], expression=exprssn)

    # Appending of extra columns from 'team related' columns
    for season in seasons:
        for exprssn in extra_team_columns:
            column_creator(df=X_prep[season]
                           ['teams_stats'], expression=exprssn)

    # Find which position most represents the player i.e. position with the most frequency. If tie, pick position that occurs first
    for season in seasons:
        for team in teams[season]:
            positions = X_prep[season][team]['player_stats']['position']
            places = []
            for p in positions:
                keys = list(p.keys())
                values = list(p.values())
                if len(values) > 0:
                    mx = max(values)
                    ind = values.index(mx)

                    top_pstn = keys[ind]
                    if top_pstn[-1] == 'K':
                        places.append('Gkp')
                    elif top_pstn[-1] == 'B':
                        places.append('Def')
                    elif top_pstn[-1] == 'M':
                        places.append('Mid')
                    else:
                        places.append('Fwd')
                else:
                    places.append("Nil")

            X_prep[season][team]['player_stats']['place'] = places

            # Get age of player from age column
            ages = X_prep[season][team]['player_stats']['age']
            ages = [int(age.split('-')[0]) if age != 0 else 0 for age in ages]
            X_prep[season][team]['player_stats']['age'] = ages

    # Filtering of player_stats, given players have been filtered by threshold
    filtered_players = {}
    for season in seasons:
        filtered_players[season] = {}
        for team in teams[season]:
            filtr = (X_prep[season][team]['player_stats']
                     ["minutes"] >= threshold)
            X_prep[season][team]['player_stats'] = X_prep[season][team]['player_stats'][filtr]
            X_prep[season][team]['player_stats'].reset_index(
                inplace=True, drop=True)
            filtered_players[season][team] = list(
                X_prep[season][team]['player_stats']['player'])

    # Sort teams based on points gathered over the course of games to get position of club
    for season in seasons:
        teams_positions = X_prep[season]['teams_stats'].sort_values(by='pts')
        teams_positions.reset_index(inplace=True, drop=True)
        X_prep[season]['teams_stats']['team_position'] = teams_positions.index
        X_prep[season]['teams_stats']['team_position'] += 1

    cols = ['player'] + columns['player_stats']

    X = {}
    for season in seasons:
        t_stats = X_prep[season]['teams_stats']
        X[season] = {}

        # Append team stats to their corresponding players
        for team in teams[season]:
            t_col_stats = t_stats[t_stats['team_name']
                                  == team][columns['teams_stats']]
            num_of_plyrs = len(filtered_players[season][team])
            t_col_stats = t_col_stats.loc[t_col_stats.index.repeat(
                num_of_plyrs)]
            t_col_stats.reset_index(inplace=True, drop=True)

            # Combine all data into one DataFrame
            X[season][team] = pd.concat(
                [X_prep[season][team]["player_stats"][cols], t_col_stats], axis=1)

    # Generating y part of dataset

    # Dataset containing DFs from PlayerData 'data_lister' method
    y_prep = {key: value.data_lister(gameweek_range=[gameweek_range[1], gameweek_range[1]+target])
              for key, value in all_data.items()}

    y = {}
    for season in seasons:
        y[season] = {}
        for team in teams[season]:
            y[season][team] = pd.DataFrame(
                filtered_players[season][team], columns=["player"])
            y[season][team] = y[season][team].reindex(
                columns=["player"]+outfield_outcomes+discipline_outcomes, fill_value=0)  # initialisation of outcomes to 0

    # 'GOALS', 'ASSISTS', 'APPS', 'PLAYED_60+', 'STARTS', 'YELLOW_CARDS', 'RED_CARDS', 'CONCEDED_2_GOALS+', 'CLEANSHEETS'

    # Setting of outcomes
    for season in seasons:
        for team in teams[season]:
            fltr = (y_prep[season]['played_fixtures']['squad_a'] == team) | (
                y_prep[season]['played_fixtures']['squad_b'] == team)  # Filter for home and away matches
            played_fixtures = y_prep[season]['played_fixtures'][fltr].reset_index(
            )

            # Record how many times a team conceded two or more goals
            conceded_2 = 0
            for row in range(len(played_fixtures)):
                score = played_fixtures.loc[row]['score'].split('–')
                if played_fixtures.loc[row]['squad_a'] == team:
                    conceded_2 = conceded_2 + \
                        1 if int(score[1]) >= 2 else conceded_2
                else:
                    conceded_2 = conceded_2 + \
                        1 if int(score[0]) >= 2 else conceded_2

            # Record how cleansheets a team accumulated
            cleansheets = y_prep['teams_stats'][y_prep['teams_stats']
                                                ['team'] == team]['cleansheets'].values[0]

            # Loop through filtered players and record all the outcomes specified
            for player in filtered_players[season][team]:
                stats = y_prep[season][team]['player_stats'].copy()
                row = stats[stats['player'] == player]

                if not row.empty:
                    idx = y[season][team].loc[y[season]
                                              [team]['player'] == player].index[0]

                    y[season][team].loc[idx, 'GOALS'] += int(row['goals'])
                    y[season][team].loc[idx, 'APPS'] += int(row['appearances'])
                    y[season][team].loc[idx, 'STARTS'] += int(row['starts'])
                    y[season][team].loc[idx, 'ASSISTS'] += int(row['assists'])
                    y[season][team].loc[idx,
                                        'YELLOW_CARDS'] += int(row['cards_yellow'])
                    y[season][team].loc[idx,
                                        'RED_CARDS'] += int(row['cards_red'])
                    if int(row['minutes']) > 60:
                        y[season][team].loc[idx, 'PLAYED_60+'] += 1
                    y[season][team].loc[idx, 'CONCEDED_2_GOALS+'] += conceded_2
                    y[season][team].loc[idx, 'CLEANSHEETS'] += cleansheets

    # Joining of X, y parts of datasets
    datasets_prep = {}
    for season in seasons:
        datasets_prep[season] = {}
        for team in teams[season]:
            datasets_prep[season][team] = pd.concat(
                [X[season][team], y[season][team][outfield_outcomes+discipline_outcomes]], axis=1)

    # Concatenating of all datasets to form one dataset
    datasets = []
    for season in seasons:
        for team in teams[season]:
            datasets.append(datasets_prep[season][team])

    # Concatenate and save dataset in .csv file
    df = pd.concat(datasets, ignore_index=True)
    df.to_csv(
        f'datasets/dataset_{gameweek_range[0]}_to_{gameweek_range[1]}_{target}.csv', index=False)
