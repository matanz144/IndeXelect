import itertools
import logging
import xlrd
from collections import defaultdict, OrderedDict
from typing import List, Tuple
# from django.core.files import File

NUM_COLUMNS = 12
MAX_RESULTS = 100
MAX_NUM_PERMUTATIONS = 1000000

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Index(object):
    def __init__(self, index_well, index_tag, index_id, sequence, volume):
        self.well = index_well
        self.row, self.column = self._get_row_and_column()
        self.sequence = sequence
        self.size = len(self.sequence)  # Do we need this ??
        self.id = index_id
        self.volume = volume
        self.tag = index_tag

    def __repr__(self):
        return 'well: {}, tag: {}, sequence: {}, id: {}, volume: {}'.format(self.well, self.tag, self.sequence, self.id, self.volume)

    def to_dict(self):
        return {'well': self.well, 'tag': self.tag, 'id': self.id, 'sequence': self.sequence, 'volume': self.volume}

    def _get_row_and_column(self):
        row = ord(self.well[0]) - ord('A')
        if len(self.well) == 3:
            col = (int(self.well[1])) * 10 + (int(self.well[2]))
        else:
            col = int(self.well[1])
        return row, col - 1

    def distance(self, other):
        return distance(self.sequence, other.sequence)


class IndexSet(Index):
    def __init__(self, index_set_id, index_list):
        self.indexes = index_list
        self.id = index_set_id
        self.min_volume = min([index.volume for index in index_list])
        self.match = 0

    def __repr__(self):
        return repr(dict(id=self.id, min_volume=self.min_volume, indexes=self.indexes))


def read_indexes_from_excel(file):
    file_contents = file.read()
    wb = xlrd.open_workbook(file_contents=file_contents)
    sheet = wb.sheet_by_name('Sheet0')
    index_list = []

    if sheet.cell_value(0, 0) == "Index Well" and sheet.cell_value(0, 2) == "Index Tag":
        pass
    else:
        logger.error('There is a problem with the file')
    for i in range(1, sheet.nrows):
        index_well = sheet.cell_value(i, 0)
        index_id = sheet.cell_value(i, 1)
        index_tag = sheet.cell_value(i, 2)
        sequence = sheet.cell_value(i, 3)
        volume = sheet.cell_value(i, 4)
        new_index = Index(index_well, index_tag, index_id, sequence, volume)
        index_list.append(new_index)
    return index_list


def find_max_min_volume(index_dict):
    vol_dict = {}
    for index_set_id, index_list in index_dict.items():
        vol_dict[index_set_id] = min([index.volume for index in index_list])
    ordered_vol_list = sorted(vol_dict.items(), key=lambda item: item[1])
    return ordered_vol_list[-1]


def divide_index_list_by_column(index_list, num_columns):
    index_dict = OrderedDict(defaultdict(list))
    columns = range(NUM_COLUMNS)
    num_permutations = 1
    for i in range(NUM_COLUMNS, NUM_COLUMNS-num_columns, -1):
        num_permutations *= i
    logger.info('num_permutations: {}'.format(num_permutations))
    if num_permutations <= MAX_NUM_PERMUTATIONS:
        column_groups = list(itertools.permutations(columns, num_columns))
    else:
        column_groups = list(itertools.combinations(columns, num_columns))
    logger.info('#column_groups: {}'.format(len(column_groups)))
    for column_group in column_groups:
        index_dict[column_group] = _union_columns(index_list, column_group)
    all_index_sets = [IndexSet(column_group, index_list) for column_group, index_list in index_dict.items()]
    all_index_sets.sort(key=lambda i: i.min_volume, reverse=True)
    index_dict = OrderedDict(defaultdict(list))
    for index_set in all_index_sets:
        index_dict[index_set.id] = index_set.indexes
    return index_dict


def _union_columns(index_list, column_group):
    """Return a list of indexes which are located in the given columns of the index plate"""
    lst = []
    for index in index_list:
        if index.column in column_group:
            lst.append(index)
    return lst


def distance(first, second):
    dist = 0
    for x, y in zip(first, second):
        if x != y:
            dist += 1
    return dist


def calc_distances(index_list):
    if len(index_list) == 0:
        raise ValueError('Empty index list')
    dist_list = []
    for i in range(len(index_list)):
        for j in range(i + 1, len(index_list)):
            dist_list.append(distance(index_list[i].sequence, index_list[j].sequence))
    return dist_list


def find_min_distance(index_list):
        return min(calc_distances(index_list))


