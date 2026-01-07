import numpy as np

class TimeUtility:

    def __init__(self, configuration_time = None, 
                    configuration_fig = None):
        
        self.dt = int(configuration_time['dt'])
        self.outputdir = int(configuration_fig['outputdir'])

