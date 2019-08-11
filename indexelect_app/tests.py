import os
import pprint

from django.test import Client
from django.urls import reverse
from indexelect_app.index_select import *
import unittest

logger = logging.getLogger(__name__)

TEST_SET1_FILENAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test-data', 'test_data_for_Set1.xlsx')


class GetIndexesTest1(unittest.TestCase):
    # noinspection SpellCheckingInspection
    EXPECTED_RESULTS = {
        'data': [{'min_volume': 100.0,
                  'indexes': [{'well': 'B4', 'tag': 'tagged_214', 'id': 'BC26', 'sequence': 'AGGATCTA',
                               'volume': 100.0},
                              {'well': 'C4', 'tag': 'tagged_579', 'id': 'BC27', 'sequence': 'GACAGTAA',
                               'volume': 100.0},
                              {'well': 'D4', 'tag': 'tagged_426', 'id': 'BC28', 'sequence': 'CCTATGCC',
                               'volume': 100.0},
                              {'well': 'E4', 'tag': 'tagged_866', 'id': 'BC29', 'sequence': 'TCGCCTTG',
                               'volume': 100.0}]},
                 {'min_volume': 100.0,
                  'indexes': [{'well': 'C4', 'tag': 'tagged_579', 'id': 'BC27', 'sequence': 'GACAGTAA',
                               'volume': 100.0},
                              {'well': 'D4', 'tag': 'tagged_426', 'id': 'BC28', 'sequence': 'CCTATGCC',
                               'volume': 100.0},
                              {'well': 'E4', 'tag': 'tagged_866', 'id': 'BC29', 'sequence': 'TCGCCTTG',
                               'volume': 100.0},
                              {'well': 'F4', 'tag': 'tagged_250', 'id': 'BC30', 'sequence': 'ATAGCGTC',
                               'volume': 100.0}]},
                 {'min_volume': 100.0,
                  'indexes': [{'well': 'D4', 'tag': 'tagged_426', 'id': 'BC28', 'sequence': 'CCTATGCC',
                               'volume': 100.0},
                              {'well': 'E4', 'tag': 'tagged_866', 'id': 'BC29', 'sequence': 'TCGCCTTG',
                               'volume': 100.0},
                              {'well': 'F4', 'tag': 'tagged_250', 'id': 'BC30', 'sequence': 'ATAGCGTC',
                               'volume': 100.0},
                              {'well': 'G4', 'tag': 'tagged_752', 'id': 'BC31', 'sequence': 'GTCGCCTT',
                               'volume': 100.0}]},
                 {'min_volume': 100.0,
                  'indexes': [{'well': 'E4', 'tag': 'tagged_866', 'id': 'BC29', 'sequence': 'TCGCCTTG',
                               'volume': 100.0},
                              {'well': 'F4', 'tag': 'tagged_250', 'id': 'BC30', 'sequence': 'ATAGCGTC',
                               'volume': 100.0},
                              {'well': 'G4', 'tag': 'tagged_752', 'id': 'BC31', 'sequence': 'GTCGCCTT',
                               'volume': 100.0},
                              {'well': 'H4', 'tag': 'tagged_293', 'id': 'BC32', 'sequence': 'ATTCTAGG',
                               'volume': 100.0}]},
                 {'min_volume': 100.0,
                  'indexes': [{'well': 'B9', 'tag': 'tagged_500', 'id': 'BC66', 'sequence': 'CTAACTCG',
                               'volume': 100.0},
                              {'well': 'C9', 'tag': 'tagged_732', 'id': 'BC67', 'sequence': 'GTAACATC',
                               'volume': 100.0},
                              {'well': 'D9', 'tag': 'tagged_924', 'id': 'BC68', 'sequence': 'TGTAATCA',
                               'volume': 100.0},
                              {'well': 'E9', 'tag': 'tagged_288', 'id': 'BC69', 'sequence': 'ATTATCAA',
                               'volume': 100.0}]},
                 {'min_volume': 100.0,
                  'indexes': [{'well': 'C10', 'tag': 'tagged_567', 'id': 'BC75', 'sequence': 'GAAGGAAG',
                               'volume': 100.0},
                              {'well': 'D10', 'tag': 'tagged_868', 'id': 'BC76', 'sequence': 'TCGCTAGA',
                               'volume': 100.0},
                              {'well': 'E10', 'tag': 'tagged_110', 'id': 'BC77', 'sequence': 'ACAGTTGA',
                               'volume': 100.0},
                              {'well': 'F10', 'tag': 'tagged_320', 'id': 'BC78', 'sequence': 'CAATAGTC',
                               'volume': 100.0}]},
                 {'min_volume': 100.0,
                  'indexes': [{'well': 'D10', 'tag': 'tagged_868', 'id': 'BC76', 'sequence': 'TCGCTAGA',
                               'volume': 100.0},
                              {'well': 'E10', 'tag': 'tagged_110', 'id': 'BC77', 'sequence': 'ACAGTTGA',
                               'volume': 100.0},
                              {'well': 'F10', 'tag': 'tagged_320', 'id': 'BC78', 'sequence': 'CAATAGTC',
                               'volume': 100.0},
                              {'well': 'G10', 'tag': 'tagged_583', 'id': 'BC79', 'sequence': 'GACCGTTG',
                               'volume': 100.0}]},
                 {'min_volume': 100.0,
                  'indexes': [{'well': 'E10', 'tag': 'tagged_110', 'id': 'BC77', 'sequence': 'ACAGTTGA',
                               'volume': 100.0},
                              {'well': 'F10', 'tag': 'tagged_320', 'id': 'BC78', 'sequence': 'CAATAGTC',
                               'volume': 100.0},
                              {'well': 'G10', 'tag': 'tagged_583', 'id': 'BC79', 'sequence': 'GACCGTTG',
                               'volume': 100.0},
                              {'well': 'H10', 'tag': 'tagged_878', 'id': 'BC80', 'sequence': 'TCTGCAAG',
                               'volume': 100.0}]}]}

    def setUp(self):
        self.maxDiff = 100000  # to enable comparing the output when result is not as expected
        self.parameters = {
            'min_distance': 3, 'dist_from_middle': 0.3, 'max_bad_places': 2, 'min_volume': 100,
            'num_indexes': [4], 'file': open(TEST_SET1_FILENAME, 'rb')
        }
        # self.test_final_result = get_indexes(self.parameters)
        # self.result_list = self.test_final_result['data']
        # self.result_length = len(self.test_final_result['data'])
        self.client = Client()

    # Testing the post request
    def test_register_plates(self):
        response = self.client.post(reverse('register-index-plate'), self.parameters)
        self.assertEqual(response.status_code, 200)

    # Testing if the amount of indexes in each set of the results is equal to "num indexes" in parameters
    def test_get_indexes(self):
        result = get_indexes(self.parameters)
        logger.debug('Result: {}'.format(result))
        logger.debug('Result: {}'.format(pprint.pformat(result)))
        self.assertEqual(dict, type(result))
        self.assertTrue('data' in result)
        result_list = result['data']
        num_results = len(result_list)
        self.assertEqual(8, num_results, msg='Different amount of sets')
        self.assertEqual(self.EXPECTED_RESULTS, result)


