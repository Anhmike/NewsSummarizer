#Summarizes a news article

#text processing
from nltk.tokenize.punkt import PunktWordTokenizer
from nltk.tokenize.punkt import PunktSentenceTokenizer

#TfIdf, LSI and similarity testing modules
from gensim import corpora, models, similarities

#Web Processing 
from bs4 import BeautifulSoup
import urllib.request as urllib

import operator

#Current Issues:
#1) Because I tokenize by splitting on ".", sometimes sentences get cut off e.g St. Lawrence = "...St" "Lawrence"
#2) BeautifulSoup's extract works pretty well to remove javascript and css but there is still some junk left in the html page.

def web_crawler(userinput):
    url = urllib.urlopen(userinput).read()
    #add exception here for internet connection not avalaible
    soup = BeautifulSoup(url.decode('utf8'))
    title = str(soup.title).strip("<title>")
    title = title.strip("</")
    htmlText =' '.join(map(lambda p : p.text, soup.findAll('p')))
    htmlText = ' '.join(htmlText.split())   #remove unnecessary whitspace
    #for now return the title query and the article text
    return (title, htmlText)


#edit for memory friendly version later
def summarizer(query, textList):
    dictionary = corpora.Dictionary(textList)   #conv

    corpus = [dictionary.doc2bow(i) for i in textList]

    tfidf = models.TfidfModel(corpus, normalize = True)
    myTfidf = tfidf[corpus]

    lsi = models.LsiModel(myTfidf,id2word = dictionary, num_topics =300)
    myLsi = lsi[myTfidf] 
    #convert textList(List of Lists of strings) to gensim's lsi model

    query_bow = dictionary.doc2bow(query)   
    #convert the query to gensim's bag of words model and next to the lsi model
    query_lsi = lsi[query_bow]

    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[query_lsi]

    return sorted(enumerate(sims), key = lambda item: -item[1]) 
# return a list of tuples, sorted from highest to lowest


def usingTitleAlgorithm(userinput):
    #nltk's english stopword list
    stop = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
     'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
     'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
     'itself', 'they', 'them', 'their', 'theirs', 'themselves',
     'what', 'which', 'who', 'whom', 'this', 'that', 'these',
     'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
     'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
     'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
     'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
     'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
    'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
     'why', 'how', 'all', 'any', 'both', 'each', 'few','more', 'most', 'other', 'some', 'such',
     'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'don', 'should', 'now']
    url = str(userinput)
    title, htmlText = web_crawler(url)
    qry = PunktWordTokenizer().tokenize(title)  #tokenize title
    qry = [words for words in qry if words.lower() not in stop] #Run Query through stopwords
    totalText = PunktSentenceTokenizer().tokenize(htmlText)
    textList = []
    for i in totalText:
        i = PunktWordTokenizer().tokenize(i.strip('.'))
        textList.append(i)

    sentenceRanks = summarizer(qry, textList)
    finalResults = []
    for num in range(1,4):  #skipping the first sentence because it's just going to be the title
        ind = sentenceRanks[num][0]
        finalResults.append(' '.join(textList[ind]))
    finalResults.append(title)
    return finalResults
    
    
def sentence_intersection(sen1, sen2):
    if(len(sen1) + len(sen2) == 0):
        return 0
    s1 = set(sen1)      #We convert the strings to sets so we can advantage of set's intersection function
    s2 = set(sen2)
    
    return ((len(s1.intersection(s2))/ ((len(s1) +len(s2))/2))) #We normalize the result 


#textList is a list of lists of strings
#
def sentence_ranks(textList):
    n = len(textList)
    v =[[0 for i in range(0,n)] for i in range(0,n)] #initialize matrix
    for i in range(0,n):
        for j in range(0,n):
            v[i][j] = sentence_intersection(textList[i],textList[j]) #Store the sentence intersections in the matrix
    dict = {}
    for i in range(0,n):
        score = 0
        for j in range(0,n):
            if i == j: #same sentence
                continue
            score += v[i][j]        #Add all a sentence's intersection
        dict[' '.join(textList[i])] = score #Store the sentence score in a dictionary, 
                                            #with the key being the sentence itself and the value being the score 
    return dict
    
def usingSentenceIntersectionAlgorithm(userinput):
    url = userinput
    title, htmlText = web_crawler(url)
    qry = PunktWordTokenizer().tokenize(title)  #tokenize title
    
    totalText = PunktSentenceTokenizer().tokenize(htmlText)
    textList = []
    for i in totalText:
        i = PunktWordTokenizer().tokenize(i.strip('.'))
        textList.append(i)
    ranks = sentence_ranks(textList)
    ranks_sorted = sorted(ranks.items(), key = operator.itemgetter(1))
    ranks_sorted.reverse()
    
    finalResults = []
    for num in range(1,4):  #skipping the first sentence because it's just going to be the title
        finalResults.append(ranks_sorted[num][0])
    finalResults.append(title)
    
    return finalResults
