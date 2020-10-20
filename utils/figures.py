
class Figure:
    def __init__(self):
        self.figures = {
            'total': 0,
            'discharged': 0,
            'deaths': 0,
            'critical': 0
        }
    
    def read_file(self):
        pass
    
    def read_file_v1(self, file):
        '''
        '''

        with open(file, 'r') as f:
            previous_total = int(f.readline())
            previous_recovered = int(f.readline())

    def set_new(self, n, type):
        '''
        '''

        pass
    
    def set_new_confirmed(self, n):
        '''
        '''

        pass
    
    def set_new_recovered(self, n):
        pass

    def set_total(self, n, figure_type):
        '''
        Set the total number of confirmed cases.
        '''
        
        assert n >= self.figures[figure_type], 'Today\'s total confirmed figure must be equal to or higher than yesterday!'
        difference = n - self.figures[figure_type]
        self.figures[figure_type] = n

        return difference
    
    def set_total_recovered(self, n):
        '''
        '''
        pass

    def get_n_recovered(self):
        return 0
    