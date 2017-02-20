import unittest
import tweepy
import requests
import json
import twitter_info

## SI 206 - W17 - HW5
## COMMENT WITH:
## Your section day/time: Thursday 6-7pm
## Any names of people you worked with on this assignment:

######## 500 points total ########

## Write code that uses the tweepy library to search for tweets with a phrase of the user's choice (should use the Python input function), and prints out the Tweet text and the created_at value (note that this will be in GMT time) of the first THREE tweets with at least 1 blank line in between each of them, e.g.

## TEXT: I'm definitely not an awesome Python programmer, but I let other people think that.
## CREATED AT: Sat Feb 11 04:28:19 +0000 2017

## TEXT: Go blue!
## CREATED AT: Sun Feb 12 12::35:19 +0000 2017

## .. plus one more.

## You should cache all of the data from this exercise in a file, and submit the cache file along with your assignment. 

## So, for example, if you submit your assignment files, and you have already searched for tweets about "rock climbing", when we run your code, the code should use CACHED data, and should not need to make any new request to the Twitter API. 
## But if, for instance, you have never searched for "bicycles" before you submitted your final files, then if we enter "bicycles" when we run your code, it _should_ make a request to the Twitter API.

## The lecture notes and exercises from this week will be very helpful for this. 
## Because it is dependent on user input, there are no unit tests for this -- we will run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

## **** For 50 points of extra credit, create another file called twitter_info.py that contains your consumer_key, consumer_secret, access_token, and access_token_secret, import that file here, and use the process we discuss in class to make that information secure! Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information for an 'extra' Twitter account you make just for this class, and not your personal account, because it's not ideal to share your authentication information for a real account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these with variables rather than filling in the empty strings if you choose to do the secure way for 50 EC points
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser()) # Set up library to grab stuff from twitter with your authentication, and return it in a JSON-formatted way

## Write the rest of your code here!

#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except statement shown in class.
## 2. Write a function to get twitter data that works with the caching pattern, so it either gets new data or caches data, depending upon what the input to search for is. You can model this off the class exercise from Tuesday.
## 3. Invoke your function, save the return value in a variable, and explore the data you got back!
## 4. With what you learn from the data -- e.g. how exactly to find the text of each tweet in the big nested structure -- write code to print out content from 3 tweets, as shown above.



CACHE_FNAME = "TWITTER_DATA.json"

try:
    cache_file = open(CACHE_FNAME,'r') #reading the data from the cache file
    cache_contents = cache_file.read() # get the data into a string
    CACHE_DICTION = json.loads(cache_contents) #load that stuff info a dictionary
    cache_file.close() # close that file when were done with it

except:

    CACHE_DICTION = {} # if there is nothing there, make sure that CACHE_DICTION is empty!


def get_twitter_data(search_request):
    if search_request in CACHE_DICTION: #seeing if the search request is in the CACHE_DICTION
        print ("\n" + "USING CACHED DATA FOR: " + search_request + "\n") #print a nice message
        twitter_search_results = CACHE_DICTION[search_request] 

    else:
        
        try:
            print ("\n" +"GETTING NEW DATA FOR: " + search_request + "\n")
            twitter_search_results = api.search(q=search_request)
            CACHE_DICTION[search_request] = twitter_search_results 
            cached_file = open(CACHE_FNAME,'w') 
            cached_file.write(json.dumps(CACHE_DICTION, indent=2))
            cached_file.close() #close the file

        except: 
            print ("There seems to have been a problem, try checking your network connection then try again")
            exit()

    return twitter_search_results #json object is returned from this function



def run_program(): #function for running program
    search_word = input("Enter your search query here: " + "\n") 
    compiled_tweets = get_twitter_data(search_word) #make the twitter search using API or cached file
    for a_tweet in compiled_tweets['statuses'][:3]: #getting 3 tweets
        print ("TEXT: " + a_tweet['text']) #twitter text
        print ("CREATED AT: " + a_tweet['created_at']) 
        print("\n")


run_program() 



###########>>>>>>>> PLEASE READ <<<<<<<<<<<<<<#############
# In my cached file, I searched up "Rocket League" and "University of Michigan" and "Vanoss Gaming"
# When searching for "UMSI", the spacing in the terminal for some reason, but for everything else it's fine!!!