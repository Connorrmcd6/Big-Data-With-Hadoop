from mrjob.job import MRJob

class MREventCounter(MRJob):
    def mapper(self, key, line):
        event = line.split(',')[0].strip().replace(' ','_')
        yield event, 1

    def reducer(self, opening, occurences):
        yield opening, sum(occurences)

if __name__ == '__main__':
    MREventCounter.run()


'''
Run this in terminal to get results

python3 "MapReduce Jobs"/"Opening Efficiency Analysis"/event_counter.py "MapReduce Jobs"/datasets/data.csv > Results/event_counter.csv

'''