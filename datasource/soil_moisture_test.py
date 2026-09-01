import unittest

from datasource.soil_moisture import SoilMoistureDataSource


class StubMCP:
    def __init__(self, value):
        self.value = value
        self.requested_channel = None

    def read_adc(self, channel):
        self.requested_channel = channel
        return self.value


class SoilMoistureDataSourceTest(unittest.TestCase):
    def test_reads_the_configured_channel(self):
        mcp = StubMCP(500)
        SoilMoistureDataSource(mcp, adc_channel=3, dry_adc=700, wet_adc=300).read()
        self.assertEqual(mcp.requested_channel, 3)

    def test_dry_boundary_is_zero_percent(self):
        source = SoilMoistureDataSource(StubMCP(700), adc_channel=0, dry_adc=700, wet_adc=300)
        raw, percent = source.read()
        self.assertEqual(raw, 700)
        self.assertEqual(percent, 0.0)

    def test_wet_boundary_is_hundred_percent(self):
        source = SoilMoistureDataSource(StubMCP(300), adc_channel=0, dry_adc=700, wet_adc=300)
        raw, percent = source.read()
        self.assertEqual(raw, 300)
        self.assertEqual(percent, 100.0)

    def test_midpoint_is_fifty_percent(self):
        source = SoilMoistureDataSource(StubMCP(500), adc_channel=0, dry_adc=700, wet_adc=300)
        _, percent = source.read()
        self.assertAlmostEqual(percent, 50.0)

    def test_reversed_calibration_polarity_still_works(self):
        # Some sensors report a *lower* ADC value when dry -- the mapping shouldn't assume
        # dry_adc > wet_adc.
        source = SoilMoistureDataSource(StubMCP(300), adc_channel=0, dry_adc=300, wet_adc=700)
        _, percent = source.read()
        self.assertEqual(percent, 0.0)

    def test_out_of_range_reading_is_a_fault(self):
        source = SoilMoistureDataSource(StubMCP(2000), adc_channel=0, dry_adc=700, wet_adc=300,
                                         min_valid_adc=0, max_valid_adc=1023)
        raw, percent = source.read()
        self.assertEqual(raw, 2000)
        self.assertIsNone(percent)

    def test_missing_reading_is_a_fault(self):
        source = SoilMoistureDataSource(StubMCP(None), adc_channel=0, dry_adc=700, wet_adc=300)
        raw, percent = source.read()
        self.assertIsNone(raw)
        self.assertIsNone(percent)

    def test_uncalibrated_sensor_is_a_fault(self):
        source = SoilMoistureDataSource(StubMCP(500), adc_channel=0, dry_adc=700, wet_adc=700)
        _, percent = source.read()
        self.assertIsNone(percent)

    def test_percent_is_clamped_within_calibrated_range(self):
        source = SoilMoistureDataSource(StubMCP(250), adc_channel=0, dry_adc=700, wet_adc=300,
                                         min_valid_adc=0, max_valid_adc=1023)
        _, percent = source.read()
        self.assertEqual(percent, 100.0)


if __name__ == '__main__':
    unittest.main()
