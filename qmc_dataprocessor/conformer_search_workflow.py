from enum import Enum
from tkinter import messagebox
import os
import shutil
import re
from datetime import datetime
import math
import xlsxwriter

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
    KEY_IS_LOW_ENERGY = 10
    KEY_ABSOLUTE_PATH = 11


class CustomConstants:
    HATREE_CONST = 627.5094740631 #kcal/mol
    GAS_CONST = 0.00198720425864083 #kcal/(K/mol)


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
    list_of_filenames_with_numbers = [x for x in list_to_sort if len(re.findall(r'\d+', x)) > 0]
    list_of_filenames_no_numbers = [x for x in list_to_sort if len(re.findall(r'\d+', x)) == 0]

    # if there are filenames with number in them
    if list_of_filenames_with_numbers:

        # find all numbers in filename and pick up the last number as key for sorting. 
        list_of_filenames_with_numbers.sort(key=lambda x: int(re.findall(r'\d+', x)[-1]))
    
    # sort remaining filenames using default sorting.
    list_of_filenames_no_numbers.sort()

    # merge sorted lists and return new list
    return list_of_filenames_with_numbers + list_of_filenames_no_numbers


def create_output_folder(selected_path: str) -> str:
    """Creates folder with unique name based on current time and date
    that will store output data. Returns path to created folder"""
    
    # create unique name for output folder using current time and date
    output_folder_name = "Output_" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # get parent folder name to place output folder there
    parent_folder_name = os.path.dirname(selected_path)

    # create absolute path to output folder
    output_folderpath = "\\".join([parent_folder_name, output_folder_name])

    # create new directory
    os.mkdir(output_folderpath)

    # return created output folder path
    return output_folderpath


# method for creating database with placeholder entries for each file
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
                  DictKeys.KEY_IS_LOW_ENERGY : False,
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
def extract_data_from_files(parent_folder_path: str, filenames_list: list, data_base_dict: dict) -> None:
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

            # create absolute path for file for convenience
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


def get_valid_energy_values(database_dict: dict, INPUT_ENERGY_KEY, VALIDATION_KEY) -> list:
    """Extract values specified by an INPUT_ENERGY_KEY from a database_dict that return True from VALIDATION_KEY. Returns list of extracted values"""

    return [database_dict[file][INPUT_ENERGY_KEY] for file in database_dict.keys() if database_dict[file][VALIDATION_KEY]]


def get_relative_value_in_kcal(input_value: float, base_value: float) -> float:
    """Takes input value and substracts minimal value from it. Use HATREE_CONST to convert value to kcal/mol. Returns relative value as float"""
    
    if type(input_value) not in [int, float]:
        raise TypeError("Input value must be a number")
    
    if type(base_value) not in [int, float]:
        raise TypeError("Base value must be a number")

    return (input_value - base_value) * CustomConstants.HATREE_CONST


def calculate_relative_energy_values(database_dict: dict, INPUT_ENERGY_KEY: int, VALIDATION_KEY: int, OUTPUT_ENERGY_KEY: int) -> None:
    """Calculate relative values of energy data. Insert data straight into dictionary. Returns None."""
    
    # Get correct values by removing values from files that failed calculations.
    list_of_all_energies = get_valid_energy_values(database_dict, INPUT_ENERGY_KEY, VALIDATION_KEY)

    # get minimal value of energy to use it in relative values calculation.
    min_energy_value = min(list_of_all_energies)

    # for each file calculate relative energy value in kcal/mol and insert it into database dict
    for file in database_dict.keys():

        database_dict[file][OUTPUT_ENERGY_KEY] = get_relative_value_in_kcal(database_dict[file][INPUT_ENERGY_KEY], min_energy_value)


