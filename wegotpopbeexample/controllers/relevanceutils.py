import collections

class SorterList:
    def __init__(self, sorter_dict):
        ''' sorter_dict maps sorter names to functions '''
        self.sorter_dict = sorter_dict
        self.sorter_weights = {}

    def add_weight(self, label, weight):
        self.sorter_weights[weight] = label

    def sort(self, list_to_sort):
        # First sort the list so weakest first

        sorters_ordered = collections.OrderedDict(sorted(self.sorter_weights.items(),
                                                         reverse=True))

        for weight, sorter in sorters_ordered.items():
            print('Iterating sorters %s' % sorter)
            list_to_sort = self.sorter_dict[sorter](list_to_sort)

        return list_to_sort

def is_exact_match(artist):
    return((artist['age_distance'] == 0)
        and (artist['location_distance'] == 0.0)
        and (artist['rate_distance'] == 0.0)
        and (artist['gender_distance'] == 0))

def decorate_artist(artist, age_criteria, location_criteria, rate_criteria, gender_criteria):
    if(age_criteria is not None):
        artist['age_distance'] = age_criteria.get_distance(artist['age'])
    else:
        artist['age_distance'] = 0

    if(location_criteria is not None):
        artist['location_distance'] = location_criteria.get_distance(artist['latitude'],
                                                                    artist['longitude'])
    else:
        artist['location_distance'] = 0.0

    if(rate_criteria is not None):
        artist['rate_distance'] = rate_criteria.get_distance(artist['rate'])
    else:
        artist['rate_distance'] = 0.0

    if(gender_criteria is not None):
        artist['gender_distance'] = gender_criteria.get_distance(artist['gender'])
    else:
        artist['gender_distance'] = 0

    return artist