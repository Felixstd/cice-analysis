from argparse import ArgumentParser

def parse_args(num = True):
    '''
    To add command line arguments when running an analysis file

    
    :param num: When analysing outputs related to the numerics
    '''
    
    if num:
        #---- For numerical analysis ----#
        parser = ArgumentParser()
        parser.add_argument("-e", "--exp", dest="exp",
                            help="Experiment to read data from")

        args = parser.parse_args()

    return args
