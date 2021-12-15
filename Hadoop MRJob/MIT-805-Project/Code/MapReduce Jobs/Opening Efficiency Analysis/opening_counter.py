from mrjob.job import MRJob

class MROpeningCounter(MRJob):
    def mapper(self, key, line):
        opening = line.split(',')[11].strip().replace(' ','_')
        yield opening, 1

    def reducer(self, opening, occurences):
        yield opening, sum(occurences)

if __name__ == '__main__':
    MROpeningCounter.run()


'''
Run this in terminal to get results

python3 "MapReduce Jobs"/"Opening Efficiency Analysis"/opening_counter.py "MapReduce Jobs"/datasets/data.csv > Results/opening_counter.csv

'''