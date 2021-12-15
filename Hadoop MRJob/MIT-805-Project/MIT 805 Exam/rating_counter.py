from mrjob.job import MRJob
from mrjob.step import MRStep

class MostRatedMovie(MRJob):

    def mapper(self, _, line):
        (movieID) = line.split('\t')[1]
        yield movieID, 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MostRatedMovie.run()
