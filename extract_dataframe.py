import json
import pandas as pd
from textblob import TextBlob

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list    
    
    def find_full_text(self)->list:
        text = []
        for tweets in self.tweets_list:
            text.append(tweets['text'])
        return text
    
    def find_clean_text(self, text)->list:
        clean_text = []
        for t in text:
            new_t = re.sub(r'^.*?:', '', t)
            clean_text.append(new_t)
        return clean_text
    
    def find_screen_name(self)->list:
        screen_name = []
        for tweets in self.tweets_list:
            screen_name.append(tweets['user']['screen_name'])
        return screen_name
    

    def find_created_time(self)->list:
        created_at = []
        for tweets in self.tweets_list:
            created_at.append(tweets['created_at'])
        return created_at

    def find_source(self)->list:
        source = []
        for tweets in self.tweets_list:
            source.append(tweets['source'])
        return source
        
    def find_followers_count(self)->list:
        followers_count = []
        for tweets in self.tweets_list:
            followers_count.append(tweets['user']['followers_count'])
        return followers_count

    def find_friends_count(self)->list:
        friends_count = []
        for tweets in self.tweets_list:
            friends_count.append(tweets['user']['friends_count'])
        return friends_count
    
    def find_sentiments(self, text)->list:
        polarity_l = []
        subjectivity_l = []
        for tweets in text:
            polarity= (TextBlob(tweets).sentiment[0])
            self.subjectivity= (TextBlob(tweets).sentiment[1])
            polarity_l.append(polarity)
            subjectivity_l.append(self.subjectivity)
        return polarity_l, subjectivity_l
    
    def find_lang(self) ->list:
        lang = []
        for tweets in self.tweets_list:
            lang.append(tweets['lang'])
        return lang

    def find_favourite_count(self)->list:
        favourite_count = []
        for tweets in self.tweets_list:
            favourite_count.append(tweets['user']['favourites_count'])
        return favourite_count
    
    def find_retweet_count(self)->list:
        retweet_count = []
        for tweets in self.tweets_list:
            try: 
                retweet = tweets['retweeted_status']['retweet_count']
            except:
                retweet = None
            retweet_count.append(retweet)
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = []
        for tweets in self.tweets_list:
            hashtags.append(tweets['entities']['hashtags'])
        return hashtags

    def find_mentions(self)->list:
        mentions = []
        for tweets in self.tweets_list:
            mentions.append(tweets['entities']['user_mentions'])
        return mentions
    
    def find_location(self)->list:
        locations = []
        for tweets in self.tweets_list:
            try:
                location = tweets['user']['location']
            except TypeError:
                location= ''
            locations.append(location)
        return locations
    
    
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at','source', 'original_text','clean_text', 'polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 'original_author',
             'followers_count','friends_count', 'hashtags', 'user_mentions','place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        clean_text = self.find_clean_text(text)
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        
        data = list(zip(created_at, source, text, clean_text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, hashtags, mentions, location))
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at','source', 'original_text', 'clean_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 'original_author',
             'followers_count','friends_count', 'hashtags', 'user_mentions','place']
    _, tweet_list = read_json("./data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above

    