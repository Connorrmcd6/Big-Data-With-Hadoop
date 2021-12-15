from mrjob.job import MRJob

class MRRatingByTime(MRJob):

    def mapper(self, _, line):
        rating = line.split(',')[6]
        time = line.split(',')[5].split(':')[0]
        yield int(time), float(rating)

    def reducer(self, time, rating):
        total = 0
        numElements = 0
        for i in rating:
            total += i
            numElements += 1
            
        yield time, int(round(total / numElements,0))


if __name__ == '__main__':
    MRRatingByTime.run()


'''
Run this in terminal to get results

python3 "MapReduce Jobs"/"Player Skill Analysis"/average_rating_by_time.py "MapReduce Jobs"/datasets/data.csv> Results/average_rating_by_time.csv

'''