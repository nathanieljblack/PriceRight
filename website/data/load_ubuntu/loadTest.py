import datetime
from load import LoadData

if __name__ == "__main__":
    date = datetime.date.today()
    ld = LoadData()
    ld.load('both', 'T', 'T', '2015-03-19', '2015-03-20')

