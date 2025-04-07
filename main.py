import leaderboardapp
from pathlib import Path    

calc_path = Path(f"{Path.cwd()}/calcs")
calc_path.mkdir(exist_ok=True, parents=True)

if __name__ == "__main__":
    testObj = leaderboardapp.LeaderboardApp()
    testObj.mainloop()