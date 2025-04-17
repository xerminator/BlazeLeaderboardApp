import tkinter as tk
import time
from pathlib import Path
from tkinter import ttk, filedialog
import pandas as pd
import StatsCalc
from datetime import datetime
import numpy as np
import dateparser
import traceback

class LeaderboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LeaderboardApp")
        self.geometry("512x512")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.main_page = MainPage(notebook, self)
        self.games_page = GamesPage(notebook, self)
        self.discarded_page = DiscardPage(notebook, self)

        notebook.add(self.main_page, text="Main")
        notebook.add(self.games_page, text="Games")
        notebook.add(self.discarded_page, text="Discarded")

        self.notebook = notebook
    
    def update_pages(self, folder_path, discard_word):
        # Pass the selected folder path and discard word to the pages
        self.games_page.update_listbox(folder_path, discard_word, include_discarded=False)
        self.discarded_page.update_listbox(folder_path, discard_word, include_discarded=True)
        self.games_page.update_label(folder_path)
        self.discarded_page.update_label(folder_path, discard_word)
    
    def retrieve_games(self):
        #return self.games_page.get_listbox_items()
        listbox_items = [item[0] for item in self.games_page.get_listbox_items()]
        #print(listbox_items)
        return listbox_items

    def calculate(self, folder_path):
        self.main_page.reset_progress()
        Calculate(folder_path, self.retrieve_games(), self.update_progress, self.main_page.crewentry_lb_games.get(), self.main_page.impentry_lb_games.get())
    
    def update_progress(self, value, maximum):
        self.main_page.update_progress(value, maximum)

        if value == maximum:
            #self.main_page.update_progresslabel()
            self.main_page.progresslabel.config(text="Complete")

class BasePage(tk.Frame):
    def __init__(self, parent, controller, label_text):
        super().__init__(parent)
        self.controller = controller
        self.label = tk.Label(self, text=label_text)
        self.label.pack(padx=10, pady=10)

        # Create a frame to hold the listbox and scrollbar
        listbox_frame = tk.Frame(self)
        listbox_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Create the listbox widget
        self.listbox = tk.Listbox(listbox_frame, height=15, width=60, selectmode="extended")
        self.listbox.pack(side="left", fill="both", expand=True)

        # Create the scrollbar widget and link it to the listbox
        self.scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")  # Ensure fill is 'y' for vertical scroll

        # Link the scrollbar to the listbox
        self.listbox.config(yscrollcommand=self.scrollbar.set)
    
    def update_listbox(self, folder_path, discard_word, include_discarded):
        self.listbox.delete(0, tk.END)

        base_path = Path(folder_path)
        all_files = []

        for file_path in base_path.rglob("*"):
            try:
                if file_path.is_file():
                    filename = file_path.name
                    parsed_date = parse_date_from_filename(filename)
                    if parsed_date:
                        all_files.append((file_path, parsed_date))
            except Exception as e:
                print(f"Skipping file due to error: {e}")



        sorted_files = sorted(all_files, key=lambda x: x[1])
        for path_obj, ctime in sorted_files:
            filename = path_obj.name
            #human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
            human_time = ctime.strftime('%Y-%m-%d %H:%M:%S')
            if (include_discarded and discard_word.lower() in filename.lower()) or \
               (not include_discarded and discard_word.lower() not in filename.lower()):
                self.listbox.insert(tk.END, (filename , human_time))
    
    def update_label(self, folder_path, is_discard_page=False):
        if is_discard_page:
            # For DiscardPage, include discard_word in the label
            self.label.config(text=f"Discarded games in: {folder_path}")
        else:
            # For GamesPage, only update with folder path
            self.label.config(text=f"Games in: {folder_path}")

    def add_item_to_listbox_sorted(self, item):
        items = list(self.listbox.get(0, tk.END))
        items.append(item)
        items_sorted = sorted(items, key=lambda x: x[1])

        self.listbox.delete(0, tk.END)
        for item in items_sorted:
            self.listbox.insert(tk.END, item)

    
    
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.label = tk.Label(self, text="No Folder Selected")
        self.label.pack(padx=10, pady=10)
        self.folder_path = ""

        open_dir_btn = tk.Button(
            self,
            text="Select Folder",
            command=self.open_dir_dialog
        )
        crewentry_frame = tk.Frame(self)
        crewentry_frame.pack(pady=10)

        impentry_frame = tk.Frame(self)
        impentry_frame.pack(pady=10)

        crewentry_label = tk.Label(crewentry_frame, text="Leaderboard Crew Games: ")
        crewentry_label.pack(side="left")

        self.crewentry_lb_games = tk.Entry(crewentry_frame)
        self.crewentry_lb_games.insert(0, "50")
        self.crewentry_lb_games.pack(side="left")

        impentry_label = tk.Label(impentry_frame, text="Leaderboard Imp Games: ")
        impentry_label.pack(side="left")

        self.impentry_lb_games = tk.Entry(impentry_frame)
        self.impentry_lb_games.insert(0, "50")
        self.impentry_lb_games.pack(side="left")

        open_dir_btn.pack(pady=10)

        calc_btn = tk.Button(
            self,
            text="Calculate",
            command=self.calc
        )
        calc_btn.pack(pady=10)

        # Create a Progressbar widget
        self.progresslabel = tk.Label(self, text="Progress")
        self.progresslabel.pack(padx=10, pady=10)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(padx=10, pady=20)

        

    def update_progress(self, value, maximum):
        """ Update the progress bar """
        self.progress["maximum"] = maximum
        self.progress["value"] = value
        self.update_idletasks()

    def reset_progress(self):
        """ Reset the progress bar """
        self.progress["value"] = 0
        self.progresslabel.config(text="Processing Files...")

    def calc(self):
        self.controller.calculate(self.folder_path)

    def open_dir_dialog(self):
        folder_path = filedialog.askdirectory(
            title="Select a Folder"
        )
        if folder_path:
            self.folder_path = folder_path
            print(f"Selected Folder: {folder_path}")
            self.label.config(text=f"{folder_path}")
            discard_word = "Disconnect"
            # Update the pages with the folder and discard word
            self.controller.update_pages(folder_path, discard_word)

class GamesPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "No Games Found")
        discard_btn = tk.Button(
            self,
            text="Discard Selected",
            command=self.move_to_discard
        )
        discard_btn.pack(pady=10)

    def update_listbox(self, folder_path, discard_word, include_discarded=False):
        # Call the base class update_listbox method, which will handle both filtering and displaying
        super().update_listbox(folder_path, discard_word, include_discarded=False)

    def move_to_discard(self):
        selected_items = self.listbox.curselection()
        if selected_items:
            selected_items = sorted(selected_items, reverse=True)
            for item_index in selected_items:
                item = self.listbox.get(item_index)
                self.controller.discarded_page.add_item_to_listbox_sorted(item)
                self.listbox.delete(item_index)

    def get_listbox_items(self):
        return self.listbox.get(0, tk.END)

class DiscardPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "No Discards Found")
        self.restore_button = tk.Button(self, text="Restore Selected", command=self.restore_to_games)
        self.restore_button.pack(pady=10)

    def restore_to_games(self):
        # Get selected items from the listbox
        selected_items = self.listbox.curselection()
        if selected_items:
            # Move selected items to GamesPage listbox
            selected_items = sorted(selected_items, reverse=True)
            for item_index in selected_items:
                item = self.listbox.get(item_index)
                # Add the item to the GamesPage listbox (keeping it sorted)
                self.controller.games_page.add_item_to_listbox_sorted(item)
                # Remove the item from the DiscardPage listbox
                self.listbox.delete(item_index)

    def update_listbox(self, folder_path, discard_word, include_discarded=True):
        # Call the base class update_listbox method, which will handle both filtering and displaying
        super().update_listbox(folder_path, discard_word, include_discarded=True)

