from argparse import ArgumentParser

def parse_args(num = True):
    '''
    To add command line arguments when running an analysis file

    
    :param num: When analysing outputs related to the numerics
    '''
    
    if num:
        #---- For numerical analysis ----#
        parser = ArgumentParser(fromfile_prefix_chars='@')

        parser.add_argument("-e", "--exp", dest="exp",
                            help="Experiment to read data from")
        
        parser.add_argument('-n', '--numerics', dest = 'num', 
                            help = 'Analysing the numerics, true or false.')
        
        parser.add_argument('-v', '--velocity', dest = 'vel', 
                            help = 'Plotting the velocity, set to true or false.')
        
        parser.add_argument('-g', '--grid', dest = 'grid', 
                            help = 'The grid on which the data is on, C or B.')
        
        parser.add_argument('-r', '--res', dest = 'res', 
                            help = 'set to true to analyse the residuals spatially ')

        parser.add_argument('-s', '--solver', dest = 'solver', 
                            help = 'solver used in exp')
        
        parser.add_argument('-p', '--precond', dest = 'precond', 
                            help = 'Was a precond used in the run, True or False')
        
        parser.add_argument('-P', '--precondname', dest = 'precondname', 
                            help = 'name of the precond used in the run')
        
        
        args = parser.parse_args()

    return args
