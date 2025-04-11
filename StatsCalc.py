import pandas as pd
from datetime import datetime

# class StatsCalc:
#     def __init__(self, df: pd.DataFrame):
#         self.df = df
    
# class CrewmateCalc:
#     def __init__ (self):
#         self.crewColumns = [
#             "Name", 
#             "CrewGames", 
#             "PPG", 
#             "First Round Victim",
#             "√ Eject",
#             "x Eject",
#             "Eject Voting Acc",
#             "√ Indv",
#             "x Indv",
#             "Indv Voting Acc.",
#             "TCV",
#             "Total V",
#             "True VA",
#             "Vote Farmer",
#             "Critical Error",
#             "Alv Last Meeting",
#             "Throw Rate",
#             "Win Alv",
#             "Loss Alv",
#             "Task Bozo",
#             "Avg Task Compl.",
#             "Task Wins",
#             "Points",
#             "CAP",
#             "Total Tasks Completed"
#         ]
#         self.crewdf = pd.DataFrame(columns=self.crewColumns)
#         self.crewdf.set_index("Name",inplace=True)

#     def getCrewDf(self):
#         return self.crewdf

#     def getCrewgames(self, df):
#         row = df
        
#         role = str(row["Role"]).strip().upper()
#         if role != "CREWMATE":
#             return
        
#         name = row["Name"]
#         # If player's row is not in the crew dataframe, initialize it using a dictionary.
#         if name not in self.crewdf.index:
#             default_row = {col: 0 for col in self.crewdf.columns}
#             self.crewdf.loc[name] = default_row
        
#         def to_bool(val):
#             if isinstance(val, bool):
#                 return val
#             if isinstance(val, str):
#                 return val.strip().lower() == "true"
#             return bool(val)

#         win_type = str(row["Win Type"]).strip().lower()
        
#         self.crewdf.at[name, "CrewGames"] += 1

#         if to_bool(row["First Two Victims R1"]):
#             self.crewdf.at[name, "First Round Victim"] +=1
        
#         correct_ejects = row["Correct Ejects"]
#         incorrect_ejects = row["Incorrect Ejects"]
        
#         self.crewdf.at[name, "√ Eject"] += correct_ejects
#         self.crewdf.at[name, "x Eject"] += incorrect_ejects

#         correct_votes = row["Correct Votes"]
#         incorrect_votes = row["Incorrect Votes"]

#         self.crewdf.at[name, "TCV"] += correct_votes
#         total_votes = correct_votes + incorrect_votes
#         self.crewdf.at[name, "Total V"] += total_votes

#         indv_correct = correct_votes - correct_ejects
#         indv_incorrect = incorrect_votes - incorrect_ejects
#         self.crewdf.at[name, "√ Indv"] += indv_correct
#         self.crewdf.at[name, "x Indv"] += indv_incorrect
    
#         if correct_votes >= 4:
#             self.crewdf.at[name, "Vote Farmer"] += 1
        
#         if to_bool(row["Critical Meeting Error"]):
#             self.crewdf.at[name, "Critical Error"] += 1
        

#         alv_last_meeting = to_bool(row["Alive at Last Meeting"])
#         if alv_last_meeting:
#             self.crewdf.at[name, "Alv Last Meeting"] += 1

#             if win_type in ["crewmatewin", "taskwin"]:
#                 self.crewdf.at[name, "Win Alv"] += 1
#             elif win_type in ["impostorwin", "timesup", "reactorwin"]:
#                 self.crewdf.at[name, "Loss Alv"] += 1
            
#         alv_count = self.crewdf.at[name, "Alv Last Meeting"]
#         if alv_count > 0:
#             self.crewdf.at[name, "Throw Rate"] = round(
#                 self.crewdf.at[name, "Critical Error"] / alv_count * 100, 2
#             )

#         total_alv = (
#             self.crewdf.at[name, "Win Alv"] + self.crewdf.at[name, "Loss Alv"]
#         )

