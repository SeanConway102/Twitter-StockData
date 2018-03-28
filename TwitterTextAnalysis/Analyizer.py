import os
import ast
import tweepy
import pysentiment as ps


configfile = './settings/config.txt'
class Analyizer:
    info={}
    auth = None
    api = None
    authenticated=False
    def __init__(self):
        global configfile
        if os.path.exists(configfile):
            with open(configfile,'r')as conf:
                self.info = ast.literal_eval(conf.read())
            if self.authenticated==False:
                authenticated=self.authenticate()
        else:
            self.initconfig()
    def initconfig(self):
        self.info={}
        self.info['key']=input("Enter your Key: ")
        self.info['secret']=input("Enter your secert: ")
        self.info['token']=input("Enter your token: ")
        self.info['tsecret']=input("Enter your token secert: ")
        if os.path.exists('./settings')==False: os.mkdir('settings')
        with open(configfile, 'a')as conf:
            conf.write(str(self.info))
    def authenticate(self):
        print('Authenticating')
        #try:
        self.auth = tweepy.OAuthHandler(self.info['key'], self.info['secret'])
        self.auth.set_access_token(self.info['token'], self.info['tsecret'])
        self.api = tweepy.API(self.auth)
        return True
        #except:
        #    return False
    #Get a number of tweets with key words(query)
    def search(self,query, count=100):
        max_tweets = count
        return [status for status in tweepy.Cursor(self.api.search, q=query).items(max_tweets)]
    #Return a list of all significant sentiment scores, all that do not equal zero
    def getallsentiment(self,tweets):
        scores = []
        for tweet in tweets:
            analyizer = ps.HIV4()
            tokens = analyizer.tokenize(tweet.text)
            score = analyizer.get_score(tokens)
            if score['Polarity'] != 0:
                scores += [score]
        return scores
    #Get a single sentiment score for all tweets in a list
    def getgeneralsentiment(self,tweets):
        return self.__mergescores(self.getallsentiment(tweets))
    #Merge multiple sentiment scores into one
    def __mergescores(self,scores):
        keys = ['Positive', 'Negative', 'Polarity', 'Subjectivity']
        newscore = {}
        for key in keys:
            newscore[key] = 0
        for item in scores:
            for key in keys:
                newscore[key] += item[key]
        newscore['Polarity'] = newscore['Polarity'] / len(scores)
        newscore['Subjectivity'] = newscore['Subjectivity'] / len(scores)
        return newscore
    def savetweets(self,tweets,path,name):
        if os.path.exists(path+'/tweets')==False: os.mkdir(path+'/tweets')
        with open(path+'/tweets/'+name, 'a')as file:
            file.write(str(tweets))
    def savescores(self,scores,path,name):
        if os.path.exists(path+'/scores')==False: os.mkdir(path+'/scores')
        with open(path+'/scores/'+name, 'a')as file:
            file.write(str(scores))
    def loadtweets(self,path,name):
        try:
            with open('tweets_'+name, 'r')as file:
                return ast.literal_eval(file.read())
        except:
            None
    def loadscores(self,path,name):
        try:
            with open('scores_'+name, 'r')as file:
                return ast.literal_eval(file.read())
        except:
            return []
