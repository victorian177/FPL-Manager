import json

import numpy as np
import pandas as pd


class PlayerData:
    def __init__(self, season):
        if season not in range(17, 22):
            raise Exception(
                "'season' expects value between 17 and 21 inclusive(2017/18 to 2021/22)")
        else:
            self.season = season
        self.fixtures = self.fixtures_lister()  # fixtures corresponding to season
        # headers corresponding to season, headers contain column names
        self.headers = self.headers_lister()
        self.players = self.players_lister()  # players corresponding to season

    def fixtures_lister(self):
        """Read fixtures file for season"""
        fixture_df = pd.read_csv(
            f"data/Premier League/scores and fixtures/20{self.season}-20{self.season + 1} PL Scores & Fixtures.csv")
        fixture_df["date"] = pd.to_datetime(fixture_df["date"])

        return fixture_df

    def headers_lister(self):
        """Read header files for season"""
        header_dctnry = {}  # Dictonary to store all header values

        # Header for outfield player stats
        with open("data/Premier League/header information/headers.json") as hdr:
            header = json.load(hdr)

        # Header for goalkeeper stats
        with open("data/Premier League/header information/gk_headers.json") as gk_hdr:
            gk_header = json.load(gk_hdr)
        gk_header = gk_header["List"]

        # Header for shot related stats
        with open("data/Premier League/header information/sh_headers.json") as sh_hdr:
            sh_header = json.load(sh_hdr)
        sh_header = sh_header["List"]

        header_dctnry["header"] = header
        header_dctnry["gk_header"] = gk_header
        header_dctnry["sh_header"] = sh_header

        return header_dctnry

    def players_lister(self):
        """Read players file for season"""
        with open(f"data/Premier League/player information/20{self.season}-20{self.season + 1} player_info.json", encoding="utf-8") as players_with_team:
            plyrs_dctnry = json.load(players_with_team)

        return plyrs_dctnry

    def data_lister(self, **options):
        """
            Uses the filters specified in **options to collate data pertaining player stats, goalkeeper stats and team stats.
            No options does for all played matches in the specified season.

            :param **options
                String-based inputs -> expects a valid team name
                    home: str(team name) | list -> matches in which the team(s) is/are home
                    away: str(team name) | list -> matches in which the team(s) is/are away
                    team: str(team name) | list -> matches in which the team(s) is featured
                    date_range: str(YYYY-MM-DD) | list -> matches with date range specified

                Integer-based inputs -> expects 
                    match_range: int | list -> number of matches to be considered
                    gameweek_range: int | list -> matches with gameweek(s) to be considered

                ~ list is expected to have a length of 2 specifying a start and end

            :return: dict, a dictionary containing each team with its corresponding player stats and goalkeeper stats(both as pandas Dataframe), team stats(pandas DataFrame)

            :raises: Exception, when any option is not valid i.e.
                - invalid option is inputted
                - length of option is more than two for integer-based inputs and date_range
                - date_range, gameweek_range is not in specified range
                - match_range is more matches that the fixture list stipulates
                - home, away, team is not a team that played in the specified season
                - list is more than two elements and not correct type

        """

        VALID_OPTIONS = {
            "home": "matches in which the team(s) is/are home",
            "away": "matches in which the team(s) is/are away",
            "team": "matches in which the team(s) is featured",
            "date_range": "YYYY-MM-DD: matches with date range specified",
            "match_range": "number of matches to be considered",
            "gameweek_range": "matches with gameweek(s) to be considered*"
        }

        # Teams corresponding to season
        VALID_TEAMS = sorted(list(set(self.fixtures["squad_a"])))

        TEAM_STATS_TEMPLATE = {
            "matches_played": 0,
            "pts": 0,
            "home_pts": 0,
            "away_pts": 0,
            "xG": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "home_wins": 0,
            "away_wins": 0,
            "home_draws": 0,
            "away_draws": 0,
            "home_losses": 0,
            "away_losses": 0,
            "form": [],
            "home_form": [],
            "away_form": [],
            "cleansheets": 0,
            "home_cleansheets": 0,
            "away_cleansheets": 0,
            "number_of_players": 0,
            "active_players": 0,
            "goals_for": 0,
            "goals_against": 0,
            "home_goals_for": 0,
            "home_goals_against": 0,
            "away_goals_for": 0,
            "away_goals_against": 0,
            "pct_possession": 0,
            "manager(s)": [],
            "formation(s)": [],
        }

        # ERROR DETECTION

        # If key specified in not in valid options, raise an error
        for key in list(options.keys()):
            if key not in list(VALID_OPTIONS.keys()):
                raise Exception(f"{key} not in valid options.")

        # drop matches that have not been played
        played_fixtures = self.fixtures.dropna()
        team_names = list(self.players.keys())

        team_list = []

        # OPTIONS
        for option_key, option_value in options.items():
            optn_value = [option_value] if type(option_value) == str or type(
                option_value) == int else option_value

            # checks for string-based inputs
            if option_key in ["home", "away", "team"]:
                # Check if team is in current season
                for value in optn_value:
                    if value not in team_names:
                        raise Exception(
                            f"Team name - {value} is invalid.\nTeams:\n{VALID_TEAMS}.")
                if option_key == "home":
                    filtr = (played_fixtures["squad_a"].isin(optn_value))

                elif option_key == "away":
                    filtr = (played_fixtures["squad_b"].isin(optn_value))

                elif option_key == "team":
                    filtr = ((played_fixtures["squad_a"].isin(
                        optn_value) | played_fixtures["squad_b"].isin(optn_value)))

                team_list += list(optn_value)

            # check for integer-based inputs
            else:
                # Check if date range is in current season
                if option_key == "date_range":
                    if len(optn_value) > 2:
                        raise Exception(
                            "Date range expected one or two options but got more.\nCheck the 'fixtures' to see how the fixtures are distributed.")

                    elif len(optn_value) == 1:
                        filtr = (played_fixtures["date"] < optn_value[0])

                    else:
                        try:
                            filtr = (played_fixtures["date"] > optn_value[0]) and (
                                played_fixtures["date"] < optn_value[1])
                        except ValueError:
                            raise Exception(
                                "Date range is not valid.\nCheck the 'fixtures' to see how the fixtures are distributed.")
                        else:
                            pass
                # Check if match range is in current season
                elif option_key == "match_range":
                    if len(optn_value) > 2:
                        raise Exception(
                            "Match range expected one or two options but got more.\nCheck the 'fixtures' to see how the fixtures are distributed.")

                    elif len(optn_value) == 1:
                        played_fixtures = played_fixtures.reset_index(
                        ).loc[:optn_value[0] - 1]
                    else:
                        played_fixtures = played_fixtures.reset_index(
                        ).loc[optn_value[0]:optn_value[1] - 1]

                # Check if gameweek range is in current season
                elif option_key == "gameweek_range":
                    if len(optn_value) > 2:
                        raise Exception(
                            "Gameweek range is not valid.\nCheck the 'fixtures' to see how the fixtures are distributed.")
                    elif len(optn_value) == 1:
                        filtr = (played_fixtures["gameweek"] == optn_value[0])
                    else:
                        filtr = (played_fixtures["gameweek"].isin(
                            range(optn_value[0], optn_value[1])))

            if option_key != "match_range":
                played_fixtures = played_fixtures[filtr]

            # Raise error if query yields an empty fixture list
            if played_fixtures.empty:
                raise Exception(
                    "There are no fixtures corresponding with your query.\nCheck the 'fixtures' to see how the fixtures are distributed.")

        played_fixtures = played_fixtures.reset_index(drop=True)

        # data dictionary to store players and teams's stats
        data = {}

        team_list = sorted(list(self.players.keys())) if len(
            team_list) == 0 else team_list

        # column names for player data
        plyr_column_names = []
        for stat in self.headers["header"].values():
            plyr_column_names += stat

        gk_columns_names = self.headers["gk_header"]

        # Collate data for teams mentioned in team list, if empty, get for all teams
        for team in team_list:
            # Collate player names and initialise a dataframe
            player_names = self.players[team]["outfield"] + \
                self.players[team]["goalkeeper"]
            plyr_stats_df = pd.DataFrame(
                sorted(player_names), columns=['player'])

            # Contains FPL related columns names and appearance related column names
            extras = ["appearances", "starts", "sub_ins", "sub_outs", "played_60", "influence", "creativity", "threat", "ict_index",
                      "total_points", "transfers_balance", "transfers_in", "transfers_out", "bonus", "bps", "value", "value_change"]

            # Create player stats dataframe with specified column names and player names and fill with zero
            plyr_stats_df = plyr_stats_df.reindex(
                columns=plyr_column_names+extras, fill_value=0)

            # Initialise 'position' column to empty dictionary
            plyr_stats_df["position"] = [{} for _ in range(len(player_names))]

            # Store player stats dataframe
            data[team] = {"player_stats": plyr_stats_df}

            # Collate goalkeeper names
            gk_names = self.players[team]["goalkeeper"]
            gk_stats_df = pd.DataFrame(sorted(gk_names), columns=["player"])

            # Create goalkeeper stats dataframe with specified column names and goalkeeper names and fill with zero
            gk_stats_df = gk_stats_df.reindex(
                columns=gk_columns_names+["appearances"], fill_value=0)

            # Store goalkeeper stats dataframe
            data[team]["gk_stats"] = gk_stats_df

        # Create teams stats dataframe with specified column names and team names and fill with zero
        teams_stats_df = pd.DataFrame(sorted(team_list), columns=["team_name"])
        teams_stats_df = teams_stats_df.reindex(
            columns=["team_name"]+list(TEAM_STATS_TEMPLATE.keys()), fill_value=0)

        # Initialise specified columns to empty dictionaries
        for column in ["formation(s)", "manager(s)", "form", "home_form", "away_form"]:
            teams_stats_df[column] = [[] for _ in range(len(team_list))]

        # Store teams stats dataframe
        data["teams_stats"] = teams_stats_df

        # Store fixtures over which data was collated
        data['played_fixtures'] = played_fixtures

        number_of_fixtures = len(played_fixtures.index)

        # DATA COLLECTION FOR EACH FIXTURE IN 'played_fixtures'
        for index in range(number_of_fixtures):
            # Get home and away teams corresponding to fixture
            squads = (played_fixtures["squad_a"][index],
                      played_fixtures["squad_b"][index])

            # Get score and gameweek for fixture
            score = played_fixtures["score"][index].split('–')
            gameweek = played_fixtures["gameweek"][index]

            # Read FPL data for corresponding gameweek
            fpl_data = pd.read_csv(
                f"data/Fantasy Premier League/20{self.season}-{self.season + 1} gws/gw{gameweek}.csv", encoding="ISO-8859-1")

            # Given every season after 17/18 season had a different way of storing names of players (presence of '_' and number in 'name' column)
            # Process it to align with names gotten from 'players'
            if self.season >= 18:
                names = [name.split("_") for name in list(fpl_data["name"])]
                names = [n[0] + ' ' + n[1]
                         if len(n) > 1 else n[0] for n in names]
                fpl_data["name"] = names
            else:
                names = [name.replace("_", ' ')
                         for name in list(fpl_data["name"])]
                fpl_data["name"] = names

            # Path to report folder corresponding to fixture
            path = f"data/Premier League/reports/20{self.season}-{self.season + 1}/{squads[0]} v {squads[1]}"

            is_home = True  # help decipher between home and away team in fixture to seperate data collection for team data

            for squad in squads:
                if squad in team_list:
                    # Collate match_info stats which includes substitutes information
                    squad_stats_df = pd.read_csv(
                        f"{path}/{squad} stats.csv")
                    with open(f"{path}/match_info.json", encoding="utf-8") as match_file:
                        match_info = json.load(match_file)

                    subs = match_info["substitutes"][squad]

                    # PLAYER STATS
                    # Player names corresponding to team currently be checked
                    plyr_names = sorted(list(squad_stats_df["player"]))

                    for name in plyr_names:
                        # # input age for player
                        filtr = (data[squad]["player_stats"]["player"] == name)
                        sq_filtr = (squad_stats_df["player"] == name)
                        fpl_fltr = (fpl_data["name"] == name)

                        if filtr.any():
                            # update stats for each player
                            for column in plyr_column_names:
                                # specifies columns that are not string-based
                                if column not in ["player", "position", "age"]:
                                    data[squad]["player_stats"].loc[filtr,
                                                                    column] += float(squad_stats_df.loc[sq_filtr, column])
                                    if column == "minutes":
                                        mins = float(
                                            squad_stats_df.loc[sq_filtr, column])
                                        if mins > 60:  # check if minutes played in match are more than 60
                                            data[squad]["player_stats"].loc[filtr,
                                                                            "played_60"] += 1

                                        # if player was not subbed in, player started match, thus increment 'starts'
                                        if name not in list(subs.values()):
                                            data[squad]["player_stats"].loc[filtr,
                                                                            "starts"] += 1
                                        else:  # player was subbed in, increment 'sub_ins'
                                            data[squad]["player_stats"].loc[filtr,
                                                                            "sub_ins"] += 1

                                        # player among those subbed out, increment 'sub_outs'
                                        if name in list(subs.keys()):
                                            data[squad]["player_stats"].loc[filtr,
                                                                            "sub_outs"] += 1

                                else:
                                    if column == "age":  # input age for player
                                        age = data[squad]["player_stats"].loc[filtr,
                                                                              column].values
                                        if age == 0:
                                            age_string = squad_stats_df.loc[sq_filtr, column].astype(
                                                "str").values
                                            data[squad]["player_stats"].loc[filtr,
                                                                            column] = age_string

                                    elif column == "position":  # input position for each player
                                        positions = data[squad]["player_stats"].loc[filtr, column].to_dict(
                                        )
                                        row_num = list(positions.keys())[0]
                                        positions = positions[row_num]

                                        # Collating position played by player in match
                                        pstn = squad_stats_df.loc[sq_filtr, column].values.tolist(
                                        )
                                        pstns = pstn[0].split(",")

                                        for p in pstns:
                                            if p not in list(positions.keys()):
                                                positions[p] = 1
                                            else:
                                                positions[p] += 1

                            # Increment appearances for player
                            data[squad]["player_stats"].loc[filtr,
                                                            "appearances"] += 1

                            # FPL related data
                            for column in extras[5:-1]:
                                value = fpl_data.loc[fpl_fltr, column].values
                                if len(value) == 1:
                                    if column != 'value':  # increment value of column, if not 'value' column
                                        data[squad]["player_stats"].loc[filtr,
                                                                        column] += float(value)
                                    else:  # if 'value' column, calculate value change and store 'value'
                                        prev_value = float(
                                            data[squad]["player_stats"].loc[filtr, column].values)
                                        data[squad]["player_stats"].loc[filtr, 'value_change'] = (
                                            float(value) - prev_value)
                                        data[squad]["player_stats"].loc[filtr, column] = float(
                                            value)

                    # GOALKEEPER STATS
                    # Goalkeeper name(s) corresponding to team currently be checked
                    gk_squad_stats_df = pd.read_csv(
                        f"{path}/{squad} gk_stats.csv")
                    glkpr_names = sorted(list(gk_squad_stats_df["player"]))

                    for name in glkpr_names:
                        # Filter squad data by goalkeeper name
                        filtr = (data[squad]["gk_stats"]["player"] == name)
                        sq_filtr = (gk_squad_stats_df["player"] == name)

                        for column in gk_columns_names:
                            if column not in ["player", "age"]:
                                data[squad]["gk_stats"].loc[filtr,
                                                            column] += float(gk_squad_stats_df.loc[sq_filtr, column])
                            else:
                                if column == "age":  # input age for player
                                    age = data[squad]["gk_stats"].loc[filtr,
                                                                      column].values
                                    if age == 0:
                                        age_string = gk_squad_stats_df.loc[sq_filtr, column].astype(
                                            "str").values
                                        data[squad]["gk_stats"].loc[filtr,
                                                                    column] = age_string

                        data[squad]["gk_stats"].loc[filtr, "appearances"] += 1

                    # Collate manager for each team
                    mngrs = (
                        match_info["managers_captains"][0].split(": ")[-1],
                        match_info["managers_captains"][2].split(": ")[-1]
                    )
                    mngrs = {squads[i]: mngrs[i] for i in range(2)}

                    # Collate manager for each team
                    pssn = match_info["possession"]
                    pssn = {squads[i]: pssn[i] for i in range(2)}

                    # Store formations used by team
                    frmtns = list(match_info["formations"].values())
                    frmtns = {squads[i]: frmtns[i] for i in range(2)}

                    # Store xG for each team
                    xgs = match_info["score_xgs"]
                    xgs = {squads[i]: xgs[i] for i in range(2)}

                    tm_filtr = (data["teams_stats"]["team_name"] == squad)

                    data["teams_stats"].loc[tm_filtr,
                                            "pct_possession"] += int(pssn[squad])

                    # Collate and store manager for each team in list
                    managers = data["teams_stats"].loc[tm_filtr,
                                                       "manager(s)"].values
                    if mngrs[squad] not in managers.tolist()[0]:
                        managers[0].append(mngrs[squad])
                    data["teams_stats"].loc[tm_filtr, "manager(s)"] = managers

                    # Collate and store formations used by each team in list
                    formations = data["teams_stats"].loc[tm_filtr,
                                                         "formation(s)"].values
                    if frmtns[squad] not in formations.tolist()[0]:
                        formations[0].append(frmtns[squad])
                    data["teams_stats"].loc[tm_filtr,
                                            "formation(s)"] = formations

                    data["teams_stats"].loc[tm_filtr,
                                            "xG"] += float(xgs[squad])

                    # score additions
                    result = None
                    if is_home:  # if team is at home, increment corresponding home stats
                        data["teams_stats"].loc[tm_filtr,
                                                "goals_for"] += int(score[0])
                        data["teams_stats"].loc[tm_filtr,
                                                "goals_against"] += int(score[1])
                        data["teams_stats"].loc[tm_filtr, "cleansheets"] = data["teams_stats"].loc[tm_filtr,
                                                                                                   "cleansheets"] + 1 if int(score[1]) == 0 else data["teams_stats"].loc[tm_filtr, "cleansheets"]
                        data["teams_stats"].loc[tm_filtr, "home_cleansheets"] = data["teams_stats"].loc[tm_filtr,
                                                                                                        "home_cleansheets"] + 1 if int(score[1]) == 0 else data["teams_stats"].loc[tm_filtr, "home_cleansheets"]
                        data["teams_stats"].loc[tm_filtr,
                                                "home_goals_for"] += int(score[0])
                        data["teams_stats"].loc[tm_filtr,
                                                "home_goals_against"] += int(score[1])

                        # Determine results and append points accordingly
                        if score[0] > score[1]:
                            result = 'W'
                            data["teams_stats"].loc[tm_filtr, "wins"] += 1
                            data["teams_stats"].loc[tm_filtr, "home_wins"] += 1
                            data["teams_stats"].loc[tm_filtr, "pts"] += 3
                            data["teams_stats"].loc[tm_filtr, "home_pts"] += 3

                        elif score[0] == score[1]:
                            result = 'D'
                            data["teams_stats"].loc[tm_filtr, "draws"] += 1
                            data["teams_stats"].loc[tm_filtr, "home_draws"] += 1
                            data["teams_stats"].loc[tm_filtr, "pts"] += 1
                            data["teams_stats"].loc[tm_filtr, "home_pts"] += 1

                        else:
                            result = 'L'
                            data["teams_stats"].loc[tm_filtr, "losses"] += 1
                            data["teams_stats"].loc[tm_filtr, "home_losses"] += 1

                        # Form data stores form for the last 5 home matches
                        h_form = data["teams_stats"].loc[tm_filtr,
                                                         "home_form"].values
                        if len(h_form.tolist()[0]) == 5:
                            h_form[0] = h_form[0][1:] + [result]
                        else:
                            h_form[0].append(result)
                        data["teams_stats"].loc[tm_filtr, "home_form"] = h_form

                    else:  # if team is at away, increment corresponding away stats
                        data["teams_stats"].loc[tm_filtr,
                                                "goals_for"] += int(score[1])
                        data["teams_stats"].loc[tm_filtr,
                                                "goals_against"] += int(score[0])
                        data["teams_stats"].loc[tm_filtr, "cleansheets"] = data["teams_stats"].loc[tm_filtr,
                                                                                                   "cleansheets"] + 1 if int(score[0]) == 0 else data["teams_stats"].loc[tm_filtr, "cleansheets"]
                        data["teams_stats"].loc[tm_filtr, "away_cleansheets"] = data["teams_stats"].loc[tm_filtr,
                                                                                                        "away_cleansheets"] + 1 if int(score[1]) == 0 else data["teams_stats"].loc[tm_filtr, "away_cleansheets"]
                        data["teams_stats"].loc[tm_filtr,
                                                "away_goals_for"] += int(score[1])
                        data["teams_stats"].loc[tm_filtr,
                                                "away_goals_against"] += int(score[0])

                        # Determine results and append points accordingly
                        if score[1] > score[0]:
                            result = 'W'
                            data["teams_stats"].loc[tm_filtr, "wins"] += 1
                            data["teams_stats"].loc[tm_filtr, "away_wins"] += 1
                            data["teams_stats"].loc[tm_filtr, "pts"] += 3
                            data["teams_stats"].loc[tm_filtr, "away_pts"] += 3

                        elif score[1] == score[0]:
                            result = 'D'
                            data["teams_stats"].loc[tm_filtr, "draws"] += 1
                            data["teams_stats"].loc[tm_filtr, "away_draws"] += 1
                            data["teams_stats"].loc[tm_filtr, "pts"] += 1
                            data["teams_stats"].loc[tm_filtr, "away_pts"] += 1

                        else:
                            result = 'L'
                            data["teams_stats"].loc[tm_filtr, "losses"] += 1
                            data["teams_stats"].loc[tm_filtr, "away_losses"] += 1

                        # Form data stores form for the last 5 away matches
                        a_form = data["teams_stats"].loc[tm_filtr,
                                                         "away_form"].values
                        if len(a_form.tolist()[0]) == 5:
                            a_form[0] = a_form[0][1:] + [result]
                        else:
                            a_form[0].append(result)
                        data["teams_stats"].loc[tm_filtr, "away_form"] = a_form

                    form = data["teams_stats"].loc[tm_filtr, "form"].values
                    if len(form.tolist()[0]) == 5:
                        form[0] = form[0][1:] + [result]
                    else:
                        form[0].append(result)
                    data["teams_stats"].loc[tm_filtr, "form"] = form

                    data["teams_stats"].loc[tm_filtr, "matches_played"] += 1

                is_home = False

            # team totals: columns are summed and added to the 'team_stats'
            team_totals = {}
            stats_total = ["cards_yellow", "cards_red", "cards_yellow_red"]

            for team in team_list:
                for stat in stats_total:
                    total = sum(list(data[team]["player_stats"][stat]))
                    if stat not in list(team_totals.keys()):
                        team_totals[stat] = [total]
                    else:
                        team_totals[stat].append(total)

            for stat in stats_total:
                data["teams_stats"][stat] = team_totals[stat]

        for key, value in data.items():
            if key not in ['teams_stats', 'played_fixtures']:
                total_aerials = value["player_stats"]["aerials_lost"] + \
                    value["player_stats"]["aerials_won"]  # total aerials is sum of aerials won and lost
                value["player_stats"]["aerials_won_pct"] = (
                    value["player_stats"]["aerials_won"] / total_aerials)  # calculate aerials won percentage

                dribble_tackles = value["player_stats"]["dribble_tackles"] + \
                    value["player_stats"]["dribbled_past"] # total dribble tackles is sum of dribble tackles and dribbles past
                value["player_stats"]["dribble_tackles_pct"] = (
                    value["player_stats"]["dribble_tackles"] / dribble_tackles) # calculate dribble tackles percentage

                value["player_stats"]['dribbles_completed_pct'] = (
                    value["player_stats"]['dribbles_completed'] / value["player_stats"]['dribbles']) # calculate dribbles completed percentage

                value["player_stats"]['passes_pct'] = (
                    value["player_stats"]['passes_completed'] / value["player_stats"]['passes']) # calculate passes completed percentage
                value["player_stats"]['passes_pct_medium'] = (
                    value["player_stats"]['passes_completed_medium'] / value["player_stats"]['passes_medium']) # calculate passes medium completed percentage
                value["player_stats"]['passes_pct_long'] = (
                    value["player_stats"]['passes_completed_long'] / value["player_stats"]['passes_long']) # calculate passes long completed percentage

                value["player_stats"]['passes_received_pct'] = (
                    value["player_stats"]['passes_received'] / value["player_stats"]['pass_targets']) # calculate passed received percentage
                value["player_stats"]['pressure_regain_pct'] = (
                    value["player_stats"]['pressure_regains'] / value["player_stats"]['pressures']) # calculate pressure regain percentage

                # Fill NaNs to zeros
                value["player_stats"].fillna(0, inplace=True)

                # if player change is greater than 30, this implies there has not been any change in value
                value["player_stats"]["value_change"] = np.where(
                    value["player_stats"]["value_change"] > 30, 0, value["player_stats"]["value_change"])

        return data