#         if total_alv > 0:
#             self.crewdf.at[name, "Win % Alv"] = round(
#                 self.crewdf.at[name, "Win Alv"] / total_alv * 100, 2
#             )
        
#         if win_type == "timesup" and row["Tasks Completed"] < 10:
#             self.crewdf.at[name, "Task Bozo"] += 1

#         self.crewdf.at[name, "Total Tasks Completed"] += row["Tasks Completed"]
#         games = self.crewdf.at[name, "CrewGames"]
#         total_tasks = self.crewdf.at[name, "Total Tasks Completed"]
#         self.crewdf.at[name, "Avg Task Compl."] = round(total_tasks / games, 2)

#         if win_type == "taskwin":
#             self.crewdf.at[name, "Task Wins"] += 1
        
#         points = (
#             self.crewdf.at[name, "√ Eject"] * 3
#             - self.crewdf.at[name, "x Eject"] * 2
#             + self.crewdf.at[name, "√ Indv"] * 1
#             - self.crewdf.at[name, "x Indv"] * 0.5
#             + self.crewdf.at[name, "First Round Victim"] * 0.5
#             + self.crewdf.at[name, "Task Wins"] * 3
#             - self.crewdf.at[name, "Critical Error"] * 6
#             - self.crewdf.at[name, "Task Bozo"] * 8
#         )
#         self.crewdf.at[name, "Points"] = round(points, 2)

#         # PPG
#         crew_games = self.crewdf.at[name, "CrewGames"]
#         if crew_games > 0:
#             self.crewdf.at[name, "PPG"] = round(
#                 self.crewdf.at[name, "Points"] / crew_games, 2
#             )

#         # Accuracy Calculations
#         eject_total = self.crewdf.at[name, "√ Eject"] + self.crewdf.at[name, "x Eject"]
#         if eject_total > 0:
#             self.crewdf.at[name, "Eject Voting Acc"] = round(
#                 self.crewdf.at[name, "√ Eject"] / eject_total * 100, 2
#             )

#         indv_total = self.crewdf.at[name, "√ Indv"] + self.crewdf.at[name, "x Indv"]
#         if indv_total > 0:
#             self.crewdf.at[name, "Indv Voting Acc."] = round(
#                 self.crewdf.at[name, "√ Indv"] / indv_total * 100, 2
#             )

#         total_votes = self.crewdf.at[name, "Total V"]
#         if total_votes > 0:
#             self.crewdf.at[name, "True VA"] = round(
#                 self.crewdf.at[name, "TCV"] / total_votes * 100, 2
#             )

