import json
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

# All data gotten here is from scraping the https://fbref.com website for Premier League

SEASON_RANGE = range(17, 22)
COLUMNS = ['player',
           'position',
           'age',
           'minutes',
           'cards_yellow',
           'cards_red',
           'cards_yellow_red',
           'fouls',
           'fouled',
           'offsides',
           'pens_won',
           'pens_conceded',
           'own_goals',
           'ball_recoveries',
           'aerials_won',
           'aerials_lost',
           'aerials_won_pct',
           'passes_completed',
           'passes',
           'passes_pct',
           'passes_total_distance',
           'passes_progressive_distance',
           'passes_completed_short',
           'passes_short',
           'passes_pct_short',
           'passes_completed_medium',
           'passes_medium',
           'passes_pct_medium',
           'passes_completed_long',
           'passes_long',
           'passes_pct_long',
           'assisted_shots',
           'passes_into_final_third',
           'passes_into_penalty_area',
           'crosses_into_penalty_area',
           'progressive_passes',
           'passes_live',
           'passes_dead',
           'passes_free_kicks',
           'through_balls',
           'passes_pressure',
           'passes_switches',
           'crosses',
           'corner_kicks',
           'passes_ground',
           'passes_low',
           'passes_high',
           'passes_head',
           'throw_ins',
           'passes_other_body',
           'passes_offsides',
           'passes_oob',
           'passes_intercepted',
           'passes_blocked',
           'tackles',
           'tackles_won',
           'tackles_def_3rd',
           'tackles_mid_3rd',
           'tackles_att_3rd',
           'dribble_tackles',
           'dribbles_vs',
           'dribble_tackles_pct',
           'dribbled_past',
           'pressures',
           'pressure_regains',
           'pressure_regain_pct',
           'pressures_def_3rd',
           'pressures_mid_3rd',
           'pressures_att_3rd',
           'blocks',
           'blocked_shots',
           'blocked_shots_saves',
           'blocked_passes',
           'interceptions',
           'tackles_interceptions',
           'clearances',
           'errors',
           'goals',
           'assists',
           'pens_made',
           'pens_att',
           'shots_total',
           'shots_on_target',
           'xg',
           'npxg',
           'xa',
           'sca',
           'gca',
           'touches',
           'touches_def_pen_area',
           'touches_def_3rd',
           'touches_mid_3rd',
           'touches_att_3rd',
           'touches_att_pen_area',
           'touches_live_ball',
           'dribbles_completed',
           'dribbles',
           'dribbles_completed_pct',
           'players_dribbled_past',
           'carries',
           'carry_distance',
           'carry_progressive_distance',
           'progressive_carries',
           'carries_into_final_third',
           'carries_into_penalty_area',
           'miscontrols',
           'dispossessed',
           'pass_targets',
           'passes_received',
           'passes_received_pct',
           'progressive_passes_received',
           ]


def folder_create(folder_path):
    # Creates folder for each fixture retrieved
    try:
        os.mkdir(folder_path)
    except OSError:
        return False
    else:
        return True


def file_create(file_details, file_name, file_path):
    # Creates files for each fixture retrieved
    try:
        with open(f"{file_path}/{file_name}") as file:
            file_data = json.load(file)
    except FileNotFoundError:
        file_data = json.dumps(file_details, indent=4)
        with open(f"{file_path}/{file_name}", "w", encoding="utf-8") as file:
            file.write(file_data)
        return True
    else:
        return False


