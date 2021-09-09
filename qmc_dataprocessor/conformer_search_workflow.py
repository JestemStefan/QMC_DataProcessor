from enum import Enum
from tkinter import messagebox
import os
import re

class DictKeys(Enum):
    KEY_FILENAME = 0
    KEY_IS_OPTIMIZATION_DONE = 1
    KEY_ARE_FREQUENCIES_REAL = 2
    KEY_HF_ENERGY = 3
    KEY_HF_RELATIVE_ENERGY = 4
    KEY_HF_POPULATION = 5
    KEY_DG_ENERGY = 6
    KEY_DG_RELATIVE_ENERGY = 7
    KEY_DG_POPULATION = 8
    KEY_IS_UNIQUE = 9
    KEY_ABSOLUTE_PATH = 10



# Method to find and load .out files in selected folder
def find_out_files(selected_path: str) -> list:
    """Finds all files with .out extension in folder specified by path string. Returns list of filenames as list."""

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
    """Sorts list by last number in filename if possible. Use default sort otherwise. Returns sorted list."""

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
    """Creates database dictionary with placeholder data for each file. Returns database as dictionary."""

    # TODO Move to SQL or some other database

    # create empty dict that will be filled with placeholder data and returned
    new_database_dict = {}

    # prepare placeholder data that will be inserted into dict for each file
    empty_data = {DictKeys.KEY_FILENAME : "no_name",
                  DictKeys.KEY_IS_OPTIMIZATION_DONE : False,
                  DictKeys.KEY_ARE_FREQUENCIES_REAL : True,
                  DictKeys.KEY_HF_ENERGY : 0,
                  DictKeys.KEY_HF_RELATIVE_ENERGY : 0,
                  DictKeys.KEY_HF_POPULATION : 0,
                  DictKeys.KEY_DG_ENERGY : 0,
                  DictKeys.KEY_DG_RELATIVE_ENERGY : 0,
                  DictKeys.KEY_DG_POPULATION : 0,
                  DictKeys.KEY_IS_UNIQUE : False,
                  DictKeys.KEY_ABSOLUTE_PATH : "default_path"}

    # fill the database with placeholder data
    for filename in list_of_filenames:
        new_database_dict[filename] = empty_data.copy() # <-- must use .copy() or they will share the same dict by reference

    # return filled database dictionary
    return new_database_dict


def filter_nonexisting_filenames(root_folder_path: str, filenames_list: list) -> list:
    """Removes filenames to not existing files and return filtered list of valid filenames"""

    return list(filter(lambda x: os.path.isfile("\\".join([root_folder_path, x])), filenames_list))


# Method for extracting data from text files. This method is very specific to Gaussian output files.
def extract_data_from_files(parent_folder_path, filenames_list, data_base_dict):
    """Extracts data values from Gaussian output files. Insert them into provided dictionary. Returns None"""

    # filter out filenames to non-existing files
    filenames_list = filter_nonexisting_filenames(parent_folder_path, filenames_list)

    # if there are no valid filenames.
    if not filenames_list:
        pass
        # TODO display error

    else:
        # Run method for each file in sequence
        # TODO Can be easily parallelized (Multicore?)
        for filename in filenames_list:
            
            # get default values from database
            hf_energy_value = data_base_dict[filename][DictKeys.KEY_HF_ENERGY]
            dg_energy_value = data_base_dict[filename][DictKeys.KEY_DG_ENERGY]
            is_optimization_successful = data_base_dict[filename][DictKeys.KEY_IS_OPTIMIZATION_DONE]
            are_all_frequencies_real = data_base_dict[filename][DictKeys.KEY_ARE_FREQUENCIES_REAL]

            # create abslute path for file for convenience
            file_abs_filepath = "\\".join([parent_folder_path, filename])

            # open file and check each line in it
            with open(file_abs_filepath) as textfile_with_data:

                for line in textfile_with_data:
                    
                    # SCF (self-consistent field) method value is Hatree-Fock energy. (Historic reasons?)
                    if "SCF Done:" in line:
            
                        # find float value in line. Should be only one, but we will pick first just to be sure.
                        extracted_hf_data = re.findall("[+-]?[0-9]*[.][0-9]+", line)
                        hf_energy_value = float(extracted_hf_data[0]) if extracted_hf_data else hf_energy_value
                    
                    # dG (Gibbs free energy) value
                    elif "Free Energies=" in line:
            
                        # find float value in line. Should be only one, but we will pick first just to be sure.
                        extracted_dg_data = re.findall("[+-]?[0-9]*[.][0-9]+", line)
                        dg_energy_value = float(extracted_dg_data[0]) if extracted_dg_data else dg_energy_value
                    
                    # if file contain "Normal termination" phrase then structure optimization was successful.
                    elif "Normal termination" in line:
                        is_optimization_successful = True
                    
                    # if file contain "imaginary frequencies" phrase then some frequencies have negative values.
                    elif "imaginary frequencies" in line:
                        are_all_frequencies_real = False
            
            # Insert data into database
            data_base_dict[filename][DictKeys.KEY_FILENAME] = filename
            data_base_dict[filename][DictKeys.KEY_IS_OPTIMIZATION_DONE] = is_optimization_successful
            data_base_dict[filename][DictKeys.KEY_ARE_FREQUENCIES_REAL] = are_all_frequencies_real
            data_base_dict[filename][DictKeys.KEY_HF_ENERGY] = hf_energy_value
            data_base_dict[filename][DictKeys.KEY_DG_ENERGY] = dg_energy_value
            data_base_dict[filename][DictKeys.KEY_ABSOLUTE_PATH] = file_abs_filepath


# main method of conformer search. Called by GUI button
def conformer_search_workflow(cs_parent_folderpath: str, temperature: float, energy_limit: float) -> None:
    """Performs analysis of data from conformer search calculations in specified parameters. Returns None."""

    # if no folder path was selected
    if not cs_parent_folderpath:  
        
        # throw an error message box informing user about invalid folder path
        messagebox.showerror('Error: Invalid folder path', 'No valid folder path was selected')
        print('No valid folder path was selected')

    else: 
        # find and loads filenames of valid files in the specified folder
        outfile_list = find_out_files(cs_parent_folderpath)

        # throw an error message box if there is NO files of correct type in folder
        if not len(outfile_list):
            messagebox.showerror('Error: No valid files in selected folder', 'There is no valid *.out files in selected folder')
            print('There is no valid *.out files in selected folder')

        else:
            # Sort filenames in outfile_list using natural sort
            outfile_list = sort_filenames_by_last_number(outfile_list)

            # initialize database that will store data from files
            cs_database = create_database_with_placeholder_data(outfile_list)
            
            # TODO extract data from files
            # TODO multithreaded? :eyes:
            extract_data_from_files(cs_parent_folderpath, outfile_list, cs_database)


if __name__== "__main__":
    conformer_search_workflow()