def find_unique_and_duplicate_conformers(database_dict: dict, output_folder: str) -> None:
    """Analyze data in database and find unique and duplicate files. Copy files to new folders. Returns None"""

    # Prepare folderpath for each category of files
    duplicates_folderpath = "\\".join([output_folder, "Duplicates"])
    unique_folderpath = "\\".join([output_folder, "Unique_Conformers"])
    failed_folderpath = "\\".join([output_folder, "Failed_Files"])

    # Create output folders
    os.mkdir(duplicates_folderpath)
    os.mkdir(unique_folderpath)
    os.mkdir(failed_folderpath)

    # TODO Add 3D space coordinates analysis

    # Create an array that will store previous energies to compare and find duplicates
    existing_energy_pair_arr = []

    # Check each file
    for file in database_dict:
        
        # Round energy to 6 decimal places, because this is a limit of accuracy for this calculations
        hf_dg_energy_pair = [round(database_dict[file][DictKeys.KEY_HF_ENERGY], 6), round(database_dict[file][DictKeys.KEY_DG_ENERGY], 6)]

        # Check if this energy pair already exists
        if hf_dg_energy_pair in existing_energy_pair_arr:
            
            # Copy duplicate to Duplicates folder
            shutil.copy2(database_dict[file][DictKeys.KEY_ABSOLUTE_PATH], "\\".join([duplicates_folderpath, database_dict[file][DictKeys.KEY_FILENAME]]))

            # Set as not unique = Duplicate
            database_dict[file][DictKeys.KEY_IS_UNIQUE] = False

        
        # if unique
        else:
            # Add its energy to the list of energies
            existing_energy_pair_arr.append(hf_dg_energy_pair)

            # Copy file to the folder with Unique files
            shutil.copy2(database_dict[file][DictKeys.KEY_ABSOLUTE_PATH], "\\".join([unique_folderpath, database_dict[file][DictKeys.KEY_FILENAME]]))

            # Set as unique
            database_dict[file][DictKeys.KEY_IS_UNIQUE] = True

        # if calculations failed then copy files to Failed folder.
        if not database_dict[file][DictKeys.KEY_IS_OPTIMIZATION_DONE]:
            shutil.copy2(database_dict[file][DictKeys.KEY_ABSOLUTE_PATH], "\\".join([failed_folderpath, database_dict[file][DictKeys.KEY_FILENAME]]))


def calculate_population_of_conformers(database_dict: dict, key_relative_energy, population_key, temperature: float, energy_limit: float) -> None:
    """Finds population of each conformer from the database by comparing relative energies. Returns None"""

    # create variable that will store sum of all conformers
    population_sum = 0

    # for each conformer in database
    for conformer in database_dict:

        # set up initial population to zero
        conformer_population = 0

        # if conformer relative energy is higher then a limit or conformer is not unique or calculation failed
        if (database_dict[conformer][key_relative_energy] > energy_limit 
            or not database_dict[conformer][DictKeys.KEY_IS_UNIQUE] 
            or not database_dict[conformer][DictKeys.KEY_IS_OPTIMIZATION_DONE]):
            
            # skip / set population to 0
            conformer_population = 0
        
        # file is unique and relative energy is under limit
        else:
            # use normal distribution formula to calculate population based on input parameters
            conformer_population = math.exp(-1 * database_dict[conformer][key_relative_energy] / temperature / CustomConstants.GAS_CONST)
        
        # save row population value to database for later recalculation 
        database_dict[conformer][population_key] = conformer_population
        
        # add conformer population to the sum
        population_sum += conformer_population
        
    # recalculate population value for each conformer as percentage of sum
    for conformer in database_dict:
        database_dict[conformer][population_key] = round(100 * database_dict[conformer][population_key]/population_sum, 2)


def find_low_energy_conformers(database_dict: dict, energy_limit: float, output_folder: str) -> None:
    """Finds conformers in database that have energy below specified limit and copy them to output folder. Returns None"""

    # Create path to folder that will store low energy conformers
    low_energy_folderpath = "\\".join([output_folder, "Low_energy_conformers"])

    # create folder
    os.mkdir(low_energy_folderpath)

    # for each conformer
    for conformer in database_dict:
        
        # check if file is unique
        if database_dict[conformer][DictKeys.KEY_IS_UNIQUE]:
            
            # if any energy is below energy limit
            if database_dict[conformer][DictKeys.KEY_HF_ENERGY] <= energy_limit or database_dict[conformer][DictKeys.KEY_DG_RELATIVE_ENERGY] <= energy_limit:
                
                # mark as low energy conformer
                database_dict[conformer][DictKeys.KEY_IS_LOW_ENERGY] = True

                # copy file to folder
                shutil.copy2(database_dict[conformer][DictKeys.KEY_ABSOLUTE_PATH], "\\".join([low_energy_folderpath, database_dict[conformer][DictKeys.KEY_FILENAME]]))