def players_with_team_position(season):
    """Returns list of players in a team and whether or not they are an outfield player or a goalkeeper"""

    if season not in SEASON_RANGE:
        print("Season should range from 17 to 21 representing 2017-2018 to 2021-2022.")
        return

    # Links corresponding to seasons specified
    SEASON_STATS = {
        "2021-2022": "https://fbref.com/en/comps/9/Premier-League-Stats",
        "2020-2021": "https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats",
        "2019-2020": "https://fbref.com/en/comps/9/3232/2019-2020-Premier-League-Stats",
        "2018-2019": "https://fbref.com/en/comps/9/1889/2018-2019-Premier-League-Stats",
        "2017-2018": "https://fbref.com/en/comps/9/1631/2017-2018-Premier-League-Stats"
    }

    # Links of teams belonging to a season and link to players list
    team_links = {}
    response = requests.get(SEASON_STATS[f"20{season}-20{season + 1}"])
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("caption").parent
    trows = table.find("tbody").find_all("tr")
    for row in trows:
        link = row.find("td").find("a")
        team_links[link.text] = link["href"]

    PREFIX = "https://fbref.com"

    plyrs_tm_pstn = {}

    # Scrape data from website to locate outfield players and goalkeepers
    for team, link in team_links.items():
        plyrs_tm_pstn[team] = {
            "outfield": [],
            "goalkeeper": []
        }
        response = requests.get(PREFIX + link)
        soup = BeautifulSoup(response.text, "html.parser")
        trows = soup.find("tbody").find_all("tr")
        for row in trows:
            if row.get("class") is None:
                player = row.find("th").text
                outfield = False if row.find(
                    "td", {"data-stat": "position"}).text == "GK" else True
                if outfield:
                    plyrs_tm_pstn[team]["outfield"].append(player)
                else:
                    plyrs_tm_pstn[team]["goalkeeper"].append(player)

    return plyrs_tm_pstn


def score_and_fixtures(season):
    """Return scores and fixtures belonging a particular season"""

    if season not in SEASON_RANGE:
        raise Exception(
            f"Season should range from {SEASON_RANGE.start} to {SEASON_RANGE.stop - 1} representing 20{SEASON_RANGE.start}-20{SEASON_RANGE.start + 1} to 20{SEASON_RANGE.stop - 1}-20{SEASON_RANGE.stop}.")

    else:
        # Links corresponding to seasons specified
        SEASONS = {
            "2021-2022": "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures",
            "2020-2021": "https://fbref.com/en/comps/9/10728/schedule/2020-2021-Premier-League-Scores-and-Fixtures",
            "2019-2020": "https://fbref.com/en/comps/9/3232/schedule/2019-2020-Premier-League-Scores-and-Fixtures",
            "2018-2019": "https://fbref.com/en/comps/9/1889/schedule/2018-2019-Premier-League-Scores-and-Fixtures",
            "2017-2018": "https://fbref.com/en/comps/9/1631/schedule/2017-2018-Premier-League-Scores-and-Fixtures"
        }

        fxtr_link = SEASONS[f"20{season}-20{season + 1}"]
        response = requests.get(fxtr_link)
        soup = BeautifulSoup(response.text, "html.parser")
        trows = soup.find("tbody").find_all("tr")

        headers = ["gameweek", "date", "squad_a",
                   "score", "squad_b", "match_report"]
        match_reports = {}

        for i in headers:
            match_reports[i] = []
        for row in trows:
            gmwk = row.find("th")
            if gmwk.text not in ["", "Wk"]:
                match_reports["gameweek"].append(gmwk.text)
                match_stats = row.find_all("td")
                for stat in match_stats:
                    if stat["data-stat"] in headers:
                        if stat["data-stat"] != "match_report":
                            match_reports[stat["data-stat"]].append(stat.text)
                        else:
                            href = stat.find("a")
                            link = href["href"].split(
                                "?")[0] if href != None else None
                            match_reports["match_report"].append(link)
        scores_and_fixtures_df = pd.DataFrame(match_reports)
        scores_and_fixtures_df.to_csv(
            f"data/Premier League/scores and fixtures/20{season}-20{season + 1} PL Scores & Fixtures.csv", index=False)


