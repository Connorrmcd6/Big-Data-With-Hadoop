from mrjob.job import MRJob

class MRRatingByEvent(MRJob):

    def mapper(self, _, line):
        rating = line.split(',')[6]
        event = line.split(',')[0].strip().replace(' ','_')
        yield event, float(rating)

    def reducer(self, event, rating):
        total = 0
        numElements = 0
        for i in rating:
            total += i
            numElements += 1
            
        yield event, int(round(total / numElements,0))


if __name__ == '__main__':
    MRRatingByEvent.run()


'''
Run this in terminal to get results

python3 "MapReduce Jobs"/"Player Skill Analysis"/average_rating_by_event.py "MapReduce Jobs"/datasets/data.csv> Results/average_rating_by_event.csv

'''