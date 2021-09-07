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

    # check if all names contain at least one number
    # TODO It should check if all names are identical, except number at the end. But this is user mistake if names are mixed...
    list_of_filenames_with_digits = [x for x in list_to_sort if len(re.findall('\d+', x)) > 0]
    list_of_filesnames_no_digits = [x for x in list_to_sort if len(re.findall('\d+', x)) == 0]
    

    if len(list_of_filenames_with_digits) > 0:

        # find all numbers in name and pick up the last number for sorting. 
        list_of_filenames_with_digits.sort(key=lambda x: int(re.findall('\d+', x)[-1]))
    
    list_of_filesnames_no_digits.sort()

    # not necessary, but I like it this way
    return list_of_filenames_with_digits + list_of_filesnames_no_digits


# method to create placeholder entires in database
def create_empty_database(filepath_list: list) -> dict:

    # create empty dict that will be returned
    new_database_dict = {}

    # prepare placeholder data that will be used for each file
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
    for file in filepath_list:
        new_database_dict[file] = empty_data.copy() #<-- must use .copy or they will share the same dict

    return new_database_dict


def extract_data_from_files(folder_path, filepath_list):
    pass


# main method of conformer search. Called by GUI button
def conformer_search_workflow(CS_folder_path, temperature, energy_limit):

    # if no folder path was selected
    if not CS_folder_path:  
        
        # throw an error box informing user about invalid folder path
        messagebox.showerror('Error: Invalid folder path', 'No valid folder path was selected')
        print('No valid folder path was selected')

    else:
        # load valid files in the folder
        outfile_list = load_files(CS_folder_path)

        # throw an error if there is NO files of correct type in folder
        if len(outfile_list) == 0:
            messagebox.showerror('Error: No valid files in selected folder', 'There is no valid *.out files in selected folder')
            print('There is no valid *.out files in selected folder')

        else:
            # Sort files in outfile_list using natural sort
            outfile_list = sort_files(outfile_list)

            # initialize database that will store data from files
            CS_database = create_empty_database(outfile_list)

            # FOR DEBUGGING PURPOSE #
            for entry in CS_database:
                print([entry, CS_database[entry]])
            
            # TODO extract data from files
            # TODO multithreaded? :eyes:
            extract_data_from_files(CS_folder_path, outfile_list)
            


if __name__== "__main__":
    conformer_search_workflow()