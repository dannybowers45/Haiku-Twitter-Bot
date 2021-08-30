import time
from datamuse import datamuse
from keys import *
import tweepy
from spellchecker import SpellChecker
#import pandas as pd

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
museApi = datamuse.Datamuse()
spell = SpellChecker()
continueOn = True



def check_haiku(inputString):
    punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
    #inputString = 'Hello I will be writing. a/ haiku for you. I hope you like it'
    for i in inputString:
        if i in punc:
            inputString = inputString.replace(i, "")


    chunks = inputString.split(' ')
    print (chunks)
    while '' in chunks:
        chunks.remove('')
    print (chunks)
    misspelled = spell.unknown(chunks)

    if len(misspelled) != 0:
        print('You misspelled these words idiot')
        print(misspelled)
        return 'fail'
    else:
        fiveCountOne, sevenCount, fiveCountTwo, totalSylCount = 0, 0, 0, 0
        fiveCountOneStr, sevenCountStr, fiveCountTwoStr = '', '', ''
        for j in chunks:
            rhymesJSON = (museApi.words(sl=j, max=5))[0]
            sylCount = rhymesJSON["numSyllables"]
            totalSylCount += sylCount
            if totalSylCount > 17:
                break
                #print(j + ' has ' + str(sylCount) + ' syllable(s)')
            elif fiveCountOne < 5:
                fiveCountOne += sylCount
                fiveCountOneStr += (j + ' ')
            elif fiveCountOne == 5 and sevenCount < 7:
                sevenCount += sylCount
                sevenCountStr += (j + ' ')
            elif sevenCount == 7 and fiveCountTwo < 5:
                fiveCountTwo += sylCount
                fiveCountTwoStr += (j + ' ')
        print (totalSylCount)
    # print(fiveCountOne)
    # print(sevenCount)
    # print(fiveCountTwo)
        if totalSylCount == 17 and fiveCountOne == 5 and sevenCount == 7 and fiveCountTwo == 5:
            haiku = '   ' +fiveCountOneStr  + '\n   '   + sevenCountStr + '\n   ' + fiveCountTwoStr
            print('You made a Haiku!')
            print(haiku)
            return haiku
        else:
            return 'fail'

#check_haiku('The parent tunnel after a childhood sports game was peak happiness')
# This is a Test for
# my twitter bot to check for
# purposeless haikus

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():

    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use  for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    #mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    my_timeline = api.home_timeline(last_seen_id, tweet_mode = 'extended')
    #for status in my_timeline:
    #print(status.text)
    for mention in my_timeline:

        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        print(last_seen_id)
        store_last_seen_id(last_seen_id, FILE_NAME)
        print('full text: ' + mention.full_text)
        #print('text: ' + mention.text)
        tweetInput = mention.full_text;

        tweetInput = tweetInput.replace('\n', " ")
        hash = tweetInput.find('#')
        dash = tweetInput.find('-')
        if (hash != -1):
            tweetInput = tweetInput[0:hash-1]
        if (dash != -1):
            tweetInput = tweetInput[0:dash-1]
        #at = tweetInput.find('@')
        #if (at != -1):
            #tweetInput = tweetInput[at, ]
        #tweetInput = tweetInput.replace('@DannyBOTers ', '')
        haikuOutput = check_haiku(tweetInput)
        print(haikuOutput)
        if haikuOutput != 'None' and haikuOutput != 'fail':
            api.retweet(mention.id)
            api.update_status('@' + str(mention.user.screen_name) + ' You made a haiku! \n' + str(haikuOutput), mention.id)
            #print('@' + str(mention.user.screen_name) + ' You made a haiku! \n' + str(haikuOutput), mention.id)

        #if '#helloworld' in mention.full_text.lower():
        #print('I was mentioned in a tweet!', flush=True)
        #print(mention.user.screen_name.lower())
        #mention.user.screen_name.lower() == 'dannybowers45':


while continueOn == True:
    reply_to_tweets()
    time.sleep(15)
    continueOn = False
