import leaderboardapp
from pathlib import Path    

calc_path = Path(f"{Path.cwd()}/calcs")
calc_path.mkdir(exist_ok=True, parents=True)

if __name__ == "__main__":
    testObj = leaderboardapp.LeaderboardApp()
    testObj.tk.call("source", f"{Path.cwd()}/themes/azure/azure.tcl")
    testObj.tk.call("set_theme", "dark")
    testObj.mainloop()