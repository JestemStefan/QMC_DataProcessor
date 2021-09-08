from qmc_dataprocessor.conformer_search_workflow import extract_data_from_files, filter_nonexisting_filenames, sort_filenames_by_last_number
import os
import unittest

class TestConformerSearchSorting(unittest.TestCase):

    def setUp(self):
        # initial list unsorted
        self.unsorted_testlist_case1 = ["name_01_addname_89_thirdname_11",
                                        "name_05_addname_16_thirdname_01",
                                        "name_04_addname_57_thirdname_7"]
        
        # initial numberless list unsorted
        self.unsorted_numberless_testlist = ["name_addname_thirdname_a",
                                            "name_addname_thirdname_c",
                                            "name_addname_thirdname_b"]

        # expected result, manually sorted list
        self.sorted_testlist_case1 = ["name_05_addname_16_thirdname_01",
                                      "name_04_addname_57_thirdname_7",
                                      "name_01_addname_89_thirdname_11"]

    
    def tearDown(self):
        pass


    # check if presorted list are not equal
    def test_list_presorted(self):

        # should not be equal so test should pass
        self.assertNotEqual(self.sorted_testlist_case1, self.unsorted_testlist_case1)
    

    # check if lists are equal after using sorting method
    def test_list_natural_sorted(self):

        # sort the list of names using custom sorting method
        sorted_test_list1 = sort_filenames_by_last_number(self.unsorted_testlist_case1)

        # list should be sorted
        self.assertEqual(sorted_test_list1, self.sorted_testlist_case1)
    

    # check if method handle empty list properly 
    def test_sorting_of_empty_list(self):

        # create an empty list and sort it
        empty_list = []
        sorted_empty_list = sort_filenames_by_last_number(empty_list)

        # should be equal
        self.assertEqual(sorted_empty_list, [])
    

    def test_sorting_of_list_without_numbers(self):

        expected_result_of_sorting_numberless_list = ["name_addname_thirdname_a",
                                                    "name_addname_thirdname_b",
                                                    "name_addname_thirdname_c"]

        # try sorting list without any numbers
        sorted_numberless_testlist = sort_filenames_by_last_number(self.unsorted_numberless_testlist)

        # Check if sorting of list was skipped so returned list should be still unsorted
        self.assertEqual(sorted_numberless_testlist, expected_result_of_sorting_numberless_list)
    

    def test_sorting_list_with_mixed_names(self):

        # create mixed list from number and numberless list of filenames
        unsorted_mixed_list = self.unsorted_testlist_case1 + self.unsorted_numberless_testlist

        expected_result_of_sorting_mixed_list = ["name_05_addname_16_thirdname_01",
                                                "name_04_addname_57_thirdname_7",
                                                "name_01_addname_89_thirdname_11",
                                                "name_addname_thirdname_a",
                                                "name_addname_thirdname_b",
                                                "name_addname_thirdname_c"]
        
        sorted_mixed_list = sort_filenames_by_last_number(unsorted_mixed_list)

        self.assertEqual(sorted_mixed_list, expected_result_of_sorting_mixed_list)


class TestConformerSearchExtractData(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_files_dir = "\\".join([self.root_dir, "cs_test_files"])
    

    def tearDown(self):
        pass


    def test_extract_data_filter_invalid_files(self):
        """ Tests if filter_nonexisting_filenames() filters out all filepaths that doesn't lead to existing file. """

        # create filename, absolute path for existing file
        filename_to_existing_file = "created_file_for_testing.txt"
        abs_filepath_to_existing_file = "\\".join([self.test_files_dir, filename_to_existing_file])

        # create existing file
        created_file = open(abs_filepath_to_existing_file, "x")

        # check if file was successfully created
        self.assertTrue(os.path.isfile(abs_filepath_to_existing_file))

        # run tested method with only filepath to existing file
        filtered_list_of_existing_filenames = filter_nonexisting_filenames(self.test_files_dir, [filename_to_existing_file])

        # check if filepath to existing file was returned
        self.assertEqual(filtered_list_of_existing_filenames, [filename_to_existing_file])


        # create filename of nonexisting file
        filename_of_nonexisting_file = "non_existing_file.txt"

        # run tested method with only filepath to NOT existing file
        filtered_list_of_nonexisting_filenames = filter_nonexisting_filenames(self.test_files_dir, [filename_of_nonexisting_file])

        # check if filepath to NOT existing file was removed and None was returned
        self.assertEqual(filtered_list_of_nonexisting_filenames, [])

        # create test list of filenames
        test_list_of_filepaths = [filename_to_existing_file, 
                                  filename_of_nonexisting_file]

        # run tested method
        filtered_list_of_filenames = filter_nonexisting_filenames(self.test_files_dir, test_list_of_filepaths)

        # check if method removed invalid filepath
        self.assertEqual(filtered_list_of_filenames, [filename_to_existing_file])


        # close file and delete it
        created_file.close()
        os.remove(abs_filepath_to_existing_file)
    

    def test_extract_hf_energy_data(self):
        # TODO Add test for data extraction for Hatree-Fock (SCF) energy.
        pass