def create_ac_content_list(indexes, index_length):
    num_indexes = len(indexes)
    ac_content_list = []
    for index in range(index_length):
        ac_count = 0
        for barcode in indexes:
            if barcode.sequence[index] in ('A', 'C'):
                ac_count += 1
            # print(barcode.sequence)

        ac_content_list.append(float(ac_count / num_indexes))

    return ac_content_list


def good_places(dist_from_middle, ac_content_list):
    num_good_places = 0
    for ac_content in ac_content_list:
        if abs(ac_content - 0.5) <= dist_from_middle:
            num_good_places += 1
    return num_good_places


def find_good_indexes(all_index_set, min_vol):
    list_of_good_indexes = []
    logger.debug(all_index_set[0])
    for index_set in all_index_set:
        if index_set.min_volume >= min_vol:
            list_of_good_indexes.append(index_set)
        else:
            pass
              # logger.info('IndexSet {} : minimum volume too low: {}'.format(index_set.id, index_set.min_volume))
    return list_of_good_indexes


def find_max_min_volume_with_index_set(index_set_list: List[Tuple[IndexSet, List]]):
    index_set_list_ordered_by_min_volume = sorted(index_set_list, key=lambda index_set: index_set[0].min_volume,
                                                  reverse=True)
    return index_set_list_ordered_by_min_volume


def find_one_good_column(one_column_dict):
    volume_list = []
    for index_set in one_column_dict.values():
        lst = []
        for index in index_set:
            lst.append(index.volume)
        volume_list.append(min(lst))
    maximum = max(volume_list)
    for index_set in one_column_dict.values():
        for vol in index_set:
            if vol.volume == maximum:
                col = vol.column
    for key, value in one_column_dict.items():
        for index_set in value:
            if index_set.column == col:
                return key


def create_list_of_indexes_in_one_column(one_good_column, num_of_samples):
    indexes_gruops = list(itertools.combinations(one_good_column, num_of_samples))
    return indexes_gruops


def examine_index_set(index_set, parameters):
    # logger.debug('examine_index_set with {}'.format(index_set))
    # good_index_sets = []
    # divide the single index_set to experiment index sets according to parameters['num_indexes']
    for possible_num_indexes in sorted(list(set(itertools.permutations(parameters['num_indexes'])))):
        experiment_index_sets = []
        first_index = 0
        for i in range(len(possible_num_indexes)):
            last_index = first_index + possible_num_indexes[i]
            experiment_index_set_id = str(index_set.id) + ' indexes {} to {}'.format(first_index, last_index-1)
            experiment_index_sets.append(IndexSet(experiment_index_set_id, index_set.indexes[first_index:last_index]))
            first_index += possible_num_indexes[i]
        for experiment_index_set in experiment_index_sets:
            match = examine_experiment_index_set(experiment_index_set, parameters)
            if not match:
                break
        if match:
            return experiment_index_sets, possible_num_indexes
            # good_index_sets.append(possible_num_indexes)
    # logger.debug('good_index_sets: {}'.format(good_index_sets))
    return [], False


def _build_all_index_sets(index_dict_by_column, num_indexes):
    num_indexes_from_partial_column = num_indexes % 8
    if num_indexes_from_partial_column == 0:
        logger.info('No partial columns')
        all_index_sets = [IndexSet(column_group, indexes) for column_group, indexes in index_dict_by_column.items()]
    else:
        logger.info('We have partial columns')
        all_index_sets = []
        for (iter_number, (column_group, all_indexes)) in enumerate(index_dict_by_column.items()):
            full_columns = column_group[:-1]
            partial_column = column_group[-1]
            if iter_number % 1000 == 0:
                logger.debug('{}: full_columns: {} partial_column: {}'.format(
                    iter_number, full_columns, partial_column))
            full_columns_indexes = [index for index in all_indexes if index.column in full_columns]
            all_partial_column_indexes = [index for index in all_indexes if index.column == partial_column]
            all_partial_column_indexes.sort(key=lambda index: index.row)
            for first_row in range(8-num_indexes_from_partial_column+1):
                selected_indexes = all_partial_column_indexes[first_row:first_row + num_indexes_from_partial_column]
                index_list = full_columns_indexes + selected_indexes
                index_set_id = list(full_columns) + sorted([index.id for index in selected_indexes])
                new_index_set = IndexSet(index_set_id=index_set_id, index_list=index_list)
                all_index_sets.append(new_index_set)
    logger.debug('done build_all_index_sets')
    return all_index_sets


