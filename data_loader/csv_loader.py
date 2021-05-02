# csv_loader.py

class CSV_loader():
    '''
    The Data Loader Class for CSV files.
    The input to class is the file_path of CSV file.
    It generates a ITERATOR, which can provide next row of CSV
    on every 'next' call

    Arguments:
        file_path - The path fo the CSV file.
    '''
    def __init__(self, file_path):
        self.path = file_path
        self._data = self._csv_reader()

    def _csv_reader(self):
        '''
        Generator Function which yields successive rows on calling next
        '''
        with open(self.path) as csv_file:
            yield from csv_file

    def __iter__(self):
        return self

    def __next__(self):
        '''
        Using next() on class object will call this, and this will internally call
        next method on our generator csv_reader
        '''
        return next(self._data).strip()