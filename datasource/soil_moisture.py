class SoilMoistureDataSource:
    """
    A datasource for soil moisture, backed by an MCP3008 ADC channel
    """
    def __init__(self, mcp, adc_channel, dry_adc, wet_adc, min_valid_adc=0, max_valid_adc=1023):
        self.mcp = mcp
        self.adc_channel = adc_channel
        self.dry_adc = dry_adc
        self.wet_adc = wet_adc
        self.min_valid_adc = min_valid_adc
        self.max_valid_adc = max_valid_adc

    def read(self):
        """
        :return: (raw_adc, moisture_percent). moisture_percent is None if the raw reading is
                 missing, outside [min_valid_adc, max_valid_adc], or the sensor hasn't been
                 calibrated (dry_adc == wet_adc) -- this is the fail-safe fault signal that
                 pump logic must treat as "stop/stay off".
        """
        raw_adc = self.mcp.read_adc(self.adc_channel)

        if raw_adc is None or not (self.min_valid_adc <= raw_adc <= self.max_valid_adc):
            return raw_adc, None

        if self.dry_adc == self.wet_adc:
            return raw_adc, None

        percent = 100.0 * (self.dry_adc - raw_adc) / (self.dry_adc - self.wet_adc)
        return raw_adc, max(0.0, min(100.0, percent))
