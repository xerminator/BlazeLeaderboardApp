import leaderboardapp
from pathlib import Path
import sys   

calc_path = Path(f"{Path.cwd()}/calcs")
calc_path.mkdir(exist_ok=True, parents=True)

# Determine the path to the theme file
if getattr(sys, 'frozen', False):  # If running as a bundled executable
    theme_path = Path(sys._MEIPASS) / 'themes' / 'azure' / 'azure.tcl'
else:  # If running as a script
    theme_path = Path.cwd() / 'themes' / 'azure' / 'azure.tcl'

if __name__ == "__main__":
    testObj = leaderboardapp.LeaderboardApp()
    testObj.tk.call("source", str(theme_path))
    testObj.tk.call("set_theme", "dark")
    testObj.mainloop()