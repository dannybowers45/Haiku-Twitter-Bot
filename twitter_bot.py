import time
from datamuse import datamuse
from keys import *
import tweepy
from spellchecker import SpellChecker

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
museApi = datamuse.Datamuse()
spell = SpellChecker()
continueOn = True

def check_haiku(inputString):
    punc = '''!()-[]{};:"\,<>./""?@#$%^&*_~'''
    for i in inputString:
        if i in punc:
            inputString = inputString.replace(i, '')


    chunks = inputString.split(' ')
    print (chunks)
    while '' in chunks:
        chunks.remove('')
    print (chunks)
    misspelled = spell.unknown(chunks)
    if len(chunks) > 17:
        print('Excess words')
        return 'fail'
    if len(misspelled) != 0:
        print('These words are misspelled')
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
        if totalSylCount == 17 and fiveCountOne == 5 and sevenCount == 7 and fiveCountTwo == 5:
            haiku = '   ' +fiveCountOneStr  + '\n   '   + sevenCountStr + '\n   ' + fiveCountTwoStr
            print('You made a Haiku!')
            print(haiku)
            return haiku
        else:
            return 'fail'


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

    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    #mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    my_timeline = api.home_timeline(last_seen_id, tweet_mode = 'extended')
    for mention in my_timeline:

        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        print('full text: ' + mention.full_text)
        tweetInput = mention.full_text;

        tweetInput = tweetInput.replace('\n', " ")
        hash = tweetInput.find('#')
        dash = tweetInput.find('-')
        if (hash != -1):
            tweetInput = tweetInput[0:hash-1]
        if (dash != -1):
            tweetInput = tweetInput[0:dash-1]

        haikuOutput = check_haiku(tweetInput)
        print(haikuOutput)
        if haikuOutput != 'None' and haikuOutput != 'fail':
            api.retweet(mention.id)
            api.update_status('@' + str(mention.user.screen_name) + ' You made a haiku! \n' + str(haikuOutput), mention.id)
            print('@' + str(mention.user.screen_name) + ' You made a haiku! \n' + str(haikuOutput), mention.id)



while continueOn:
    reply_to_tweets()
    time.sleep(15)
    continueOn = False
