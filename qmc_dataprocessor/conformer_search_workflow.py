from tkinter import messagebox
import os
import re


# Method to load .out file paths from selected folder
def load_files(selected_path):

    # Create list of files to analyze
    file_list = []

    # Look through files in the folder and find files with .out extension
    for file in os.listdir(selected_path):
        if file.endswith(".out"):

            # TODO Add method to check if file content is valid, not just extension
            
            # add file path to return list
            file_list.append(file)

    return file_list # returns list of valid file paths


# Method for sorting loaded files based on last number in the name
# because Gaussian number files like that ¯\_(ツ)_/¯

def sort_files(list_to_sort):

    # find all numbers in name and pick up the last number for sorting. 
    list_to_sort.sort(key=lambda x: int(re.findall('\d+', x)[-1]))



# main method of conformer search. Called by GUI button
def conformer_search_workflow(CS_folder_path, temperature, energy_limit):

    # if no folder path was selected
    if not CS_folder_path:  
        
        # throw an error box informing user about invalid folder path
        messagebox.showerror('Error: Invalid folder path', 'No valid folder path was selected')
        print('No valid folder path was selected')

    else:
        # kiad valid files in the folder
        outfile_list = load_files(CS_folder_path)

        # throw an error if there is NO files of correct type in folder
        if len(outfile_list) == 0:
            messagebox.showerror('Error: No valid files in selected folder', 'There is no valid *.out files in selected folder')
            print('There is no valid *.out files in selected folder')

        else:
            # Sort files in files list using natural sort
            sort_files(outfile_list)

            # TODO extract data from files


if __name__== "__main__":
    conformer_search_workflow()