class GetIndexesTest2(unittest.TestCase):
    # noinspection SpellCheckingInspection
    EXPECTED_RESULTS = {'data': []}

    def setUp(self):
        self.maxDiff = 100000  # to enable comparing the output when result is not as expected
        self.parameters = {
            'min_distance': 3, 'dist_from_middle': 0.3, 'max_bad_places': 2, 'min_volume': 90,
            'num_indexes': [6, 12, 20, 4], 'file': open(TEST_SET1_FILENAME, 'rb')
        }
        self.client = Client()

    def test_get_indexes(self):
        result = get_indexes(self.parameters)
        self.assertEqual(dict, type(result))
        self.assertTrue('data' in result)
        result_list = result['data']
        num_results = len(result_list)
        self.assertEqual(0, num_results, msg='Different amount of sets')
        self.assertEqual(self.EXPECTED_RESULTS, result)


class SmallMethodsTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 100000  # to enable comparing the output when result is not as expected

    def test_read_indexes_from_excel(self):
        indexes = read_indexes_from_excel(open(TEST_SET1_FILENAME, 'rb'))
        self.assertEqual(96, len(indexes))

    def test_divide_index_list_by_column(self):
        indexes = read_indexes_from_excel(open(TEST_SET1_FILENAME, 'rb'))
        x = divide_index_list_by_column(indexes, 2)
        self.assertEqual(132, len(x))
        dict_keys = list(x.keys())
        self.assertEqual([(3, 5), (5, 3), (3, 9)], dict_keys[0:3])
        self.assertEqual([(9, 1), (10, 1), (11, 1)], dict_keys[-3:])


class GetIndexesTest3(unittest.TestCase):
    # noinspection SpellCheckingInspection
    EXPECTED_RESULTS = {}

    def setUp(self):
        self.maxDiff = 100000  # to enable comparing the output when result is not as expected
        self.parameters = {
            'min_distance': 3, 'dist_from_middle': 0.2, 'max_bad_places': 3, 'min_volume': 30,
            'num_indexes': [6, 12, 20, 4], 'file': open(TEST_SET1_FILENAME, 'rb')
        }
        self.client = Client()

    def test_get_indexes(self):
        result = get_indexes(self.parameters)
        self.assertEqual(dict, type(result))
        self.assertTrue('data' in result)
        result_list = result['data']
        num_results = len(result_list)
        self.assertEqual(540, num_results, msg='Different amount of sets')
        self.assertEqual(self.EXPECTED_RESULTS, result)
