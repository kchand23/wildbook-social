import tweepy as tw
from tweepy import OAuthHandler
import pymongo
import twitterCred


auth = OAuthHandler(twitterCred.CONSUMER_KEY, twitterCred.CONSUMER_SECRET)
auth.set_access_token(twitterCred.ACCESS_TOKEN, twitterCred.ACCESS_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

#search terms and date wanted from
search_words = "whale shark"
date_since = "2018-11-16"

#gets tweet data
tweets = tw.Cursor(api.search, q=search_words, lang="en", since=date_since).items(10000)

#checks to see if there is media key in entities
def checkMedia(tweets):
    if "media" in tweets.entities:
        return tweets.entities["media"][0]["media_url"]
    else:
        return False

#checks to see if there is an extended entities attribute
#if so, loop through all of the media and return it
def checkExtendedEntities(tweets):
    if(hasattr(tweets, 'extended_entities')):
        for img in range(0, len(tweet.extended_entities["media"])):
            return(tweet.extended_entities["media"][img]["media_url"])
        return True
    else:
        return False


#loops through to get certain information
for tweet in tweets:
    
    tweetList = []
    tweetDic = {}
    
    #if there is a media key in entities then get the user name, location,
    #id, date created. url and hashtags from the post
    if (checkMedia(tweet) != False) and (tweet.retweeted == False) :
        
        createdAt = str(tweet.created_at)
        url = checkMedia(tweet)
        checkExtendedEntities(tweet)
        user_name = tweet.user.name
        location = tweet.user.location
        user_id = tweet.user.id_str
        hashtags = tweet.entities["hashtags"]
        
        tweetDic["created_at"] = createdAt
        tweetDic["location"] = location
        tweetDic["user_id"] = user_id
        tweetDic["img_url"] = str(url)
        tweetDic["user_name"] = user_name
        tweetDic["hashtags"] = hashtags
        
        #put this into an array of dictionaries
        tweetList.append(tweetDic)
        
        # add collection into mongodb
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["species"]
        mycol = mydb["whale shark"]
        x = mycol.insert_many(tweetList)