class CrewmateCalc:
    def __init__(self):
        self.crewColumns = [
            "Name", "CrewGames", "PPG", "First Round Victim", "√ Eject", "x Eject",
            "Eject Voting Acc", "√ Indv", "x Indv", "Indv Voting Acc.", "TCV", "Total V",
            "True VA", "Vote Farmer", "Critical Error", "Alv Last Meeting", "Throw Rate",
            "Win Alv", "Loss Alv", "Task Bozo", "Avg Task Compl.", "Task Wins", "Points",
            "CAP", "Total Tasks Completed", "Win % Alv"
        ]
        self.crewdf = pd.DataFrame(columns=self.crewColumns)
        self.crewdf.set_index("Name", inplace=True)

    def getCrewDf(self):
        return self.crewdf

    def getCrewgames(self, df):
        """
        Accepts a single-row DataFrame and updates stats for that row/player.
        """
        if df.empty:
            return
        
        #print(df.to_markdown())

        row = df.iloc[0]
        name = row["Name"]

        # Initialize player if not already present
        if name not in self.crewdf.index:
            self.crewdf.loc[name] = {col: 0 for col in self.crewdf.columns}

        self.aggregate_player_stats(name, df)

    def aggregate_player_stats(self, name, group):
        """
        Aggregate stats for a player based on a single row.
        """
        row = group.iloc[0]

        # Skip if not a Crewmate
        role = str(row["Role"]).strip().upper()
        if role != "CREWMATE":
            return

        # Aggregation dictionary
        aggregates = {
            "correct_ejects": row["Correct Ejects"],
            "incorrect_ejects": row["Incorrect Ejects"],
            "correct_votes": row["Correct Votes"],
            "incorrect_votes": row["Incorrect Votes"],
            "first_victim": int(to_bool(row["First Two Victims R1"])),
            "tasks_completed": row["Tasks Completed"],
            "win_type": str(row["Win Type"]).strip().lower()
        }

        if to_bool(row["Critical Meeting Error"]):
            self.crewdf.at[name, "Critical Error"] += 1

        if to_bool(row["Alive at Last Meeting"]):
            self.crewdf.at[name, "Alv Last Meeting"] += 1
            self.update_win_stats(name, aggregates["win_type"])

        #print(f"Aggregate Win_Type: {aggregates['win_type']}")
        if aggregates["win_type"] == "taskwin":
            self.crewdf.at[name, "Task Wins"] += 1

        if row["Correct Votes"] >= 4:
            self.crewdf.at[name, "Vote Farmer"] += 1

        if row["Tasks Completed"] < 10 and aggregates["win_type"] == "timesup":
            self.crewdf.at[name, "Task Bozo"] += 1

        # Increment CrewGames directly
        self.crewdf.at[name, "CrewGames"] += 1

        # Update player stats
        self.update_player_stats(name, aggregates)

    def update_win_stats(self, name, win_type):
        if win_type in ["crewmatewin", "taskwin"]:
            self.crewdf.at[name, "Win Alv"] += 1
        elif win_type in ["impostorwin", "timesup", "reactorwin"]:
            self.crewdf.at[name, "Loss Alv"] += 1

    def update_player_stats(self, name, aggregates):
        self.crewdf.at[name, "First Round Victim"] += aggregates["first_victim"]
        self.crewdf.at[name, "√ Eject"] += aggregates["correct_ejects"]
        self.crewdf.at[name, "x Eject"] += aggregates["incorrect_ejects"]
        self.crewdf.at[name, "TCV"] += aggregates["correct_votes"]
        self.crewdf.at[name, "Total V"] += aggregates["correct_votes"] + aggregates["incorrect_votes"]
        self.crewdf.at[name, "√ Indv"] += aggregates["correct_votes"] - aggregates["correct_ejects"]
        self.crewdf.at[name, "x Indv"] += aggregates["incorrect_votes"] - aggregates["incorrect_ejects"]
        self.crewdf.at[name, "Total Tasks Completed"] += aggregates["tasks_completed"]

        self.calculate_advanced_stats(name)

    def calculate_advanced_stats(self, name):
        total_votes = self.crewdf.at[name, "Total V"]
        total_ejects = self.crewdf.at[name, "√ Eject"] + self.crewdf.at[name, "x Eject"]
        total_indv = self.crewdf.at[name, "√ Indv"] + self.crewdf.at[name, "x Indv"]

        self.update_accuracy(name, total_votes, total_ejects, total_indv)
        self.calculate_points(name)
        self.calculate_ppg(name)
        self.calculate_task_avg(name)
        self.calculate_throw_rate(name)
        self.calculate_win_alv_percentage(name)
        self.calculate_cap(name)

    def update_accuracy(self, name, total_votes, total_ejects, total_indv):
        if total_votes > 0:
            self.crewdf.at[name, "True VA"] = round(self.crewdf.at[name, "TCV"] / total_votes * 100, 2)
        if total_ejects > 0:
            self.crewdf.at[name, "Eject Voting Acc"] = round(self.crewdf.at[name, "√ Eject"] / total_ejects * 100, 2)
        if total_indv > 0:
            self.crewdf.at[name, "Indv Voting Acc."] = round(self.crewdf.at[name, "√ Indv"] / total_indv * 100, 2)

    def calculate_points(self, name):
        points = (
            self.crewdf.at[name, "√ Eject"] * 3
            - self.crewdf.at[name, "x Eject"] * 2
            + self.crewdf.at[name, "√ Indv"] * 1
            - self.crewdf.at[name, "x Indv"] * 0.5
            + self.crewdf.at[name, "First Round Victim"] * 0.5
            + self.crewdf.at[name, "Task Wins"] * 3
            - self.crewdf.at[name, "Critical Error"] * 6
            - self.crewdf.at[name, "Task Bozo"] * 8
        )
        self.crewdf.at[name, "Points"] = round(points, 2)

    def calculate_ppg(self, name):
        crew_games = self.crewdf.at[name, "CrewGames"]
        if crew_games > 0:
            self.crewdf.at[name, "PPG"] = round(self.crewdf.at[name, "Points"] / crew_games, 1)

    def calculate_task_avg(self, name):
        crew_games = self.crewdf.at[name, "CrewGames"]
        total_tasks = self.crewdf.at[name, "Total Tasks Completed"]
        if crew_games > 0:
            self.crewdf.at[name, "Avg Task Compl."] = round(total_tasks / crew_games, 1)

    def calculate_throw_rate(self, name):
        """
        Calculates how often a player made critical mistakes.
        """
        #games = self.crewdf.at[name, "CrewGames"]
        alv_last_meeting = self.crewdf.at[name, "Alv Last Meeting"]
        critical_errors = self.crewdf.at[name, "Critical Error"]
        if alv_last_meeting > 0:
            self.crewdf.at[name, "Throw Rate"] = round(critical_errors / alv_last_meeting * 100, 2)
        
    def calculate_win_alv_percentage(self, name):
        total_alv = self.crewdf.at[name, "Win Alv"] + self.crewdf.at[name, "Loss Alv"]
        print(f"Total Alive: {total_alv}")
        if total_alv > 0:
            self.crewdf.at[name, "Win % Alv"] = round(self.crewdf.at[name, "Win Alv"] / total_alv * 100, 2)

    def calculate_cap(self, name):
        cap = (
            self.crewdf.at[name, "Points"] *
            (self.crewdf.at[name, "True VA"] / 100) *
            (self.crewdf.at[name, "Win % Alv"] / 100) *
            ((100 - self.crewdf.at[name, "Throw Rate"]) / 100)
        )
        self.crewdf.at[name, "CAP"] = round(cap, 1)

