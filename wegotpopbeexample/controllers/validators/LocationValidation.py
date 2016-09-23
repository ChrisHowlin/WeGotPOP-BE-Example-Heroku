import unittest
import geopy.distance

LAT_MIN = -90.0
LAT_MAX = +90.0
LAT_DEFAULT = 51.5074

LON_MIN = -180.0
LON_MAX = 180.0
LON_DEFAULT = 0.1278

RADIUS_MIN = 0.5

def validate_location(iLat, iLon, iRadius, iWeight):
    aLat = iLat
    aLon = iLon
    aRadius = iRadius
    aWeight = iWeight

    # First filter out any inputs which are not the correct type. If there is
    # an issue with the type check, set to None.
    try:
        if(aLat is not None):
            aLat = float(aLat)
    except ValueError:
        print('Location Validation: Lat (%s) cannot be converted to float, setting to None' % aLat)
        aLat = None

    try:
        if(aLon is not None):
            aLon = float(aLon)
    except ValueError:
        print('Location Validation: Lat (%s) cannot be converted to float, setting to None' % aLon)
        aLon = None

    try:
        if(aRadius is not None):
            aRadius = float(aRadius)
    except ValueError:
        print('Location Validation: Radius (%s) cannot be converted to float, setting to None' % aRadius)
        aLat = None

    try:
        if(aWeight is not None):
            aWeight = int(aWeight)
    except ValueError:
        print('Location Validation: Weight (%s) cannot be converted to integer, setting to None' % aWeight)
        aWeight = None

    if(not (aLat is not None and aLon is not None)):
        print('Location Validation: Lat (%s) or Lon (%s) has None value, location invalid' % (aLat, aLon))
        return None

    if(aWeight is None):
        print('Location Validation: Min (%s), Max (%s) or Radius (%s) provided but no aWeight (%s)' % (aLat, aLon, aRadius, aWeight))
        return None

    # We are more relaxed on radius, if this is not provided or has a value
    # less than the minimum, we assign it the minimum value
    if(aRadius is None):
        print('Location Validation: No radius (%s) provided, setting to RADIUS_MIN (%s)' % (aRadius, RADIUS_MIN))
        aRadius = RADIUS_MIN
    
    if(aRadius < RADIUS_MIN):
        print('Location Validation: Radius (%s) is less than RADIUS_MIN (%s), setting to minimum' % (aRadius, RADIUS_MIN))
        aRadius = RADIUS_MIN

    if(not (LAT_MIN <= aLat <= LAT_MAX)):
        print ('Location Validation: Lat (%s) not valid range (%s, %s), seeting default location (%s, %s)' % (aLat, LAT_MIN, LAT_MAX, LAT_DEFAULT, LON_DEFAULT))
        aLat = LAT_DEFAULT
        aLon = LON_DEFAULT

    if(not (LON_MIN <= aLon <= LON_MAX)):
        print ('Location Validation: Lat (%s) not valid range (%s, %s), seeting default location (%s, %s)' % (aLon, LON_MIN, LON_MAX, LAT_DEFAULT, LON_DEFAULT))
        aLat = LAT_DEFAULT
        aLon = LON_DEFAULT

    return ValidatedLocation(aLat, aLon, aRadius, aWeight)

class ValidatedLocation:
    def __init__(self, lat, lon, radius, weight):
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.weight = weight

    def get_distance(self, lat, lon):
        search_location = (self.lat, self.lon)
        target_location = (lat, lon)
        distance = geopy.distance.distance(search_location,
                                           target_location).miles

        if(distance <= self.radius):
            return 0
        else:
            return (distance - self.radius)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

class TestValidateLocation(unittest.TestCase):
    # Basic tests of type
    def test_lat_text(self):
        self.assertEqual(None, validate_location('xyz', None, None, '1'))

    def test_lon_text(self):
        self.assertEqual(None, validate_location(None, 'xyz', None, '1'))

    def test_radius_text(self):
        self.assertEqual(None, validate_location(None, None, 'xyz', '1'))

    def test_weight_text(self):
        self.assertEqual(None, validate_location(None, '40.0', None, 'xyz'))

    # Some types are only valid in combination
    def test_lat_lon_rad_no_weight(self):
        self.assertEqual(None, validate_location('0.0', '30.0', '1.0', None))
    
    def test_weight_no_lat_lon(self):
        self.assertEqual(None, validate_location(None, None, None, '2'))

    def test_no_arguments(self):
        self.assertEqual(None, validate_location(None, None, None, None))

    def test_missing_lat(self):
        self.assertEqual(None, validate_location(None, '40.0', '2.0', '1'))

    def test_missing_lon(self):
        self.assertEqual(None, validate_location('40.0', None, '2.0', '1'))

    # Testing values are handled correctly
    def test_valid_age_all_args(self):
        self.assertEqual(ValidatedLocation(30.0, 40.0, 2.0, 1),
                         validate_location('30.0', '40.0', '2.0', '1'))

    def test_default_radius(self):
        self.assertEqual(ValidatedLocation(30.0, 40.0, RADIUS_MIN, 1),
                         validate_location('30.0', '40.0', None, '1'))

    def test_invalid_radius(self):
        self.assertEqual(ValidatedLocation(30.0, 40.0, RADIUS_MIN, 1),
                         validate_location('30.0', '40.0', '-5.0', '1'))        

    # Test that if lat/lon are non-sensical that defaul location is used
    def test_invalid_lat_under(self):
        self.assertEqual(ValidatedLocation(LAT_DEFAULT, LON_DEFAULT, 2.0, 1),
                         validate_location('-400.0', '40.0', '2.0', '1'))

    def test_invalid_lat_above(self):
        self.assertEqual(ValidatedLocation(LAT_DEFAULT, LON_DEFAULT, 2.0, 1),
                         validate_location('400.0', '40.0', '2.0', '1'))

    def test_invalid_lon_under(self):
        self.assertEqual(ValidatedLocation(LAT_DEFAULT, LON_DEFAULT, 2.0, 1),
                         validate_location('40.0', '-400.0', '2.0', '1'))

    def test_invalid_lon_above(self):
        self.assertEqual(ValidatedLocation(LAT_DEFAULT, LON_DEFAULT, 2.0, 1),
                         validate_location('40.0', '400.0', '2.0', '1'))

class TestDistance(unittest.TestCase):
    def test_equal_distance(self):
        loc = ValidatedLocation(LAT_DEFAULT, LON_DEFAULT, 2.0, 1)
        test = (LAT_DEFAULT, LON_DEFAULT)
        self.assertEqual(loc.get_distance(test[0], test[1]),
                         0)

    def test_not_equal_within_radius(self):
        loc = ValidatedLocation(51.75436293, -0.09998975, 2.0, 1)
        test = (51.55587162, 0.13083594)
        self.assertEqual(loc.get_distance(test[0], test[1]),
                         0)

if __name__ == '__main__':
    unittest.main()