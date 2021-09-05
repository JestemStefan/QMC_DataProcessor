from tkinter import messagebox
import os
import re


# Method to load .out file paths from sleected folder
def load_files(selected_path):

    # Create array of files to analyze
    file_arr = []

    # Look through files in the folder and find files with .out extension
    for file in os.listdir(selected_path):
        if file.endswith(".out"):

            # TODO Add method to check if file content is valid, not just extension
            
            # add file path to return list
            file_arr.append(file)

    return file_arr # returns array of valid file paths


# main method of conformer search. Called by GUI button
def conformer_search_workflow(CS_folder_path, temperature, energy_limit):

    # if no folder path was selected
    if not CS_folder_path:  
        
        # throw an error box informing user about invalid folder path
        messagebox.showerror('Error: Invalid folder path', 'No valid folder path was selected')
        print('No valid folder path was selected')

    else:
        # kiad valid files in the folder
        outfile_arr = load_files(CS_folder_path)

        # throw an error if there is NO files of correct type in folder
        if len(outfile_arr) == 0:
            messagebox.showerror('Error: No valid files in selected folder', 'There is no valid *.out files in selected folder')
            print('There is no valid *.out files in selected folder')

        else:
            pass


if __name__== "__main__":
    conformer_search_workflow()