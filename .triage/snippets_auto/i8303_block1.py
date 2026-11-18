    @av._output_format
    @av._call_api_on_func
    def get_daily_adjusted(self, symbol, outputsize='compact'):
        _FUNCTION_KEY = "TIME_SERIES_DAILY_ADJUSTED"
        return _FUNCTION_KEY, 'Time Series (Daily)', 'Meta Data'
