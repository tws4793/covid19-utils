import camelot
from os import path
from glob import glob

def find_ext(dr, ext):
    return glob(path.join(dr,"*.{}".format(ext)))

files = find_ext('pdf', 'pdf')

for file in files:
    name = file.strip('pdf\.\/')
    print(file)
    tables = camelot.read_pdf(file, pages = '1-end', strip_text = '\n')
    print(len(tables))
    tables.export('out/' + name + '.csv', f = 'csv')