class ImpostorCalc:
    def __init__(self):
        self.columns = [
            "Name", "PPG", "Kills", "AKPG", "Ejects", "Kill Farmer",
            "Wins", "Losses", "ImpGames", "Win % Imp", "CAP", "Points"
        ]
        self.impdf = pd.DataFrame(columns=self.columns)
        self.impdf.set_index("Name", inplace=True)

    def getImpGames(self, df):
        """
        Accepts a single-row DataFrame and updates impostor stats.
        """
        if df.empty:
            return

        row = df.iloc[0]
        name = str(row["Name"]).strip()
        role = str(row["Role"]).strip().upper()

        # Only process if the player is an Impostor
        if role != "IMPOSTER":
            return

        # Ensure player's row exists
        if name not in self.impdf.index:
            self._initialize_player_row(name)

        # Process all relevant updates
        self._increment_game_count(name)
        self._update_kills(name, row)
        self._update_ejects(name, row)
        self._update_win_loss(name, row)
        self._update_points(name)
        self._calculate_derived_stats(name)
        self._calculate_cap(name)

    def _initialize_player_row(self, name):
        """Initialize a player's row in the DataFrame with default values."""
        self.impdf.loc[name] = {col: 0 for col in self.impdf.columns}

    def _increment_game_count(self, name):
        self.impdf.at[name, "ImpGames"] += 1

    def _update_kills(self, name, row):
        kills = row["Kills"]
        self.impdf.at[name, "Kills"] += kills
        if kills >= 4:
            self.impdf.at[name, "Kill Farmer"] += 1

    def _update_ejects(self, name, row):
        self.impdf.at[name, "Ejects"] += row["Number of Crewmates Ejected (Imposter Only)"]

    def _update_win_loss(self, name, row):
        win_type = str(row["Win Type"]).strip().lower()
        if win_type in ["impostorwin", "timesup", "reactorwin"]:
            self.impdf.at[name, "Wins"] += 1
        else:
            self.impdf.at[name, "Losses"] += 1

    def _update_points(self, name):
        points = (
            self.impdf.at[name, "Wins"] * 5
            - self.impdf.at[name, "Losses"] * 0.5
            + self.impdf.at[name, "Kills"] * 0.25
            + self.impdf.at[name, "Ejects"] * 0.25
        )
        self.impdf.at[name, "Points"] = round(points, 2)

    def _calculate_derived_stats(self, name):
        games = self.impdf.at[name, "ImpGames"]

        if games > 0:
            self.impdf.at[name, "PPG"] = round(self.impdf.at[name, "Points"] / games, 1)
            self.impdf.at[name, "AKPG"] = round(self.impdf.at[name, "Kills"] / games, 1)
            self.impdf.at[name, "Win % Imp"] = round(self.impdf.at[name, "Wins"] / games * 100, 2)
    
    def _calculate_cap(self, name):
        cap = (
            self.impdf.at[name, "Points"] *
            self.impdf.at[name, "Win % Imp"] / 100
        )
        self.impdf.at[name, "CAP"] = round(cap, 1)
    



