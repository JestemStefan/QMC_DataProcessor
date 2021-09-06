from qmc_dataprocessor.conformer_search_workflow import sort_files
import unittest

class Test_ConformerSearch_Sorting(unittest.TestCase):

    def setUp(self):
        # initial list unsorted
        self.unsorted_testlist_case1 = ["name_01_addname_89_thirdname_11",
                                        "name_05_addname_16_thirdname_01",
                                        "name_04_addname_57_thirdname_7"]

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
        sorted_test_list1 = sort_files(self.unsorted_testlist_case1)

        # list should be sorted
        self.assertEqual(sorted_test_list1, self.sorted_testlist_case1)
    

    # check if method handle empty list properly 
    def test_sorting_of_empty_list(self):

        # create an empty list and sort it
        empty_list = []
        sorted_empty_list = sort_files(empty_list)

        # should be equal
        self.assertEqual(sorted_empty_list, [])
    

    def test_sorting_of_list_without_numbers(self):
        # initial list unsorted
        unsorted_numberless_testlist = ["name_addname_thirdname_a",
                                        "name_addname_thirdname_b",
                                        "name_addname_thirdname_c"]

        # try sorting list without any numbers
        sorted_numberless_testlist = sort_files(unsorted_numberless_testlist)

        # Check if sorting of list was skipped so returned list should be still unsorted
        self.assertEqual(sorted_numberless_testlist, unsorted_numberless_testlist)