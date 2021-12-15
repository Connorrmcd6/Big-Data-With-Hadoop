from mrjob.job import MRJob
from datetime import datetime

class Time(MRJob):

    def mapper(self, _, line):
        time = line.split('\t')[3]
        time = datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d')
        yield str(time), 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    Time.run()