def match_reports(season):
    """Downloading match report for matches played in a particular season"""

    if season not in SEASON_RANGE:
        print("Season should range from 17 to 21 representing 2017-2018 to 2021-2022.")

    else:
        # Player stats header information
        with open("data/Premier League/header information/headers.json", encoding="utf-8") as hdr:
            header_dictionary = json.load(hdr)

        # Goalkeeper stats header information
        with open("data/Premier League/header information/gk_headers.json", encoding="utf-8") as gk_hdr:
            gk_header_dictionary = json.load(gk_hdr)
        gk_header_dictionary = gk_header_dictionary["List"]

        # Shots stats header information
        with open("data/Premier League/header information/sh_headers.json", encoding="utf-8") as sh_hdr:
            sh_header_dictionary = json.load(sh_hdr)
        sh_header_dictionary = sh_header_dictionary["List"]

        # Initialise scores and fixtures belonging to a season and removing all unplayed matches
        scores_and_fixtures_df = pd.read_csv(
            f"data/Premier League/scores and fixtures/20{season}-20{season + 1} PL Scores & Fixtures.csv")
        scores_and_fixtures_df.dropna(inplace=True)

        squad_a = list(scores_and_fixtures_df["squad_a"])
        squad_b = list(scores_and_fixtures_df["squad_b"])
        report_links = list(scores_and_fixtures_df["match_report"])

        PREFIX = "https://fbref.com"
        for indx in range(len(report_links)):
            PREFIX = "https://fbref.com"
            link = PREFIX + report_links[indx]
            path = f"data/Premier League/reports/20{season}-20{season + 1}/{squad_a[indx]} v {squad_b[indx]}"

            if folder_create(path):
                # Match information includes scores, manager and captain names, score xG, formations, team names, possession
                response = requests.get(link)
                soup = BeautifulSoup(response.text, "html.parser")

                match_info = {}

                scorebox = soup.find("div", class_="scorebox")
                mngrs_caps = scorebox.find_all("div", class_="datapoint")
                managers_captains = []
                for item in mngrs_caps:
                    managers_captains.append(item.text)

                match_info["managers_captains"] = managers_captains

                xgs = scorebox.find_all("div", class_="score_xg")
                score_xgs = []
                for i in xgs:
                    score_xgs.append(i.text)

                match_info["score_xgs"] = score_xgs

                frmtns = soup.find_all("div", class_="lineup")
                formations = {}

                for f in frmtns:
                    text = f.find("th").text
                    team_frmtn = text.split(" (")
                    formations[team_frmtn[0]] = team_frmtn[1].replace(")", "")

                match_info["formations"] = formations

                trows = soup.find("div", {"id": "team_stats"}).find(
                    "table").find_all("tr")

                possession = trows[2].text.replace("\n", "").split("%")[:-1]
                match_info["possession"] = possession

                events = soup.find(text="Match Summary").parent.parent

                home = events.find_all(class_="event a")
                away = events.find_all(class_="event b")

                substitutes = {}

                substitutes[squad_a[indx]] = {}
                for event in home:
                    if event.find("div", class_="event_icon substitute_in") is not None:
                        playrs = event.find_all("a")
                        if len(playrs) == 2:
                            substitutes[squad_a[indx]
                                        ][playrs[0].text] = playrs[1].text

                substitutes[squad_b[indx]] = {}
                for event in away:
                    if event.find("div", class_="event_icon substitute_in") is not None:
                        playrs = event.find_all("a")
                        if len(playrs) == 2:
                            substitutes[squad_b[indx]
                                        ][playrs[0].text] = playrs[1].text

                match_info["substitutes"] = substitutes

                file_create(file_details=match_info, file_path=path,
                            file_name="match_info.json")

                # Shots stats based on column names specified in shots stats header information
                sh_match_stats_table = {s: [] for s in sh_header_dictionary}

                sh_stats_table = soup.find(text="Shots Table").parent.parent
                trows = sh_stats_table.find("tbody").find_all("tr")
                for row in trows:
                    tdata = row.find_all("td")
                    for datum in tdata:
                        if datum["data-stat"] in list(sh_match_stats_table.keys()):
                            if datum.find("a") is not None:
                                sh_match_stats_table[datum["data-stat"]
                                                     ].append(datum.find("a").text)
                            else:
                                sh_match_stats_table[datum["data-stat"]
                                                     ].append(datum.text)

                sh_stat_df = pd.DataFrame(sh_match_stats_table)
                sh_stat_df.to_csv(f"{path}/shot_stats.csv", index=False)

                # Player and goalkeeper data based on column names specified in player and goalkeeper stats header information
                teams = list(match_info["formations"].keys())
                for team in teams:
                    match_stats_info = {}
                    for table_name, table_columns in header_dictionary.items():
                        table = {column: [] for column in table_columns}
                        match_stats_info[table_name] = table

                    match_stats_table = {team: match_stats_info}

                    STATS_KEY = {
                        0: ["misc", "attack"],
                        1: ["passing"],
                        2: ["passing_types"],
                        3: ["defense"],
                        4: ["possession"],
                        5: ["misc", "defense"]
                    }

                    stats_tables = soup.find_all(
                        text=f"{team} Player Stats Table")

                    for indx in range(len(stats_tables)):
                        stat_table = stats_tables[indx].parent.parent
                        trows = stat_table.find("tbody").find_all("tr")
                        for row in trows:
                            name = row.find("th").find("a").text
                            if name not in match_stats_table[team]["misc"]["player"]:
                                match_stats_table[team]["misc"]["player"].append(
                                    name)

                            if "misc" in STATS_KEY[indx]:
                                tdata = row.find_all('td')
                                for datum in tdata:
                                    if datum["data-stat"] in header_dictionary["misc"]:
                                        match_stats_table[team]["misc"][datum["data-stat"]].append(
                                            datum.text)

                            if "attack" in STATS_KEY[indx]:
                                tdata = row.find_all('td')
                                for datum in tdata:
                                    if datum["data-stat"] in header_dictionary["attack"]:
                                        match_stats_table[team]["attack"][datum["data-stat"]].append(
                                            datum.text)

                            if "passing" in STATS_KEY[indx]:
                                tdata = row.find_all('td')
                                for datum in tdata:
                                    if datum["data-stat"] in header_dictionary["passing"]:
                                        match_stats_table[team]["passing"][datum["data-stat"]].append(
                                            datum.text)

                            if "passing_types" in STATS_KEY[indx]:
                                tdata = row.find_all('td')
                                for datum in tdata:
                                    if datum["data-stat"] in header_dictionary["passing_types"]:
                                        match_stats_table[team]["passing_types"][datum["data-stat"]].append(
                                            datum.text)

                            if "defense" in STATS_KEY[indx]:
                                tdata = row.find_all('td')
                                for datum in tdata:
                                    if datum["data-stat"] in header_dictionary["defense"]:
                                        match_stats_table[team]["defense"][datum["data-stat"]].append(
                                            datum.text)

                            if "possession" in STATS_KEY[indx]:
                                tdata = row.find_all('td')
                                for datum in tdata:
                                    if datum["data-stat"] in header_dictionary["possession"]:
                                        match_stats_table[team]["possession"][datum["data-stat"]].append(
                                            datum.text)

                    # Removing of duplicate data from player stats for each team
                    for column in ["position", "age", "minutes", "cards_yellow", "cards_red"]:
                        column_length = int(
                            len(match_stats_table[team]['misc'][column]) / 2)
                        match_stats_table[team]['misc'][column] = match_stats_table[team]['misc'][column][:column_length]

                    for column in ["interceptions", "tackles_won"]:
                        column_length = int(
                            len(match_stats_table[team]['defense'][column]) / 2)
                        match_stats_table[team]['defense'][column] = match_stats_table[team]['defense'][column][:column_length]

                    stat_dfs = [pd.DataFrame(match_stats_table[team][s])
                                for s in ['misc', 'passing', 'passing_types', 'defense', 'attack', 'possession']]

                    team_df = pd.concat(stat_dfs, axis=1)
                    team_df.columns = COLUMNS
                    team_df.to_csv(f'{path}/{team} stats.csv', index=False)

                    gk_match_info = {item: [] for item in gk_header_dictionary}
                    gk_match_stats_table = {team: gk_match_info}

                    gk_stats_table = soup.find(
                        text=f"{team} Goalkeeper Stats Table").parent.parent
                    trows = gk_stats_table.find("tbody").find_all("tr")
                    for row in trows:
                        name = row.find("th").find("a").text
                        gk_match_stats_table[team]["player"].append(name)
                        tdata = row.find_all("td")
                        for datum in tdata:
                            if datum["data-stat"] in list(gk_match_info.keys()):
                                gk_match_stats_table[team][datum["data-stat"]
                                                           ].append(datum.text)

                    gk_stat_df = pd.DataFrame(gk_match_stats_table[team])
                    gk_stat_df.to_csv(
                        f"{path}/{team} gk_stats.csv", index=False)
