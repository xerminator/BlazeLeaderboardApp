import tkinter as tk
import time
from pathlib import Path
from tkinter import ttk, filedialog
import pandas as pd
import StatsCalc

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
        Calculate(folder_path, self.retrieve_games(), self.update_progress)
    
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
            if file_path.is_file():
                try:
                    created = file_path.stat().st_ctime
                    all_files.append((file_path, created))
                except Exception as e:
                    print(f"Skipping file due to error: {e}")
        sorted_files = sorted(all_files, key=lambda x: x[1])
        for path_obj, ctime in sorted_files:
            filename = path_obj.name
            human_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
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


def Calculate(folder_path, games, progress_callback=None):
    #print(games)
    base_path = Path(folder_path)

    columns = ["Name", "Role", "Disconnected", "Correct Votes", "Incorrect Votes", 
           "Correct Ejects", "Incorrect Ejects", "Tasks Completed", "Tasks Total", 
           "Alive at Last Meeting", "First Two Victims R1", 
           "Number of Crewmates Ejected (Imposter Only)", "Critical Meeting Error", 
           "Kills", "Survivability", "Win Type"]

    

    df = pd.DataFrame(columns=columns)
    #crewStats = StatsCalc.CrewmateCalc()


    base_path = Path(folder_path)
    all_files = []

    for file_path in base_path.rglob("*"):
        if file_path.is_file():
            try:
                created = file_path.stat().st_ctime
                all_files.append((file_path, created))
            except Exception as e:
                print(f"Skipping file due to error: {e}")
    sorted_files = sorted(all_files, key=lambda x: x[1])
    rows = []

    total_files = len(sorted_files)
    if progress_callback:
        progress_callback(0, total_files)

    crewStats = StatsCalc.CrewmateCalc()
    #print(games)
    for idx, file in enumerate(sorted_files):
        filename = Path(file[0]).name
        #print(f"{filename} \n")
        if filename not in games:
            continue
        try:
            #print(file[0])
            df_file = pd.read_csv(file[0])
            df_file.columns = df_file.columns.str.strip()


            for _, row in df_file.iterrows():
                row['Source.Name'] = Path(file[0]).stem
                row_df = pd.DataFrame([row])
                rows.append(row_df)
                crewStats.getCrewgames(row)
            df = pd.concat(rows, ignore_index=True)
            
            #print(f"Columns in {filename}:")
            #print(df_file.columns.tolist())
            df['Disconnected'] = df['Disconnected'].apply(lambda x: str(x).upper().strip())
            df['Alive at Last Meeting'] = df['Alive at Last Meeting'].apply(lambda x: str(x).upper().strip())
            df['First Two Victims R1'] = df['First Two Victims R1'].apply(lambda x: str(x).upper().strip())
            df['Critical Meeting Error'] = df['Critical Meeting Error'].apply(lambda x: str(x).upper().strip())
            # df['Disconnected'] = df['Disconnected'].str.upper()
            # df['Alive At Last Meeting'] = df['Alive At Last Meeting'].str.upper()
            # df['First Two Victims R1'] = df['First Two Victims R1'].str.upper()
            # df['Critical Meeting Error'] = df['Critical Meeting Error'].str.upper()
            df.set_index('Source.Name', inplace=True)
        except Exception as e:
            print(f"Error: {e} \n File: {filename}")
        if progress_callback:
            progress_callback(idx + 1, total_files)
    
    excel_file = f'{Path.cwd()}/calcs/leaderboard.xlsx'

    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="season13", index="Source.Name")
        crewdf = crewStats.getCrewDf().drop(columns=["Total Tasks Completed"])
        crewdf.to_excel(writer, sheet_name="stats", index="Name")

        worksheet = writer.sheets["stats"]

        max_row = crewdf.shape[0]
        max_col = crewdf.shape[1] - 1

        worksheet.autofilter(0, 0, max_row, max_col)

    if progress_callback:
        progress_callback(total_files, total_files)
        