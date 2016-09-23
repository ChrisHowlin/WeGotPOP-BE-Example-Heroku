from tg import expose, TGController
from tg.decorators import validate
from tg.validation import Convert
import unittest
from formencode import validators
from controllers.validators import AgeValidation, LocationValidation, RateValidation, GenderValidation
from controllers import BasicRelevanceStrategy,\
                        RelaxedRelevanceStrategy,\
                        BlendedRelevanceStrategy,\
                        ArtistFileService

strategy_dict = { 'basic' : BasicRelevanceStrategy.BasicRelevanceStrategy,
                  'relaxed' : RelaxedRelevanceStrategy.RelaxedRelevanceStrategy,
                  'blended' : BlendedRelevanceStrategy.BlendedRelevanceStrategy }

class RootController(TGController):

    def __init__(self, artist_service):
        self.artist_service = artist_service

    @expose()
    def index(self):
        pass

    # It may be possible to validate the arguments with @validate here
    @expose('json')
    def artists(self, age_min=None, age_max=None, age_wgt=None,
                     loc_lat=None, loc_lon=None, loc_rad=None, loc_wgt=None,
                     rate_max=None, rate_wgt=None,
                     gender=None, gender_wgt=None,
                     relevance='basic'):
        validated_age = AgeValidation.validate_age(age_min, age_max, age_wgt)
        validated_location = LocationValidation.validate_location(loc_lat,
                                                                  loc_lon,
                                                                  loc_rad,
                                                                  loc_wgt)
        validated_rate = RateValidation.validate_rate(rate_max, rate_wgt)
        validated_gender = GenderValidation.validate_gender(gender, gender_wgt)

        # Use service 
        artists = self.artist_service.get_artists()

        strategy = strategy_dict[relevance]
        filtered_artists = strategy().apply(artists,
                                            validated_age,
                                            validated_location,
                                            validated_rate, 
                                            validated_gender)

        return filtered_artists

class TestAgentGetResponse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        service = ArtistFileService.ArtistFileService('artists.json')
        cls.testController = RootController(service)

    def test_response_no_args(self):
        self.assertEqual(None, self.testController.artists())

    def test_response_age_args(self):
        self.assertEqual(None, self.testController.artists(age_min = '50', age_max = '60', age_wgt = '1'))

    def test_response_location_args(self):
        self.assertEqual(None, self.testController.artists(loc_lat = '50', loc_lon = '0.1', loc_rad = '100', loc_wgt = '1'))

    def test_response_rate_args(self):
        self.assertEqual(None, self.testController.artists(rate_max = '20', rate_wgt = '1'))

    def test_response_gender_args(self):
        self.assertEqual(None, self.testController.artists(gender = 'M', gender_wgt = '1'))

if __name__ == '__main__':
    unittest.main()
