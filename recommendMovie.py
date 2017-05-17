import codecs 
from math import sqrt


def loadMovieDB(path=''):
    users={}
    movieMessage={}
    userMes=[]

    i = 0
    j = 0

    f = codecs.open(path + "Movie_Ratings.csv", 'r', 'utf-8')
 
    for line in f:
        i += 1
        recommend=[]
        if i==1:
            userMessage = line.split(',')
            userMessage.pop(0)
            for user in userMessage:
                user = user.strip('"').strip('\n').encode('utf-8')
                userMes.append(user)
        else:
            movieLineMes = line.split(',')            
            name = movieLineMes[0].strip('"').encode('utf-8')
            recommdList=movieLineMes[1:]
            for re in recommdList:
                re = re.strip('"').strip('\n')
                if re=='':
                    recommend.append('')
                else:
                    re=float(re)
                    recommend.append(re)
            movieMessage.setdefault(name,recommend)
    f.close()
    
    for user in userMes:
        for name,recommends in movieMessage.items():
            if recommends[j] == '':
                continue
            else:
                users.setdefault(user,{})[name]=recommends[j]
        j += 1
    return users

users=loadMovieDB('/home/feishuoren/wingPy/')

class recommender:

    def __init__(self, data, k=1, metric='pearson', n=5):
        """ initialize recommender
        currently, if data is dictionary the recommender is initialized
        to it.
        For all other data types of data, no initialization occurs
        k is the k value for k nearest neighbor
        metric is which distance formula to use
        n is the maximum number of recommendations to make"""
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        # for some reason I want to save the name of the metric
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        #
        # if data is dictionary set recommender data to it
        #
        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):
        """Given product id number return product name"""
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id


    def userRatings(self, id, n):
        """Return n top ratings for user with id"""
        print ("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v)
                   for (k, v) in ratings]
        # finally sort and return
        ratings.sort(key=lambda artistTuple: artistTuple[1],
                     reverse = True)
        ratings = ratings[:n]
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))
                     
        
    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator


    def computeNearestNeighbor(self, username):
        """creates a sorted list of users based on their distance to
        username"""
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username],
                                   self.data[instance])
                distances.append((instance, distance))
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1],
                       reverse=True)
        return distances

    def recommend(self, user):
        """Give list of recommendations"""
        recommendations = {}
        # first get list of users  ordered by nearness
        nearest = self.computeNearestNeighbor(user)
        #
        # now get the ratings for the user
        #
        userRatings = self.data[user]
        #
        # determine the total distance
        totalDistance = 0.0
        for i in range(self.k):
            totalDistance += nearest[i][1]
        # now iterate through the k nearest neighbors
        # accumulating their ratings
        for i in range(self.k):
           # compute slice of pie 
            weight = nearest[i][1] / totalDistance
            # get the name of the person
            name = nearest[i][0]
            # get the ratings for this person
            neighborRatings = self.data[name]
            # get the name of the person
            # now find bands neighbor rated that user didn't
            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist]
                                                   * weight)
                    else:
                        recommendations[artist] = (recommendations[artist]
                                                   + neighborRatings[artist]
                                                   * weight)
        # now make list from dictionary
        recommendations = list(recommendations.items())
        recommendations = [(self.convertProductID2name(k), v)
                           for (k, v) in recommendations]
        # finally sort and return
        recommendations.sort(key=lambda artistTuple: artistTuple[1],
                             reverse = True)
        # Return the first n items
        return recommendations[:self.n]


    ##>>> r = recommender(users)
    ##>>> r.recommend('Zak')
    #[('Jaws', 3.0)]

