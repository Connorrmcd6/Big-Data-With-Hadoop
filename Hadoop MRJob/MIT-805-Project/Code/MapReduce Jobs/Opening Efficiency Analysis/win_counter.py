from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np

class MREfficiency(MRJob):

    def mapper(self, key, line):
        opening = line.split(',')[11].strip().replace(' ','_')
        x = str(line.split(',')[3])

        if x == '1-0':
            outcome = 1
        else:
            outcome = 0
    

        yield str(opening), float(outcome)
    

    def reducer(self, key, value):
        opening = key
        wins = value
        yield opening, sum(wins)

 

if __name__ == '__main__':
    MREfficiency.run()


'''
Run this in terminal to get results

python3 "MapReduce Jobs"/"Opening Efficiency Analysis"/win_counter.py "MapReduce Jobs"/datasets/data.csv > Results/win_counter.csv

'''