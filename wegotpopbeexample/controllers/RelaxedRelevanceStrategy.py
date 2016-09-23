import collections
from wegotpopbeexample.controllers import relevanceutils


MIN_RETURN_VALUE = 100

def sort_age(artists):
    artists = sorted(artists,
                     key = lambda x: x['age_distance'])
    return artists

def sort_location(artists):
    artists = sorted(artists,
                     key = lambda x: x['location_distance'])
    return artists

def sort_rate(artists):
    artists = sorted(artists,
                     key = lambda x: x['rate_distance'])
    return artists

def sort_gender(artists):
    artists = sorted(artists,
                     key = lambda x: x['gender_distance'])
    return artists

sorter_dict = {'age' : sort_age,
               'location' : sort_location,
               'rate' : sort_rate,
               'gender' : sort_gender}

class RelaxedRelevanceStrategy:
    def filter_artists(self, artists, age_criteria, location_criteria, rate_criteria, gender_criteria):
        # First get the exact matches, store the unmatched artists, as they
        # will need to be sorted later to get the best matches
        matched_artists, unmatched_artists = [], []
        for artist in artists:
            decorated_artist = relevanceutils.decorate_artist(artist,
                                                              age_criteria,
                                                              location_criteria,
                                                              rate_criteria,
                                                              gender_criteria)
            (matched_artists if relevanceutils.is_exact_match(artist) else unmatched_artists).append(decorated_artist)

        # If there are fewer than the mininum number of matches returned,
        # then we can draw from a wider pool. This works by sorting the
        # unmatched list first by the highest weight criteria, then by each
        # of the lesser weighted criteria.
        #
        # The order of this list will then be the order that we want to include
        # in the list returned to the user 

        if(len(matched_artists) < MIN_RETURN_VALUE):
            sorter_list = relevanceutils.SorterList(sorter_dict)
            if(age_criteria is not None):
                sorter_list.add_weight('age', age_criteria.weight)
            if(location_criteria is not None):
                sorter_list.add_weight('location', location_criteria.weight)
            if(rate_criteria is not None):
                sorter_list.add_weight('rate', rate_criteria.weight)
            if(gender_criteria is not None):
                sorter_list.add_weight('gender', gender_criteria.weight)

            sorted_artists = sorter_list.sort(unmatched_artists)

            # Only append enough items to make up the minimum value
            artists_to_add = MIN_RETURN_VALUE - len(matched_artists)
            matched_artists.extend(sorted_artists[:artists_to_add])

        return matched_artists

    def apply(self, artists, age_criteria, location_criteria,
              rate_criteria, gender_criteria):
        artists_list = artists['artists']
        filtered_artists = self.filter_artists(artists_list,
                                               age_criteria,
                                               location_criteria,
                                               rate_criteria,
                                               gender_criteria)


        artists_dict = { 'artists' : filtered_artists }

        return artists_dict 