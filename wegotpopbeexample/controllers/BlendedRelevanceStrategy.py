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

def decorate_with_combined_score(artist, age_criteria, location_criteria, rate_criteria, gender_criteria):
    # Some made up normalisation factors
    age_norm = 1
    rate_norm = 1
    location_norm = 0.5
    gender_norm = 10

    age_score = 0
    if(age_criteria is not None):
        age_score = 1/age_criteria.weight * age_norm * artist['age_distance']

    location_score = 0
    if(location_criteria is not None):
        location_score = 1/location_criteria.weight * location_norm * artist['location_distance']

    rate_score = 0
    if(rate_criteria is not None):
        rate_score = 1/rate_criteria.weight * rate_norm * artist['rate_distance']

    gender_score = 0
    if(gender_criteria is not None):
        gender_score = 1/gender_criteria.weight * gender_norm * artist['gender_distance']

    artist['combined_score'] = age_score + location_score + rate_score + gender_score

    return artist

class BlendedRelevanceStrategy:
    def filter_artists(self, artists, age_criteria, location_criteria, rate_criteria, gender_criteria):
        # First get the exact matches, store the unmatched artists, as they
        # will need to be sorted later to get the best matches
        decorated_artists = []
        for artist in artists:
            decorated_artist = relevanceutils.decorate_artist(artist,
                                                              age_criteria,
                                                              location_criteria,
                                                              rate_criteria,
                                                              gender_criteria)
            decorated_artist = decorate_with_combined_score(artist,
                                                            age_criteria,
                                                            location_criteria,
                                                            rate_criteria,
                                                            gender_criteria)
            decorated_artists.append(decorated_artist)

        sorted_artists = sorted(decorated_artists, key = lambda x: x['combined_score'])

        return sorted_artists[:MIN_RETURN_VALUE]

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