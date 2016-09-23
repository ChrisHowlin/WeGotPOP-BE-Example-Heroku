import collections
import geopy.distance
from wegotpopbeexample.controllers import relevanceutils

def sort_age(artists):
    return artists

def sort_location(artists, target_location):

    artists = sorted(artists,
                  key = lambda x: geopy.distance.distance(target_location,
                                                          (x['latitude'], x['longitude'])).miles)
    return artists

def sort_rate(artists):
    artists = sorted(artists,
                     key = lambda x: x['rate'])
    return artists

def sort_gender(artists):
    return artists

class BasicRelevanceStrategy:
    def filter_artists(self, artists_list, age_criteria, location_criteria, rate_criteria, gender_criteria):
        artists_list = list(filter(lambda x: relevanceutils.is_exact_match(x),
                                   artists_list))
        return artists_list

    def sort_artists(self, artists_list, age_criteria, location_criteria, rate_criteria, gender_criteria):
        relevance_dict = {}
        if(age_criteria is not None):
            relevance_dict[age_criteria.weight] = sort_age
        if(location_criteria is not None):
            target_location = (location_criteria.lat, location_criteria.lon)
            relevance_dict[location_criteria.weight] = lambda x: sort_location(x, target_location)
        if(rate_criteria is not None):
            relevance_dict[rate_criteria.weight] = sort_rate
        if(gender_criteria is not None):
            relevance_dict[gender_criteria.weight] = sort_gender

        relevance_ordered = collections.OrderedDict(sorted(relevance_dict.items(), reverse=True))

        for weight, sorter in relevance_ordered.items():
            print('Iterating sorters %s' % weight)
            artists_list = sorter(artists_list)

        return artists_list

    def apply(self, artists, age_criteria, location_criteria,
              rate_criteria, gender_criteria):
        artists_list = artists['artists']
        decorated_artists = []

        for artist in artists_list:
            decorated_artists.append(
                relevanceutils.decorate_artist(artist,
                                               age_criteria,
                                               location_criteria,
                                               rate_criteria,
                                               gender_criteria))

        filtered_artists = self.filter_artists(decorated_artists,
                                               age_criteria,
                                               location_criteria,
                                               rate_criteria,
                                               gender_criteria)

        sorted_artists = self.sort_artists(filtered_artists,
                                           age_criteria,
                                           location_criteria,
                                           rate_criteria,
                                           gender_criteria)

        artists_dict = { 'artists' : sorted_artists }
        # artists_dict = { 'artists' : decorated_artists }
        return artists_dict