def Calculate(folder_path, games, progress_callback=None, amountcrew="50", amountimp="50"):
    amountcrew = int(amountcrew)
    amountimp = int(amountimp)
    base_path = Path(folder_path)
    columns = [
        "Name", "Role", "Disconnected", "Correct Votes", "Incorrect Votes", 
        "Correct Ejects", "Incorrect Ejects", "Tasks Completed", "Tasks Total", 
        "Alive at Last Meeting", "First Two Victims R1", 
        "Number of Crewmates Ejected (Imposter Only)", "Critical Meeting Error", 
        "Kills", "Survivability", "Win Type"
    ]

    df = pd.DataFrame(columns=columns)
    print(f"Initialization Df: {df}")

    all_files = get_sorted_files(base_path)
    total_files = len(all_files)
    
    if progress_callback:
        progress_callback(0, total_files)

    crewStats = StatsCalc.CrewmateCalc()
    impStats = StatsCalc.ImpostorCalc()
    lbStats = StatsCalc.LeaderbordCalc()
    processed_files_allstats = set()
    processed_files_lb = set()

    rows = []
    current_progress = 0

    for idx, (file_path, _) in enumerate(all_files):
        print(f"Iterating: {Path(file_path).name}")

        if Path(file_path).name not in games:
            print(f"{Path(file_path).name} is not in games, skipping")
            if progress_callback:
                current_progress += 1
                progress_callback(current_progress, total_files * 2)
                continue

        try:
            print(f"Trying to read file: {file_path}")
            df_file = pd.read_csv(file_path)
            df_file.columns = df_file.columns.str.strip()

            #print(f"Columns in file: {df_file.columns}")

            source_name = Path(file_path).stem
            df_file['Source.Name'] = source_name

            for _, values in df_file.iterrows():
                #print(values)

                processed_row = process_single_row(values, crewStats, impStats)
                #print(f"Processed row: {processed_row}")

                if not processed_row.empty:
                    rows.append(processed_row)
            processed_files_allstats.add(Path(file_path).name)
            current_progress += 1
        except Exception as e:
            print(f"Iterating Error: {e}")
            print(f"File: {Path(file_path).name}")
            traceback.print_exc()
            
        if progress_callback:
            progress_callback(current_progress, total_files * 2)

    for idx, (file_path, _) in enumerate(reversed(all_files)):
        print(f"Reverse Iterating: {Path(file_path).name}")

        if Path(file_path).name not in games:
            print(f"{Path(file_path).name} is not in games, skipping")
            if progress_callback:
                current_progress += 1
                progress_callback(current_progress, total_files * 2)
                continue
        try:

            rev_df = pd.read_csv(file_path)
            rev_df.columns = rev_df.columns.str.strip()

            for _, row in rev_df.iterrows():
                lbStats.getLeaderboard(pd.DataFrame([row]), amountcrew, amountimp)
            processed_files_lb.add(Path(file_path).name)
            current_progress += 1

        except Exception as e:
            print(f"Reverse Iterating Error: {e}")
            print(f"File: {Path(file_path).name}")
            traceback.print_exc()
    
        if progress_callback:
            progress_callback(current_progress, total_files * 2)
        
        #print(f"Total rows to concatenate: {len(rows)}")
    if len(rows) > 0:
        #print(f"First 5 rows of data being processed: {rows[:5]}")
        df = pd.concat(rows, ignore_index=True)

    else:
        #print("No rows to concatenate.")
        df = pd.DataFrame(columns=columns)
        df.columns.append("Source.Name")

    df.set_index("Source.Name", inplace=True)
    clean_column_data(df)
    create_report(df, crewStats, impStats, lbStats)
    print(f"allStats Count: {len(processed_files_allstats)} | Leaderboard count: {len(processed_files_lb)}")

    

def get_sorted_files(base_path):
    all_files = []
    for file_path in base_path.rglob("*"):
        if file_path.is_file():
            try:
                parsed_date = parse_date_from_filename(file_path.name)
                if parsed_date:
                    all_files.append((file_path, parsed_date))
            except Exception as e:
                print(f"Skipping file due to error: {e}")
    return sorted(all_files, key=lambda x: x[1])

def parse_date_from_filename(filename):
    try:
        base_part = filename.split(",")[0].strip()
        base_part = base_part.replace("..", ".")
        dt = datetime.strptime(base_part, "%b.%d.%H.%M")
        dt = dt.replace(year=datetime.now().year)
        return dt
    except Exception as e:
        print(f"Error parsing date from filename '{filename}': {e}")
        return None

def process_single_row(row, crewStats, impStats):
        row_df = pd.DataFrame([row])
        crewStats.getCrewgames(row_df)
        impStats.getImpGames(row_df)
        return row_df
        

def clean_column_data(df):
    columns_to_clean = ["Disconnected", "Alive at Last Meeting", "First Two Victims R1", "Critical Meeting Error"]
    for column in columns_to_clean:
        df[column] = df[column].apply(lambda x: str(x).upper().strip())

