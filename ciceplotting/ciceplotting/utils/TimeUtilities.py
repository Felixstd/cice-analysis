import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class TimeUtility:

    def __init__(self, configuration_time = None):
        
        self.dt = int(configuration_time['dt'])
        self.startdate = str(configuration_time['startdate'])
        self.enddate = str(configuration_time['enddate'])
        self.freq = str(configuration_time['freq'])

    def setup_time(self):
        
        start = datetime.strptime(self.startdate, self.freq)
        end = datetime.strptime(self.enddate, self.freq)

        dates = self.dates_list(start,end,self.freq)

        return dates
    
    def infer_step(self, fmt):

        if '%d' in fmt:
            return timedelta(days = 1)
        
        elif '%m' in fmt:
            return relativedelta(months=1)
        
        elif '%Y' in fmt:
            return relativedelta(years=1)
        
        else:
            return 'unknown'

    def dates_list(self, start_date, end_date, freq):

        step = self.infer_step(freq)
        
        dates = []
        current = start_date
        while current <= end_date:
            dates.append(current.strftime(freq))
            current += step

        return dates
    