class GameManager:
    def __init__(self):
        self.games = []
    
    def add_game(self, df):
        game = Game(df)
        self.games.append()

class Game:
    def __init__(self, df):
        self.players = []
        self.starttime = datetime.now()
        self.imps = []
        self.crew = []

# class ImpostorCalc:
#     def __init__(self):
#         self.columns = [
#             "Name", "PPG Imp", "Kills", "AKPG", "Ejects", "Kill Farmer", "Wins", 
#             "Losses", "ImpGames", "Win % Imp", "CAP",
#         ]
#         self.impdf = pd.DataFrame(columns=self.columns)
#         self.impdf.set_index("Name", inplace=True)

#     def getImpGames(self, df):
#         name = str(df["Name"]).strip()
#         role = str(df["Role"]).strip().upper()

#         # Only process if the player is an Impostor
#         if role != "IMPOSTER":
#             return
        
#         # Ensure player's row exists in the dataframe
#         if name not in self.impdf.index:
#             self._initialize_player_row(name)
        
#         # Increment Impostor game count
#         self._increment_game_stats(name, df)
        
#         # Update Kill and Eject statistics
#         self._update_kills(name, df)
#         self._update_ejects(name, df)
        
#         # Update win/loss stats based on game result
#         self._update_win_loss(name, df)
        
#         # Calculate points and update related stats (PPG, AKPG, Win % Imp)
#         self._update_points(name)
#         self._calculate_derived_stats(name)

#     def _initialize_player_row(self, name):
#         """Initialize a player's row in the DataFrame with default values."""
#         default_row = {col: 0 for col in self.impdf.columns}
#         self.impdf.loc[name] = default_row

#     def _increment_game_stats(self, name, df):
#         """Increment game-related stats."""
#         self.impdf.at[name, "ImpGames"] += 1

#     def _update_kills(self, name, df):
#         """Update the number of kills for the Impostor."""
#         self.impdf.at[name, "Kills"] += df["Kills"]
#         if df["Kills"] >= 4:
#             self.impdf.at[name, "Kill Farmer"] += 1

#     def _update_ejects(self, name, df):
#         """Update the number of crewmates ejected by the Impostor."""
#         self.impdf.at[name, "Ejects"] += df["Number of Crewmates Ejected (Imposter Only)"]

#     def _update_win_loss(self, name, df):
#         """Update the win/loss record for the Impostor based on the game result."""
#         win_type = str(df["Win Type"]).strip().lower()
#         if win_type in ["impostorwin", "timesup", "reactorwin"]:
#             self.impdf.at[name, "Wins"] += 1
#         else:
#             self.impdf.at[name, "Losses"] += 1

