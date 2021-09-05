from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import conformer_search_workflow as cs_workflow

# Global Variables
# tkinter doesn't work without that :/
CS_folderPath = ""


# Select folder path for conformer search workflow
def select_CS_folder_path(CS_Var):

    # Access global variable
    global CS_folderPath

    # Use file explorer to find correct folder and get its path
    CS_folderPath = filedialog.askdirectory()

    # set path variable to selected path
    CS_Var.set(CS_folderPath)


# Input validation for entry windows
def testVal(inStr, acttyp):
    if acttyp == '1': # insert mode
        if not inStr.isdigit() and not "." in inStr and not "," in inStr:
            return False

    return True # valid input


# setup GUI
def GUI_window():
    
    # initialize
    GUI = Tk()

    # set window title and disable resizing
    GUI.title("QMC Data Processor")
    GUI.resizable(False, False)

    # prepare tab window
    tab_parent = ttk.Notebook(GUI)

    # add two tabs for different workflows
    tab_ConformerSearch = ttk.Frame(tab_parent)
    tab_CircularDichroism = ttk.Frame(tab_parent)

    # give name to each tab
    tab_parent.add(tab_ConformerSearch, text="Conformer Search")
    tab_parent.add(tab_CircularDichroism, text="Circular Dichroism")

    # create grid for elements
    tab_parent.grid()

    # String variable for storing path to folder selected for extracting CD data
    CS_path = StringVar()

    # Button for selecting path to folder for CS analysis
    CS_select_button = Button(tab_ConformerSearch,
                              text="Select folder",
                              height="2",
                              width="30",
                              command=lambda: select_CS_folder_path(CS_path),
                              font=("Calibri", 12, 'bold'))

    # Place button on grid
    CS_select_button.grid(row=0,
                          column=0,
                          padx=40,
                          pady=20,
                          columnspan=3,
                          sticky=W+E+N+S)

    # Add label that will display selected path
    filePathLabel = Message(tab_ConformerSearch,
                            textvariable=CS_path,
                            font=("Calibri", 10, "bold"),
                            width=350)

    # Place Label on the gird
    filePathLabel.grid(row=1,
                       column=0,
                       pady=0,
                       columnspan=3,
                       sticky=W+E+N+S)

     # Temperature label
    temperature_label = Label(tab_ConformerSearch,
                              text="Temperature",
                              font=("Calibri", 12, 'bold'))

    # Place temperature label on a grid
    temperature_label.grid(row=2,
                           column=0,
                           padx=0,
                           sticky=E)

    # Temperature entry
    CS_temperature_entry = Entry(tab_ConformerSearch,
                                 width=10,
                                 justify="center",
                                 validate='key',
                                 font=("Calibri", 12, 'bold'))

    # set default value for temperature (25 degrees Celsius or 298.15 K)
    CS_temperature_entry.delete(0, END)
    CS_temperature_entry.insert(0, "298.15")

    # set up validation method to validate user input
    CS_temperature_entry["validatecommand"] = (CS_temperature_entry.register(testVal), "%P", "%d")

    # Place temperature entry on a grid
    CS_temperature_entry.grid(row=2,
                              column=1,
                              padx=0,
                              pady=10,
                              sticky=E)

    # Temperature unit label
    temperature_unit_label = Label(tab_ConformerSearch,
                                   text="K",
                                   font=("Calibri", 12, 'bold'))

    # Place temperatur unit label on a grid
    temperature_unit_label.grid(row=2,
                           column=2,
                           padx=0,
                           sticky=W)

    # Energy limit label
    energyLimit_label = Label(tab_ConformerSearch,
                              text="Energy limit",
                              font=("Calibri", 12, 'bold'))

    # Place nergy limit label on a gird
    energyLimit_label.grid(row=3,
                           column=0,
                           padx=0,
                           sticky=E)

    # Energy limit entry box
    CS_EnergyLimit_entry = Entry(tab_ConformerSearch,
                                 width=10,
                                 justify="center",
                                 validate='key',
                                 font=("Calibri", 12, 'bold'))

    # set default value for energy limit (2 kcal)
    CS_EnergyLimit_entry.delete(0, END)
    CS_EnergyLimit_entry.insert(0, "2")

    # Make sure that only digits, comma and dot can be used as input
    CS_EnergyLimit_entry["validatecommand"] = (CS_EnergyLimit_entry.register(testVal), "%P", "%d")

    # Place energy limit entry box on a grid
    CS_EnergyLimit_entry.grid(row=3,
                              column=1,
                              padx=0,
                              pady=0,
                              sticky=E)

    # Energy limit label
    CS_Energy_Unit_label = Label(tab_ConformerSearch,
                                 text="kcal/mol",
                                 font=("Calibri", 12, 'bold'))

    # Place energy limit label on a grid
    CS_Energy_Unit_label.grid(row=3,
                                column=2,
                                padx=0,
                                sticky=W)

    # This button starts conformer search analysis
    CS_analysis_button = Button(tab_ConformerSearch,
                                text="Conformers energy analysis",
                                height="2",
                                width="30",
                                command=lambda: cs_workflow.conformer_search_workflow(),
                                font=("Calibri", 12, 'bold'))

    # Place button on the gird
    CS_analysis_button.grid(row=4,
                            column=0,
                            padx=40,
                            pady=20,
                            columnspan=3,
                            sticky=W+E+N+S)

    # loop/refresh
    GUI.mainloop()


if __name__== "__main__":
    GUI_window()