import unittest

AGE_MIN = 16
AGE_MAX = 74

def validate_age(iMin, iMax, iWeight):
    '''A factory function that returns a ValidatedAge object. If either iMin
    or iMax is not None, then this guaranteed that both the ValidatedAge.min
    and ValidatedAge.max values will be set to the input value or the AGE_MIN
    or AGE_MAX values as appropriate. This guarantee ensures that you do not
    have to contintue to make None checks for half-defined ranges (i.e. those
    where either a min or a max is defined but not both'''

    aMin = iMin
    aMax = iMax
    aWeight = iWeight

    # First filter out any inputs which are not the correct type. If there is
    # an issue with the type check, set to None.
    try:
        if(aMin is not None):
            aMin = int(aMin)
    except ValueError:
        print('Age Validation: Min (%s) cannot be converted to integer, setting to None' % aMin)
        aMin = None

    try:
        if(aMax is not None):
            aMax = int(aMax)
    except ValueError:
        print('Age Validation: Max (%s) cannot be converted to integer, setting to None' % aMax)
        aMax = None

    try:
        if(aWeight is not None):
            aWeight = int(aWeight)
    except ValueError:
        print('Age Validation: Weight (%s) cannot be converted to integer, setting to None' % aWeight)
        aWeight = None

    # Check combinations of values, e.g. weight only makes sense if there is a
    # min or max
    if(aWeight is None):
        print('Age Validation: Min (%s) or Max (%s) provided but no aWeight (%s)' % (aMin, aMax, aWeight))
        return None

    if(aWeight is not None and (aMin is None and aMax is None)):
        print('Age Validation: Weight (%s) provided but no Min (%s) and no Max (%s)' % (aWeight, aMin, aMax))
        return None

    if(aWeight is None and aMin is None and aMax is None):
        print('Age Validation: No Min (%s), Max (%s) or Weight (%s)' % (aMin, aMax, aWeight))
        return None

    # Now that the types have been validated, to determine if the values are
    # sensible and sensiblize them otherwise.
    if(aMin is None):
        print('Age Validation: Min (%s) is None, setting to minimum age' % aMin)
        aMin = AGE_MIN

    if(aMin is None or (aMin < AGE_MIN)):
        print('Age Validation: Min (%s) less than AGE_MIN (%s), coercing to minimum age' % (aMin, AGE_MIN))
        aMin = AGE_MIN

    if(aMin > AGE_MAX):
        print('Age Validation: Min (%s) greater than AGE_MAX (%s), coercing to maximum age' % (aMin, AGE_MAX))
        aMin = AGE_MAX

    if(aMax is None):
        print('Age Validation: Max (%s) is None, setting to maximum age' % aMax)
        aMax = AGE_MAX

    if(aMax < AGE_MIN):
        print('Age Validation: Max (%s) less than AGE_MIN (%s), coercing to minimum age' % (aMax, AGE_MIN))
        aMax = AGE_MIN

    if(aMax > AGE_MAX):
        print('Age Validation: Max (%s) greater than AGE_MAX (%s), coercing to maximum age' % (aMax, AGE_MAX))
        aMax = AGE_MAX

    if(aMin > aMax):
        print('Age Validation: Max (%s) greater than Min (%s), setting to Min'% (aMax, aMin))
        aMax = aMin

    return ValidatedAge(aMin, aMax, aWeight)


class ValidatedAge:
    def __init__(self, min, max, weight):
        self.min = min
        self.max = max
        self.weight = weight

    def get_distance(self, age):
        if age < self.min:
            return self.min - age
        elif age > self.max:
            return age - self.max
        return 0

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

class TestValidateAge(unittest.TestCase):
    # Basic tests of type
    def test_min_text(self):
        self.assertEqual(None, validate_age('xyz', None, '1'))

    def test_max_text(self):
        self.assertEqual(None, validate_age(None, 'xyz', '1'))

    def test_weight_text(self):
        self.assertEqual(None, validate_age(None, '40', 'xyz'))

    # Some types are only valid in combination
    def test_min_max_no_weight(self):
        self.assertEqual(None, validate_age('0', '30', None))
    
    def test_weight_no_min_max(self):
        self.assertEqual(None, validate_age(None, None, '2'))

    def test_no_arguments(self):
        self.assertEqual(None, validate_age(None, None, None))

    # Testing values are handled correctly
    def test_valid_age_all_args(self):
        self.assertEqual(ValidatedAge(30, 40, 1), validate_age('30', '40', '1'))

    def test_valid_age_min_weight(self):
        self.assertEqual(ValidatedAge(30, AGE_MAX, 1), validate_age('30', None, '1'))

    def test_valid_age_max_weight(self):
        self.assertEqual(ValidatedAge(AGE_MIN, 40, 1), validate_age(None, '40', '1'))

    def test_min_age_corrected_to_min_allowed(self):
        self.assertEqual(ValidatedAge(AGE_MIN, AGE_MAX, 1), validate_age(AGE_MIN - 20, None, 1))

    def test_min_age_corrected_to_max_allowed(self):
        self.assertEqual(ValidatedAge(AGE_MAX, AGE_MAX, 1), validate_age(AGE_MAX + 20, None, 1))

    def test_max_age_corrected_to_min_allowed(self):
        self.assertEqual(ValidatedAge(AGE_MIN, AGE_MIN, 1), validate_age(None, AGE_MIN - 20, 1))

    def test_max_age_corrected_to_max_allowed(self):
        self.assertEqual(ValidatedAge(AGE_MIN, AGE_MAX, 1), validate_age(None, AGE_MAX + 20, 1))

    def test_min_greater_than_max_corrected(self):
        self.assertEqual(ValidatedAge(30, 30, 1), validate_age('30', '20', 1))

if __name__ == '__main__':
    unittest.main()