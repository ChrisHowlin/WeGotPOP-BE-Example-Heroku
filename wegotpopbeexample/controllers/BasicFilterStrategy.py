import geopy.distance

class BasicFilterStrategy:
    def filter(self, artists, age_data, location_data, rate_data, gender_data):
        artists_list = artists['artists']
        print('Filter before: %s' % len(artists_list))

        if(age_data is not None):
            print('Age filtering')
            if(age_data.min is not None):
                artists_list = list(filter(lambda x: x['age'] >= age_data.min, artists_list))
            if(age_data.max is not None):
                artists_list = list(filter(lambda x: x['age'] <= age_data.max, artists_list))

        if(location_data is not None):
            print('Location filtering')
            search_location = (location_data.lat, location_data.lon)
            artists_list = list(filter(lambda x: geopy.distance.distance(search_location,
                                                                   (x['latitude'], x['longitude'])).miles <= location_data.radius, artists_list))

        if(rate_data is not None):
            print('Rate filtering')
            artists_list = list(filter(lambda x: x['rate'] <= rate_data.rate, artists_list))

        if(gender_data is not None):
            print('Gender filtering')
            artists_list = list(filter(lambda x: x['gender'] == gender_data.gender, artists_list))

        print('Filter after: %s' % len(artists_list))

        filtered_artists = { 'artists' : artists_list }

        return filtered_artists