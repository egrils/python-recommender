import codecs 
from math import sqrt

users = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "maxi": {"PSY": 3.5, "Whitney Houston": 4},
          "lyl": {"Taylor Swift": 5, "Whitney Houston": 3}}


class recommender:
    def __init__(self, data):

        if type(data).__name__ == 'dict':
            self.data = data
            
        self.frequencies = {}
        self.deviations = {}
    
    def loadMovieDB(self,path='/home/feishuoren/wingPy/'):
        self.data = {}
        i = 0
        u_rating = {}
        f = codecs.open(path + "Movie_Ratings.csv", 'r', 'utf8')
        for line in f:
            i = i + 1
            if i == 1:
                group = line.split(',')
                group.pop(0)
                user_ids = []
                for user in group:
                    user = user.strip('"').strip('"\n')
                    user_ids.append(user)
                    u_rating[user] = {}
            else:
                next_line = line.split(',')
                movie_name = next_line.pop(0).strip('"')
                scores = {}
                array = []
                for k in next_line:
                    k = k.strip().strip('\n')
                    array.append(k)
                scores[movie_name] = array
                for n in user_ids:
                    index = user_ids.index(n)
                    if scores[movie_name][index] == '':
                        continue
                    else:
                        u_rating[n].update({movie_name: float(scores[movie_name][index])})
                        self.data[n] = u_rating[n]
        f.close()    
    def computeDeviations(self):
        # 获取每位用户的评分数据
        for ratings in self.data.values():
            # 对于该用户的每个评分项（歌手、分数）
            for (item, rating) in ratings.items():
                self.frequencies.setdefault(item, {})
                self.deviations.setdefault(item, {})
                # 再次遍历该用户的每个评分项
                for (item2, rating2) in ratings.items():
                    if item != item2:
                        # 将评分的差异保存到变量中
                        self.frequencies[item].setdefault(item2, 0)
                        self.deviations[item].setdefault(item2, 0.0)
                        self.frequencies[item][item2] += 1
                        self.deviations[item][item2] += rating - rating2
        print 'self.frequencies1:{}\n'.format(self.frequencies)
        print 'self.deviations1:{}\n'.format(self.deviations)
    
        for (item, ratings) in self.deviations.items():
            for item2 in ratings:
                ratings[item2] /= self.frequencies[item][item2]  
                
        print 'self.deviations2:{}\n'.format(self.deviations)

    def slopeOneRecommendations(self, userRatings):
        recommendations = {}
        frequencies = {}
        # 遍历目标用户的评分项（歌手、分数）
        for (userItem, userRating) in userRatings.items():
            # 对目标用户未评价的歌手进行计算
            for (diffItem, diffRatings) in self.deviations.items():
                if diffItem not in userRatings and userItem in self.deviations[diffItem]:
                    freq = self.frequencies[diffItem][userItem]
                    recommendations.setdefault(diffItem, 0.0)
                    frequencies.setdefault(diffItem, 0)
                    # 分子
                    recommendations[diffItem] += (diffRatings[userItem] + userRating) * freq
                    # 分母
                    frequencies[diffItem] += freq
    
        recommendations = [(k, v / frequencies[k]) for (k, v) in recommendations.items()]
        
        # 排序并返回
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        
        print 'recommendations:{}\n'.format(recommendations)
        
        return recommendations

r = recommender(users)
r.computeDeviations()
r.slopeOneRecommendations(users['lyl'])


## movie    
r = recommender(0)
r.loadMovieDB()

 
score = {'You Got Mail': 3.0, 'Star Wars': 5.0, 'Pulp Fiction': 5.0, 'Braveheart': 4.0, 'Kazaam': 1.0, 'The Matrix': 5.0, 'Blade Runner': 5.0, 'The Happening': 2.0, 'Pootie Tang': 1.0, 'Snakes on a Plane': 3.0}

r.computeDeviations()
r.slopeOneRecommendations(score)
