import unittest

VALID_GENDER = ['F', 'M']

def validate_gender(iGender, iWeight):

    if(not isinstance(iGender, (str))):
        print('Gender Validation: Gender (%s) not valid.' % iGender)
        return None

    try:
        if(iWeight is not None):
            iWeight = int(iWeight)
    except ValueError:
        print('Gender Validation: Weight (%s) cannot be converted to integer, setting to None' % iWeight)
        iWeight = None

    if(iWeight is None):
        print('Gender Validation: Weight (%s) is None, not setting weight' % (iWeight))
        return None

    if(not iGender in VALID_GENDER):
        print('Gender Validation: Gender (%s) not in list of valid gender (%s).' % (iGender, VALID_GENDER))
        return None

    return ValidatedGender(iGender, iWeight)

class ValidatedGender:
    def __init__(self, gender, weight):
        self.gender = gender
        self.weight = weight

    def get_distance(self, gender):
        if(self.gender == gender):
            return 0
        else:
            return 1

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
    def test_no_gender(self):
        self.assertEqual(None, validate_gender(None, '1'))

    def test_no_weight(self):
        self.assertEqual(None, validate_gender('F', None))

    def test_gender_number(self):
        self.assertEqual(None, validate_gender(1, '1'))

    def test_gender_male(self):
        self.assertEqual(ValidatedGender('M', 1), validate_gender('M', '1'))

    def test_gender_female(self):
        self.assertEqual(ValidatedGender('F', 1), validate_gender('F', '1'))

    def test_gender_invalid(self):
        self.assertEqual(None, validate_gender('cat', '1'))

if __name__ == '__main__':
    unittest.main()