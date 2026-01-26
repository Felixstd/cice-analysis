class namelist:

    def __init__(self, configuration_exp = None, 
                    configuration_dyn = None, 
                    configuration_num = None, 
                    configuration_fig = None, 
                    configuration_time = None):
        
        
        # ---- Experiment settings ----- #
                
        self.exp = [str(x) for x in configuration_exp['exp'].split(',')]
        self.case = str(configuration_exp['case'])
        self.plotfields = int(configuration_exp['plot_fields'])
        self.read_all = int(configuration_exp['read_all'])
        self.plotsingle = int(configuration_exp['plot_single'])

        #----- Dynamical Settings ------#

        self.ks  = int(configuration_dyn['kstrength'])
        self.grid       = str(configuration_dyn['gridtype'])
        self.var        = str(configuration_dyn['var'])
        self.dx         = float(configuration_dyn['dx'])


        #------ numerical settings ------#
        self.solver     = str(configuration_num['solver'])
        self.imex       = int(configuration_num['imex'])
        self.Global     = int(configuration_num['global'])


        self.datadir = str(configuration_fig['datadir'])
        self.figdir    = str(configuration_fig['figdir'])


        self.dt = float(configuration_time['dt'])
        self.datestr = str(configuration_time['datestr'])
        self.startdate = str(configuration_time['startdate'])
        self.enddate = str(configuration_time['enddate'])
        self.freq = str(configuration_time['freq'])