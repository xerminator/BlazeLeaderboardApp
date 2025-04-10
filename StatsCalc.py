import pandas as pd

# class StatsCalc:
#     def __init__(self, df: pd.DataFrame):
#         self.df = df
    
class CrewmateCalc:
    def __init__ (self):
        self.crewColumns = [
            "Name", 
            "CrewGames", 
            "PPG", 
            "First Round Victim",
            "√ Eject",
            "x Eject",
            "Eject Voting Acc",
            "√ Indv",
            "x Indv",
            "Indv Voting Acc.",
            "TCV",
            "Total V",
            "True VA",
            "Vote Farmer",
            "Critical Error",
            "Alv Last Meeting",
            "Throw Rate",
            "Win Alv",
            "Loss Alv",
            "Task Bozo",
            "Avg Task Compl.",
            "Task Wins",
            "Points",
            "CAP",
            "Total Tasks Completed"
        ]
        self.crewdf = pd.DataFrame(columns=self.crewColumns)
        self.crewdf.set_index("Name",inplace=True)

    def getCrewDf(self):
        return self.crewdf

    def getCrewgames(self, df):
        row = df
        
        role = str(row["Role"]).strip().upper()
        if role != "CREWMATE":
            return
        
        name = row["Name"]
        # If player's row is not in the crew dataframe, initialize it using a dictionary.
        if name not in self.crewdf.index:
            default_row = {col: 0 for col in self.crewdf.columns}
            self.crewdf.loc[name] = default_row
        
        def to_bool(val):
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.strip().lower() == "true"
            return bool(val)

        win_type = str(row["Win Type"]).strip().lower()
        
        self.crewdf.at[name, "CrewGames"] += 1

        if to_bool(row["First Two Victims R1"]):
            self.crewdf.at[name, "First Round Victim"] +=1
        
        correct_ejects = row["Correct Ejects"]
        incorrect_ejects = row["Incorrect Ejects"]
        
        self.crewdf.at[name, "√ Eject"] += correct_ejects
        self.crewdf.at[name, "x Eject"] += incorrect_ejects

        correct_votes = row["Correct Votes"]
        incorrect_votes = row["Incorrect Votes"]

        self.crewdf.at[name, "TCV"] += correct_votes
        total_votes = correct_votes + incorrect_votes
        self.crewdf.at[name, "Total V"] += total_votes

        indv_correct = correct_votes - correct_ejects
        indv_incorrect = incorrect_votes - incorrect_ejects
        self.crewdf.at[name, "√ Indv"] += indv_correct
        self.crewdf.at[name, "x Indv"] += indv_incorrect
    
        if correct_votes >= 4:
            self.crewdf.at[name, "Vote Farmer"] += 1
        
        if to_bool(row["Critical Meeting Error"]):
            self.crewdf.at[name, "Critical Error"] += 1
        

        alv_last_meeting = to_bool(row["Alive at Last Meeting"])
        if alv_last_meeting:
            self.crewdf.at[name, "Alv Last Meeting"] += 1

            if win_type in ["crewmatewin", "taskwin"]:
                self.crewdf.at[name, "Win Alv"] += 1
            elif win_type in ["impostorwin", "timesup", "reactorwin"]:
                self.crewdf.at[name, "Loss Alv"] += 1
            
        alv_count = self.crewdf.at[name, "Alv Last Meeting"]
        if alv_count > 0:
            self.crewdf.at[name, "Throw Rate"] = round(
                self.crewdf.at[name, "Critical Error"] / alv_count * 100, 2
            )

        total_alv = (
            self.crewdf.at[name, "Win Alv"] + self.crewdf.at[name, "Loss Alv"]
        )

        if total_alv > 0:
            self.crewdf.at[name, "Win % Alv"] = round(
                self.crewdf.at[name, "Win Alv"] / total_alv * 100, 2
            )
        
        if win_type == "timesup" and row["Tasks Completed"] < 10:
            self.crewdf.at[name, "Task Bozo"] += 1

        self.crewdf.at[name, "Total Tasks Completed"] += row["Tasks Completed"]
        games = self.crewdf.at[name, "CrewGames"]
        total_tasks = self.crewdf.at[name, "Total Tasks Completed"]
        self.crewdf.at[name, "Avg Task Compl."] = round(total_tasks / games, 2)

        if win_type == "taskwin":
            self.crewdf.at[name, "Task Wins"] += 1
        
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

        # PPG
        crew_games = self.crewdf.at[name, "CrewGames"]
        if crew_games > 0:
            self.crewdf.at[name, "PPG"] = round(
                self.crewdf.at[name, "Points"] / crew_games, 2
            )

        # Accuracy Calculations
        eject_total = self.crewdf.at[name, "√ Eject"] + self.crewdf.at[name, "x Eject"]
        if eject_total > 0:
            self.crewdf.at[name, "Eject Voting Acc"] = round(
                self.crewdf.at[name, "√ Eject"] / eject_total * 100, 2
            )

        indv_total = self.crewdf.at[name, "√ Indv"] + self.crewdf.at[name, "x Indv"]
        if indv_total > 0:
            self.crewdf.at[name, "Indv Voting Acc."] = round(
                self.crewdf.at[name, "√ Indv"] / indv_total * 100, 2
            )

        total_votes = self.crewdf.at[name, "Total V"]
        if total_votes > 0:
            self.crewdf.at[name, "True VA"] = round(
                self.crewdf.at[name, "TCV"] / total_votes * 100, 2
            )