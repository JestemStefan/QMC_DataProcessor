from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import conformer_search_workflow as cs_workflow

# Global Variables
# tkinter doesn't work without that :/
CS_FOLDER_PATH = ""


# Select folder path for conformer search workflow
def select_cs_folder_path(cs_var: StringVar) -> None:
    """
    Opens file explorer and allow folder selection. Updates global variable and returns None.
    """
    
    # Access global variable
    global CS_FOLDER_PATH

    # Use file explorer to find correct folder and get its path
    CS_FOLDER_PATH = filedialog.askdirectory()

    # set path variable to selected path
    cs_var.set(CS_FOLDER_PATH)


# Input validation for entry windows
def test_val(input_str: str, action_type: int) -> bool:
    """
    Validates if user input into GUI entry is a number. Returns True if it is. False otherwise.
    """

    if action_type == '1': # insert mode
        if not input_str.isdigit() and not "." in input_str and not "," in input_str:
            return False

    return True # valid input


# setup GUI
def GUI_window() -> None:
    """
    Creates and update Graphical User Interface. Returns None
    """
    
    # initialize
    GUI = Tk()

    # set window title and disable resizing
    GUI.title("QMC Data Processor")
    GUI.resizable(False, False)

    # prepare tab window
    tab_parent = ttk.Notebook(GUI)

    # add two tabs for different workflows
    tab_conformer_search = ttk.Frame(tab_parent)
    tab_circular_dichroism = ttk.Frame(tab_parent)

    # give name to each tab
    tab_parent.add(tab_conformer_search, text="Conformer Search")
    tab_parent.add(tab_circular_dichroism, text="Circular Dichroism")

    # create grid for elements
    tab_parent.grid()

    # String variable for storing path to folder selected for extracting CD data
    cs_path = StringVar()

    # Button for selecting path to folder for CS analysis
    cs_select_button = Button(tab_conformer_search,
                              text = "Select folder",
                              height = "2",
                              width = "30",
                              # run method to select a path
                              command = lambda: select_cs_folder_path(cs_path),
                              font = ("Calibri", 12, 'bold'))

    # Place button on grid
    cs_select_button.grid(row = 0,
                          column = 0,
                          padx = 40,
                          pady = 20,
                          columnspan = 3,
                          sticky= W+E+N+S)

    # Add label that will display selected path
    file_path_label = Message(tab_conformer_search,
                            textvariable = cs_path,
                            font = ("Calibri", 10, "bold"),
                            width = 350)

    # Place Label on the gird
    file_path_label.grid(row = 1,
                       column = 0,
                       pady = 0,
                       columnspan = 3,
                       sticky = W+E+N+S)

     # Temperature label
    temperature_label = Label(tab_conformer_search,
                              text = "Temperature",
                              font = ("Calibri", 12, 'bold'))

    # Place temperature label on a grid
    temperature_label.grid(row = 2,
                           column = 0,
                           padx = 0,
                           sticky = E)

    # Temperature entry
    cs_temperature_entry = Entry(tab_conformer_search,
                                 width = 10,
                                 justify = "center",
                                 validate = 'key',
                                 font = ("Calibri", 12, 'bold'))

    # set default value for temperature (25 degrees Celsius or 298.15 K)
    cs_temperature_entry.delete(0, END)
    cs_temperature_entry.insert(0, "298.15")

    # set up validation method to validate user input
    cs_temperature_entry["validatecommand"] = (cs_temperature_entry.register(test_val), "%P", "%d")

    # Place temperature entry on a grid
    cs_temperature_entry.grid(row = 2,
                              column = 1,
                              padx = 0,
                              pady = 10,
                              sticky = E)

    # Temperature unit label
    temperature_unit_label = Label(tab_conformer_search,
                                   text = "K",
                                   font = ("Calibri", 12, 'bold'))

    # Place temperature unit label on a grid
    temperature_unit_label.grid(row = 2,
                           column = 2,
                           padx = 0,
                           sticky = W)

    # Energy limit label
    energy_limit_label = Label(tab_conformer_search,
                              text = "Energy limit",
                              font = ("Calibri", 12, 'bold'))

    # Place nergy limit label on a gird
    energy_limit_label.grid(row = 3,
                           column = 0,
                           padx = 0,
                           sticky = E)

    # Energy limit entry box
    cs_energy_limit_entry = Entry(tab_conformer_search,
                                 width = 10,
                                 justify = "center",
                                 validate = 'key',
                                 font = ("Calibri", 12, 'bold'))

    # set default value for energy limit (2 kcal)
    cs_energy_limit_entry.delete(0, END)
    cs_energy_limit_entry.insert(0, "2")

    # Make sure that only digits, comma and dot can be used as input
    cs_energy_limit_entry["validatecommand"] = (cs_energy_limit_entry.register(test_val), "%P", "%d")

    # Place energy limit entry box on a grid
    cs_energy_limit_entry.grid(row = 3,
                              column = 1,
                              padx = 0,
                              pady = 0,
                              sticky = E)

    # Energy limit label
    cs_energy_unit_label = Label(tab_conformer_search,
                                 text = "kcal/mol",
                                 font = ("Calibri", 12, 'bold'))

    # Place energy limit label on a grid
    cs_energy_unit_label.grid(row = 3,
                                column = 2,
                                padx = 0,
                                sticky = W)

    # This button starts conformer search analysis
    cs_analysis_button = Button(tab_conformer_search,
                                text = "Conformers energy analysis",
                                height = "2",
                                width = "30",
                                # run method for conformer search with data from the GUI
                                command = lambda: cs_workflow.conformer_search_workflow(CS_FOLDER_PATH, float(cs_temperature_entry.get()), float(cs_energy_limit_entry.get())),
                                font = ("Calibri", 12, 'bold'))

    # Place button on the gird
    cs_analysis_button.grid(row = 4,
                            column = 0,
                            padx = 40,
                            pady = 20,
                            columnspan = 3,
                            sticky = W+E+N+S)

    # loop/refresh
    GUI.mainloop()


if __name__== "__main__":
    GUI_window()