def _new_build_and_filter(index_dict_by_column, num_indexes, parameters):
    num_indexes_from_partial_column = num_indexes % 8
    if num_indexes_from_partial_column == 0:
        logger.info('No partial columns')
        # TODO add filtering here too (like in the partial columns scenario)
        all_index_sets = [IndexSet(column_group, indexes) for column_group, indexes in index_dict_by_column.items()]
    else:
        logger.info('We have partial columns')
        all_index_sets = []
        for (iter_number, (column_group, all_indexes)) in enumerate(index_dict_by_column.items()):
            if len(all_index_sets) > MAX_RESULTS:
                break
            full_columns = column_group[:-1]
            partial_column = column_group[-1]
            if iter_number % 1000 == 0:
                logger.debug('{}: full_columns: {} partial_column: {} number of indexes so far: {}'.format(
                    iter_number, full_columns, partial_column, len(all_index_sets)))
            full_columns_indexes = [index for index in all_indexes if index.column in full_columns]
            all_partial_column_indexes = [index for index in all_indexes if index.column == partial_column]
            all_partial_column_indexes.sort(key=lambda index: index.row)
            for first_row in range(8-num_indexes_from_partial_column+1):
                selected_indexes = all_partial_column_indexes[first_row:first_row + num_indexes_from_partial_column]
                index_list = full_columns_indexes + selected_indexes
                index_set_id = list(full_columns) + sorted([index.id for index in selected_indexes])
                new_index_set = IndexSet(index_set_id=index_set_id, index_list=index_list)
                # TODO add filtering to know if we want to keep this set or not
                if new_index_set.min_volume < parameters['min_volume']:
                    # logger.debug('Index set skipped - min_volume is {}'.format(new_index_set.min_volume))
                    continue
                experiment_index_sets, match = examine_index_set(new_index_set, parameters)
                if not match:
                    # logger.debug('Index set skipped - no matches found')
                    continue
                # all_index_sets += [(new_index_set, match) for match in matches]
                all_index_sets.append((new_index_set, match))
    return all_index_sets


def examine_experiment_index_set(index_set, parameters):
    indexes = index_set.indexes
    errors = []
    index_length_set = set([i.size for i in indexes])
    if len(index_length_set) != 1:
        raise ValueError('Cannot determine index length: {}'.format(index_length_set))
    index_length = index_length_set.pop()
    # print(indexes)
    min_distance = find_min_distance(indexes)
    # print('Min distance: {}'.format(min_distance))
    if min_distance < parameters['min_distance']:
        logger.debug('IndexSet {} : indexes too close. Distance: {}'.format(index_set.id, min_distance))
        errors.append('Indexes are too close')
    lst = create_ac_content_list(indexes, index_length)
    num_good_places = good_places(parameters['dist_from_middle'], lst)
    # print('Good places: {}'.format(num_good_places))
    # if num_good_places < index_length - parameters['max_bad_places']:
    #     logger.debug('IndexSet {} : too many bad places. Good places: {}'.format(index_set.id, num_good_places))
    #     errors.append('There are too many bad places')
    if min_distance >= parameters['min_distance'] and num_good_places >= index_length - parameters['max_bad_places']:
        match = True
    else:
        match = False
    return match  # return 'match' instead of 'errors' list


def _translate_list_to_dict(final_list):
    new_list = []
    final_result_dict = {'data': []}
    # for value in final_list:
    #     new_list.append(value[0])
    for (index_set, match) in final_list:
    # for value in new_list:
        new_dict = {
            'min_volume': index_set.min_volume,
            'indexes': [obj.to_dict() for obj in index_set.indexes],
            'num_samples': match
        }
        final_result_dict['data'].append(new_dict)
    return final_result_dict


# TODO rename
def get_indexes(parameters):
    logger.info('Searching for proper indexes with parameters: {}'.format(parameters))
    # 1. read the full 96 indexes
    final_list = []
    file = parameters['file']
    indexes = read_indexes_from_excel(file)
    num_total_indexes = sum(parameters['num_indexes'])
    num_full_columns = (num_total_indexes+7) // 8

    logger.info('#Total indexes: {} #Full columns: {}'.format(num_total_indexes, num_full_columns))

    # The function gets a list of indexes and the number of columns to union
    index_dict_by_column = divide_index_list_by_column(indexes, num_full_columns)
    logger.info('#index_dict_by_column {}'.format(len(index_dict_by_column)))

    list_of_good_indexes = _new_build_and_filter(index_dict_by_column, num_total_indexes, parameters)
    logger.info('#index sets: {}'.format(len(list_of_good_indexes)))

    if len(list_of_good_indexes) == 0:
        logger.info('There are no good indexes')
    else:
        final_list = find_max_min_volume_with_index_set(list_of_good_indexes)
    logger.info('#final_list: {}'.format(len(final_list)))

    final_result = _translate_list_to_dict(final_list)

    return final_result
