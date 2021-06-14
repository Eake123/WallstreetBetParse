
from questrade_api import Questrade
import praw
import json
import yfinance as yf
from time import time as timer
from jsonclass import *
import concurrent.futures
# Enter your info here
reddittoken = ''
clientID = ''
password = ''
userName = ''

def dataParse(top_subreddit):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = [executor.submit(searchRedditDes, title) for title in top_subreddit]
        totalList = [f.result() for f in future]
    titleList = []
    commentList = []
    for i in totalList:
        try:
            titleList.append(i[0])
            commentList.append(i[1])
        except:
            pass
    titleTicker = findTickerTitle(titleList)
    commentTicker = findTickerCom(commentList)
    J = Json('title.txt',str(Reddit()))
    J.changeDump(titleList)
    totalTicker = titleTicker + commentTicker
    return totalTicker

def findTickerCom(words_collection):
    title_collection = cleanWords(words_collection,'title.txt',"title",False)
    ticker = []
    for i in title_collection:
        noDuplicate = list(dict.fromkeys(i))
        for j in noDuplicate:
            if(j.isupper() or "$" in j):
                ticker.append(j)
    return ticker

def findTickerTitle(words_collection):
    title_collection = cleanWords(words_collection,'title.txt',"title",False)
    ticker = []
    for i in title_collection:
        noDuplicate = list(dict.fromkeys(i[0]))
        for j in noDuplicate:
            if(j.isupper() or "$" in j):
                ticker.append(j)
    return ticker
def searchRedditDes(submission):
    try:
        start = timer()
        words_collection = []
        title = submission.title
        title_words = title.split()
        comment_collection = []
        words_collection.append(title_words)
        for comment in submission.comments:
            comment_collection.append(comment.body)
        return words_collection, comment_collection
    except:
        pass



def parseReddit(newCount):
    top_subreddit = redditConnect(newCount)
    ticker,duplicate = titleParse(top_subreddit)
    tickerDic = tickertoDic(ticker,duplicate)
    J = Json('ticker.txt',str(Reddit()))
    J.dicDump(tickerDic)





def cleanWords(dirtyList,file,key,up):
    J = Json(file,str(Reddit()))
    data = J.readKey()
    #print(data1)
    # with open(file) as json_file:
    #     data = json.load(json_file)
        #print(data,key)
    words = []
    for p in data:
        if(up == True):
            word = p.upper()
        else:
            word = p
        words.append(word)
    cleanWords = [x for x in dirtyList if x not in words]
    return cleanWords


def redditConnect(newCount):
    reddit = praw.Reddit(client_id=clientID, client_secret=reddittoken,password=password,user_agent='SHANE',username=userName)
    subreddit = reddit.subreddit('wallstreetbets')
    top_subreddit = subreddit.new(limit=newCount)
    return top_subreddit

def titleParse(top_subreddit):
    ticker = dataParse(top_subreddit)
    goodTicker,duplicate = searchYahoo(ticker)
    return goodTicker,duplicate


def searchYahoo(ticker):
    getVals = list([val for val in ticker
                if(val.isalpha() or val.isnumeric())])
    goodTicker = []
    noDuplicate = list(dict.fromkeys(getVals))
    useList = cleanWords(noDuplicate,'commonWord.txt','commonWord',True)
    unCheckedList,checkedList = tickerCheck(useList)
    for o in unCheckedList:
        symbol = yf.Ticker(o)
        symbol = symbol.info
        try:
            if(symbol.get('zip') != None):
                print("goodTicker",o)
                goodTicker.append(o)
        except:
            print("badTicker",o)
            pass
    masterList = checkedList + goodTicker
    badTicker = [x for x in useList if x not in masterList]
    fileDic = {"commonWord.txt":badTicker,'goodTicker.txt':goodTicker}
    for i in fileDic:
        J = Json(i,str(Reddit()))
        J.addDump(fileDic[i])
    return masterList,getVals

def tickerCheck(useList):
    J = Json('goodTicker.txt',str(Reddit()))
    dic = J.readKey()
    unCheckedList = [x for x in useList if x not in dic]
    checkedList = [x for x in useList if x in dic]
    print(unCheckedList,"un",checkedList,"check")

    return unCheckedList,checkedList


def goodStock(goodTicker):
    with open('goodTicker.txt', 'r') as f:
        json_decoded = json.loads(f.read())
    dic = json_decoded['goodTicker']
    for i in goodTicker:
        dic.append(i)
    realDic = {'goodTicker':dic}
    with open('goodTicker.txt', 'w') as f:
        f.write(json.dumps(realDic, sort_keys=True, indent=4, separators=(',', ': ')))
    


def searchRedditTitle(top_subreddit):
    words_collection = []
    for submission in top_subreddit:
        title = submission.title
        title_words = title.split()
        words_collection.append(title_words)
    title_collection = cleanWords(words_collection,'title.txt',"title",False)
    ticker = []
    for i in title_collection:
        noDuplicate = list(dict.fromkeys(i))
        for j in noDuplicate:
            if(j.isupper() or "$" in j):
                ticker.append(j)
    J = Json('title.txt',str(Reddit()))
    J.changeDump(words_collection)
    return ticker


def tickertoDic(ticker,duplicate):
    newList = [x for x in duplicate if x in ticker]
    tickerDic = {}
    for i in newList:
        if(tickerDic.get(i) == None):
            tickerDic[i] = 1
        else:
            tickerDic[i] += 1
    return tickerDic



parseReddit(1000)
#debug(25)