#     def _update_points(self, name):
#         """Calculate the points for the Impostor."""
#         points = (
#             self.impdf.at[name, "Wins"] * 5 -
#             self.impdf.at[name, "Losses"] * 0.5 +
#             self.impdf.at[name, "Kills"] * 0.25 +
#             self.impdf.at[name, "Ejects"] * 0.25
#         )
#         self.impdf.at[name, "Points"] = round(points, 2)

#     def _calculate_derived_stats(self, name):
#         """Calculate derived statistics such as PPG, AKPG, and Win % Imp."""
#         imp_games = self.impdf.at[name, "ImpGames"]

#         # Calculate PPG (Points Per Game)
#         if imp_games > 0:
#             self.impdf.at[name, "PPG Imp"] = round(self.impdf.at[name, "Points"] / imp_games, 2)
        
#         # Calculate AKPG (Average Kills Per Game)
#         if imp_games > 0:
#             self.impdf.at[name, "AKPG"] = round(self.impdf.at[name, "Kills"] / imp_games, 2)
        
#         # Calculate Win Percentage
#         if imp_games > 0:
#             self.impdf.at[name, "Win % Imp"] = round(self.impdf.at[name, "Wins"] / imp_games * 100, 2)

def to_bool(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() == "true"
    return bool(val)
# class ImpostorCalc:
#     def __init__(self):
#         self.columns = [
#             "Name",
#             "PPG Imp",
#             "Kills",
#             "AKPG",
#             "Ejects",
#             "Kill Farmer",
#             "Wins",
#             "Losses",
#             "ImpGames",
#             "Win % Imp",
#             "CAP",
#         ]
#         self.impdf = pd.DataFrame(columns=self.columns)
#         self.impdf.set_index("Name",inplace=True)

#     def getImpGames(self, df):
#         row = df
        
#         role = str(row["Role"]).strip().upper()
#         if role != "IMPOSTER":
#             return
        
#         name = row["Name"]
#         # If player's row is not in the crew dataframe, initialize it using a dictionary.
#         if name not in self.impdf.index:
#             default_row = {col: 0 for col in self.impdf.columns}
#             self.impdf.loc[name] = default_row
        
#         self.impdf.at[name, "ImpGames"] += 1
#         self.impdf.at[name, "Kills"] += row["Kills"]

#         win_type = str(row["Win Type"]).strip().lower()

#         if (win_type in ["impostorwin", "timesup", "reactorwin"]):
#             self.impdf.at[name, "Wins"] += 1
#         else:
#             self.impdf.at[name, "Losses"] += 1
        
#         if (row["Kills"] >= 4):
#             self.impdf.at[name, "Kill Farmer"]
        
#         #print(row["Number of Crewmates Ejected (Imposter Only)"], type(row["Number of Crewmates Ejected (Imposter Only)"]))
#         self.impdf.at[name, "Ejects"] += row["Number of Crewmates Ejected (Imposter Only)"]

#         points = (
#             self.impdf.at[name, "Wins"] * 5 -
#             self.impdf.at[name, "Losses"] * 0.5 +
#             self.impdf.at[name, "Kills"] * 0.25 +
#             self.impdf.at[name, "Ejects"] * 0.25
#         )
#         self.impdf.at[name, "Points"] = round(points, 2)
        
#         # PPG
#         imp_games = self.impdf.at[name, "ImpGames"]
#         if imp_games > 0:
#             self.impdf.at[name, "PPG Imp"] = round(
#                 self.impdf.at[name, "Points"] / imp_games, 2
#             )
#         # AKPG
#         if imp_games > 0:
#             self.impdf.at[name, "AKPG"] = self.impdf.at[name, "Kills"] / imp_games
#             self.impdf.at[name, "AKPG"] = round(self.impdf.at[name, "AKPG"], 2)
        
#         # Win %
#         if imp_games > 0:
#             self.impdf.at[name, "Win % Imp"] = round(
#                 self.impdf.at[name, "Wins"] / imp_games * 100, 2)
        