def export_to_excel(database_dict: dict, output_folderpath: str) -> None:
    """Exports collected data to excel file. Returns None"""
    
    # Createnew excel file
    excel_output_file = xlsxwriter.Workbook("\\".join([output_folderpath, "Summary.xlsx"]))

    # Inside file create worksheet called Summary, Unique and Low Energy Conformers
    ws_summary = excel_output_file.add_worksheet("Summary")
    ws_unique = excel_output_file.add_worksheet("Unique")
    ws_low_energy_conformers = excel_output_file.add_worksheet("Low Energy Conformers")

    # Setting format for cells
    center = excel_output_file.add_format({'align': 'center'})
    mark_green = excel_output_file.add_format({'align': 'center', 'bg_color': "#98fb98"})  # green in HEX
    mark_yellow = excel_output_file.add_format({'align': 'center', 'bg_color': "#f7ff7e"})  # red in HEX
    mark_red = excel_output_file.add_format({'align': 'center', 'bg_color': "#ffcccb"})  # red in HEX

    # Preparing titles for 1st row
    titles = ["Name", "Opt_Done", "Vib_Done",
              "HF", "Relative HF [kcal]", "HF population[%]",
              "dG", "Relative dG [kcal]", "dG population[%]", "Unique?"]
    
     # column width setup
    for worksheet in ws_summary, ws_unique, ws_low_energy_conformers:
        worksheet.set_column("A:A", 36)
        worksheet.set_column("B:I", 20)

        # Place titles in first row
        for index, title in enumerate(titles):
            worksheet.write(0, index, title, center)
    
    row_u = 1  # row value for unique worksheet
    row_l = 1  # row value for low energy worksheet

    # for each data entry in database
    for index, file in enumerate(database_dict):
        
        # set format as center by default
        use_format = center

        # list of keys to use
        key_list = [DictKeys.KEY_FILENAME,
                  DictKeys.KEY_IS_OPTIMIZATION_DONE,
                  DictKeys.KEY_ARE_FREQUENCIES_REAL,
                  DictKeys.KEY_HF_ENERGY,
                  DictKeys.KEY_HF_RELATIVE_ENERGY,
                  DictKeys.KEY_HF_POPULATION,
                  DictKeys.KEY_DG_ENERGY,
                  DictKeys.KEY_DG_RELATIVE_ENERGY,
                  DictKeys.KEY_DG_POPULATION,
                  DictKeys.KEY_IS_UNIQUE]

        # If file is unique then mark row in green
        if database_dict[file][DictKeys.KEY_IS_UNIQUE]:
            use_format = mark_green

            # if file failed is result of failed calculations then mark row in red
            if not database_dict[file][DictKeys.KEY_IS_OPTIMIZATION_DONE]:
                use_format = mark_red
            
            # if file have negative frequencies (imaginary frequencies) then mark in yellow
            elif not database_dict[file][DictKeys.KEY_ARE_FREQUENCIES_REAL]:
                use_format = mark_yellow
            
            # for each key enter data into a row
            for column in range(len(key_list)):
                ws_unique.write(row_u, column, database_dict[file][key_list[column]], use_format)

            # next row in unique spreadsheet
            row_u += 1

            # if this unique file is also low energy conformer then add data to low_energy worksheet
            if database_dict[file][DictKeys.KEY_IS_LOW_ENERGY]:
                for column in range(len(key_list)):
                    ws_low_energy_conformers.write(row_l, column, database_dict[file][key_list[column]], use_format)
                
                # prepare next row in low_energy worksheet
                row_l += 1  

        # write every file data in first spreadsheet
        for column in range(len(key_list)):
            ws_summary.write(index + 1, column, database_dict[file][key_list[column]], use_format)

    excel_output_file.close()



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

            output_folder_path = create_output_folder(cs_parent_folderpath)

            # initialize database that will store data from files
            cs_database = create_database_with_placeholder_data(outfile_list)
            
            # Extract data from file to database
            extract_data_from_files(cs_parent_folderpath, outfile_list, cs_database)

            # Calculate relative values of energy for Hatree-Fock energy and Gibbs free energy
            calculate_relative_energy_values(cs_database, DictKeys.KEY_HF_ENERGY, DictKeys.KEY_IS_OPTIMIZATION_DONE, DictKeys.KEY_HF_RELATIVE_ENERGY)
            calculate_relative_energy_values(cs_database, DictKeys.KEY_DG_ENERGY, DictKeys.KEY_ARE_FREQUENCIES_REAL, DictKeys.KEY_DG_RELATIVE_ENERGY)

            find_unique_and_duplicate_conformers(cs_database, output_folder_path)

            calculate_population_of_conformers(cs_database, DictKeys.KEY_HF_RELATIVE_ENERGY, DictKeys.KEY_HF_POPULATION, temperature, energy_limit)
            calculate_population_of_conformers(cs_database, DictKeys.KEY_DG_RELATIVE_ENERGY, DictKeys.KEY_DG_POPULATION, temperature, energy_limit)

            find_low_energy_conformers(cs_database, energy_limit, output_folder_path)

            export_to_excel(cs_database, output_folder_path)

            os.startfile(output_folder_path)




if __name__== "__main__":
    conformer_search_workflow(os.path.dirname(os.path.abspath(__file__)), 293.15, 2.0)