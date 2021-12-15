from mrjob.job import MRJob
from mrjob.step import MRStep
from math import sqrt

from itertools import combinations

class OpeningSimilarities(MRJob):

    def configure_options(self):
        super(OpeningSimilarities, self).configure_options()
        self.add_file_option('--openings', help='Path to openings.csv')

    def load_opening_names(self):
        # Load database of movie names.
        self.openingNames = {}

        with open("openings.csv", encoding='ascii', errors='ignore') as f:
            for line in f:
                fields = line.split(',')
                self.openingNames[int(fields[0])] = fields[1]

    def steps(self):
        return [
            MRStep(mapper=self.mapper_parse_input,
                    reducer=self.reducer_ratings_by_user),
            MRStep(mapper=self.mapper_create_item_pairs,
                    reducer=self.reducer_compute_similarity),
            MRStep(mapper=self.mapper_sort_similarities,
                    mapper_init=self.load_opening_names,
                    reducer=self.reducer_output_similarities)]

    def mapper_parse_input(self, key, line):
        # Outputs userID => (movieID, rating)
        userID = line.split(',')[15]
        openingID = line.split(',')[16]
        rating = line.split(',')[6]
        yield  userID, (openingID, float(rating))

    def reducer_ratings_by_user(self, user_id, itemRatings):
        #Group (item, rating) pairs by userID

        ratings = []
        for openingID, rating in itemRatings:
            ratings.append((openingID, rating))

        yield user_id, ratings

    def mapper_create_item_pairs(self, user_id, itemRatings):
        # Find every pair of movies each user has seen, and emit
        # each pair with its associated ratings

        # "combinations" finds every possible pair from the list of movies
        # this user viewed.
        for itemRating1, itemRating2 in combinations(itemRatings, 2):
            openingID1 = itemRating1[0]
            rating1 = itemRating1[1]
            openingID2 = itemRating2[0]
            rating2 = itemRating2[1]

            # Produce both orders so sims are bi-directional
            yield (openingID1, openingID2), (rating1, rating2)
            yield (openingID2, openingID1), (rating2, rating1)


    def cosine_similarity(self, ratingPairs):
        # Computes the cosine similarity metric between two
        # rating vectors.
        numPairs = 0
        sum_xx = sum_yy = sum_xy = 0
        for ratingX, ratingY in ratingPairs:
            sum_xx += ratingX * ratingX
            sum_yy += ratingY * ratingY
            sum_xy += ratingX * ratingY
            numPairs += 1

        numerator = sum_xy
        denominator = sqrt(sum_xx) * sqrt(sum_yy)

        score = 0
        if (denominator):
            score = (numerator / (float(denominator)))

        return (score, numPairs)

    def reducer_compute_similarity(self, openingPair, ratingPairs):
        # Compute the similarity score between the ratings vectors
        # for each movie pair viewed by multiple people

        # Output movie pair => score, number of co-ratings

        score, numPairs = self.cosine_similarity(ratingPairs)

        # Enforce a minimum score and minimum number of co-ratings
        # to ensure quality
        if (numPairs > 100 and score > 0.95):
            yield openingPair, (score, numPairs)

    def mapper_sort_similarities(self, openingPair, scores):
        # Shuffle things around so the key is (movie1, score)
        # so we have meaningfully sorted results.
        score, n = scores
        movie1, movie2 = openingPair

        yield (self.openingNames[int(movie1)], score), \
            (self.openingNames[int(movie2)], n)

    def reducer_output_similarities(self, openingScore, similarN):
        # Output the results.
        # Movie => Similar Movie, score, number of co-ratings
        opening1, score = openingScore
        for opening2, n in similarN:
            yield opening1, (opening2, score, n)


if __name__ == '__main__':
    OpeningSimilarities.run()

'''
python3 "MapReduce Jobs"/"Opening Similarity Analysis"/similar_openings.py --openings="Recomender Data"/openings.csv "Recomender Data"/data100k.csv > Results/similarity.csv

'''