import unittest

RATE_MIN = 10.0  # Taken from spec email
RATE_MAX = 39.97 # Taken from spec email

def validate_rate(iRateMax, iWeight):
    aRateMax = iRateMax
    aWeight = iWeight

    try:
        if(aRateMax is not None):
            aRateMax = float(aRateMax)
    except ValueError:
        print('Rate Validation: Rate Max (%s) cannot be converted to float, setting to None' % aRateMax)
        aRateMax = None

    try:
        if(aWeight is not None):
            aWeight = int(aWeight)
    except ValueError:
        print('Rate Validation: Weight (%s) cannot be converted to integer, setting to None' % aWeight)
        aWeight = None

    if(aRateMax is None):
        print('Rate Validation: Rate Max (%s) is None, not setting rate' % (aRateMax))
        return None

    if(aWeight is None):
        print('Rate Validation: Weight (%s) is None, not setting weight' % (aWeight))
        return None

    if(not(RATE_MIN <= aRateMax <= RATE_MAX)):
        print('Rate Validation: Rate (%s) not in range (%s, %s), setting within range.' % (aRateMax, RATE_MIN, RATE_MAX))
        aRateMax = min(max(aRateMax, RATE_MIN), RATE_MAX)

    return ValidatedRate(aRateMax, aWeight)

class ValidatedRate:
    def __init__(self, rate, weight):
        self.rate = rate
        self.weight = weight

    def get_distance(self, rate):
        if(rate <= self.rate):
            return 0.0
        else:
            return (rate - self.rate)

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
    def test_no_rate(self):
        self.assertEqual(None, validate_rate(None, '1'))

    def test_no_weight(self):
        self.assertEqual(None, validate_rate('50', None))

    def test_rate_text(self):
        self.assertEqual(None, validate_rate('xyz', '1'))

    def test_rate_under(self):
        self.assertEqual(ValidatedRate(RATE_MIN, 1), validate_rate('0.0', '1'))

    def test_rate_above(self):
        self.assertEqual(ValidatedRate(RATE_MAX, 1), validate_rate('100.0', '1'))

if __name__ == '__main__':
    unittest.main()