def create_report(df, crewStats, impStats, lbStats):
    crewdf = crewStats.getCrewDf().drop(columns=["Total Tasks Completed"])
    imp_df = impStats.impdf
    lb_df = lbStats.getLeaderboardDf().drop(columns=["Total Tasks Completed"])

    all_stats = pd.merge(
        crewdf,
        imp_df,
        left_index=True,
        right_index=True,
        how='outer',
        suffixes=(" (crew)", " (imp)")
    ).fillna(0)

    all_stats["Games"] = all_stats["CrewGames"] + all_stats["ImpGames"]
    all_stats["Final CAP"] = all_stats["CAP (crew)"] + all_stats["CAP (imp)"]

    crewexclude_cols = ["Avg Task Compl.","CAP", "PPG"]
    impexclude_cols = ["CAP", "PPG", "AKPG"]
    allexclude_cols = ["PPG (crew)", "PPG (imp)", "AKPG", "CAP (crew)", "CAP (imp)", "Avg Task Compl.", "Final CAP"]
    lbexclude_cols = ["CrewPPG", "ImpPPG", "AKPG", "CrewCAP", "ImpCAP", "Avg Task Compl.", "Final CAP"]

    crewnumeric_cols = crewdf.select_dtypes(include=[np.number]).columns.difference(crewexclude_cols)
    impnumeric_cols = imp_df.select_dtypes(include=[np.number]).columns.difference(impexclude_cols)
    allnumeric_cols = all_stats.select_dtypes(include=[np.number]).columns.difference(allexclude_cols)
    lbnumeric_cols = lb_df.select_dtypes(include=[np.number]).columns.difference(lbexclude_cols)

    crewdf[crewnumeric_cols] = np.floor(crewdf[crewnumeric_cols]).astype(int)
    imp_df[impnumeric_cols] = np.floor(imp_df[impnumeric_cols]).astype(int)
    all_stats[allnumeric_cols] = np.floor(all_stats[allnumeric_cols]).astype(int)
    lb_df[lbnumeric_cols] = np.floor(lb_df[lbnumeric_cols]).astype(int)

    crew_round_cols = [col for col in crewexclude_cols if col in crewdf.columns]
    imp_round_cols = [col for col in impexclude_cols if col in imp_df.columns]
    all_round_cols = [col for col in allexclude_cols if col in all_stats.columns]
    lb_round_cols = [col for col in lbexclude_cols if col in lb_df.columns]
   

    crewdf[crew_round_cols] = crewdf[crew_round_cols].round(1)
    imp_df[imp_round_cols] = imp_df[imp_round_cols].round(1)
    all_stats[all_round_cols] = all_stats[all_round_cols].round(1)
    lb_df[lb_round_cols] = lb_df[lb_round_cols].round(1)



    excel_file = f'{Path.cwd()}/calcs/leaderboard.xlsx'
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="season13", index="Source.Name")
        crewdf.to_excel(writer, sheet_name="crewstats", index="Name")
        imp_df.to_excel(writer, sheet_name="impstats", index="Name")
        all_stats.to_excel(writer, sheet_name="allstats", index="Name")
        lb_df.to_excel(writer, sheet_name="leaderboard", index="Final CAP")
        add_autofilter(writer, crewdf, imp_df, all_stats, lb_df)


def add_autofilter(writer, crewdf, imp_df, all_stats, lb_df):
    crewworksheet = writer.sheets["crewstats"]
    impworksheet = writer.sheets["impstats"]
    allworksheet = writer.sheets["allstats"]
    lbworksheet = writer.sheets["leaderboard"]

    # print(crewdf.columns)
    # print(imp_df.columns)
    # print(all_stats.columns)

    crewworksheet.autofilter(0, 0, crewdf.shape[0], crewdf.shape[1])
    impworksheet.autofilter(0, 0, imp_df.shape[0], imp_df.shape[1])
    allworksheet.autofilter(0, 0, all_stats.shape[0], all_stats.shape[1])
    lbworksheet.autofilter(0, 0, lb_df.shape[0], lb_df.shape[1])

def parse_date_from_filename(filename):
    try:
        # Step 1: Extract the date portion (before the first comma)
        date_str = filename.split(",")[0].strip()

        # Step 2: Replace '..' with '.' and normalize spacing
        date_str = date_str.replace("..", ".").replace("_", " ").strip()

        # Step 3: Convert things like 'apr.01.07.51' -> 'apr 01 07:51'
        # Match pattern: month.day.hour.minute
        parts = date_str.split('.')
        if len(parts) >= 4:
            # Format as: 'month day hour:minute' -> easier for dateparser
            date_str = f"{parts[0]} {parts[1]} {parts[2]}:{parts[3]}"

        # Step 4: Parse using dateparser
        dt = dateparser.parse(date_str, settings={
            'PREFER_DATES_FROM': 'past',
            'RELATIVE_BASE': datetime.now(),
            'DATE_ORDER': 'DMY'
        })

        return dt

    except Exception as e:
        print(f"[Error parsing date] '{filename}': {e}")
        return None