from mrjob.job import MRJob

class MRPlayers(MRJob):

    def mapper(self, key, line):
        event = line.split(',')[0].strip().replace(' ','_')
        time = line.split(',')[5].split(':')[0]
        r = float(line.split(',')[6])
        rating = round(r, -2)


        yield (str(event), int(time), int(rating)), 1

    def reducer(self, keys, count):
        yield keys, sum(count)


if __name__ == '__main__':
    MRPlayers.run()


'''
Run this in terminal to get results

python3 "MapReduce Jobs"/"Player Distribution Analysis"/player_distribution.py "MapReduce Jobs"/datasets/data.csv > Results/player_distribution.csv

'''