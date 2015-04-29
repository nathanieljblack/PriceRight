from mrjob.job import MRJob
from cleanData import CleanData
import datetime

class MRFileMapper(MRJob):

    def mapper(self, line_no, line):
        #call the pipeline
        date = datetime.date.today()
        date = datetime.date(2015, 3, 21)
        jf = ''.join([line, '.json'])
        p = CleanData()
        status = p.map(jf, str(date))
        yield status, 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == "__main__":
    MRFileMapper.run()

