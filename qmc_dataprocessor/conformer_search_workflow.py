from tkinter import messagebox
import os
import re


# Method to find and load .out files in selected folder
def find_out_files(selected_path: str) -> list:
    """
    Finds all files with .out extension in folder specified by path string. Returns list of filenames as list.
    """

    # Create empty list that will store .out files names
    file_list = []

    # Look through files in the folder specified by path string and find files with .out extension
    for filename in os.listdir(selected_path):
        if filename.endswith(".out"):

            # TODO Add method to check if file content is valid, not just extension
            
            # add filename to return list
            file_list.append(filename)
    
    # returns list of valid filenames
    return file_list


# Method for sorting filenames based on last number in the name
# because Gaussian number files like that ¯\_(ツ)_/¯
# use default sorting for names without numbers
def sort_filenames_by_last_number(list_to_sort: list) -> list:
    """
    Sorts list by last number in filename if possible. Use default sort otherwise. Returns sorted list.
    """

    # Before sorting split list into two list: One with filenames with numbers and one without any.
    list_of_filenames_with_numbers = [x for x in list_to_sort if len(re.findall('\d+', x)) > 0]
    list_of_filenames_no_numbers = [x for x in list_to_sort if len(re.findall('\d+', x)) == 0]

    # if there are filenames with number in them
    if list_of_filenames_with_numbers:

        # find all numbers in filename and pick up the last number as key for sorting. 
        list_of_filenames_with_numbers.sort(key=lambda x: int(re.findall('\d+', x)[-1]))
    
    # sort remaining filenames using default sorting.
    list_of_filenames_no_numbers.sort()

    # merge sorted lists and return new list
    return list_of_filenames_with_numbers + list_of_filenames_no_numbers


# method for creating database with placeholder entires for each file
def create_database_with_placeholder_data(list_of_filenames: list) -> dict:
    """
    Creates database dictionary with placeholder data for each file. Returns database as dictionary.
    """

    # TODO Move to SQL or some other database

    # create empty dict that will be filled with placeholder data and returned
    new_database_dict = {}

    # prepare placeholder data that will be inserted into dict for each file
    empty_data = {"filename" : "no_name",
                  "optimization_calc_done" : False,
                  "frequency_calc_done" : False,
                  "HF_energy" : 0,
                  "HF_relative_energy" : 0,
                  "HF_population" : 0,
                  "dG_energy" : 0,
                  "dG_relative_energy" : 0,
                  "dG_population" : 0,
                  "isUnique" : False,
                  "full_filepath" : "default_path"}

    # fill the database with placeholder data
    for filename in list_of_filenames:
        new_database_dict[filename] = empty_data.copy() # <-- must use .copy() or they will share the same dict by reference

    # return filled database dictionary
    return new_database_dict


def extract_data_from_files(folder_path, filenames_list):
    
    extracted_data = []
    values_hf = []
    values_dG = []
    error_arr = []
    vib_failed_arr = []


# main method of conformer search. Called by GUI button
def conformer_search_workflow(cs_parent_folderpath: str, temperature: float, energy_limit: float) -> None:
    """
    Performs analysis of data from conformer search calculations in specified parameters. Returns None.
    """

    # if no folder path was selected
    if not cs_parent_folderpath:  
        
        # throw an error message box informing user about invalid folder path
        messagebox.showerror('Error: Invalid folder path', 'No valid folder path was selected')
        print('No valid folder path was selected')

    else: 
        # find and loads filenames of valid files in the specified folder
        outfile_list = find_out_files(cs_parent_folderpath)

        # throw an error message box if there is NO files of correct type in folder
        if len(outfile_list):
            messagebox.showerror('Error: No valid files in selected folder', 'There is no valid *.out files in selected folder')
            print('There is no valid *.out files in selected folder')

        else:
            # Sort filenames in outfile_list using natural sort
            outfile_list = sort_filenames_by_last_number(outfile_list)

            # initialize database that will store data from files
            cs_database = create_database_with_placeholder_data(outfile_list)
            
            # TODO extract data from files
            # TODO multithreaded? :eyes:
            extract_data_from_files(cs_parent_folderpath, outfile_list)
            


if __name__== "__main__":
    conformer_search_workflow()