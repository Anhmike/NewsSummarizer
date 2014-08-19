#Summarizes a news article


#Current Issues:
#1) Because I tokenize by splitting on ".", sometimes sentences get cut off e.g St. Lawrence = "...St" "Lawrence"
#2) BeautifulSoup's extract works pretty well to remove javascript and css but there is still some junk left in the html page.


from gensim import corpora, models, similarities
from bs4 import BeautifulSoup
import urllib.request as urllib

def web_crawler():
    userinput = str(input("Enter a valid Web Page URL: "))
    url = urllib.urlopen(userinput)
    #add exception here for internet connection not avalaible
    soup = BeautifulSoup(url.read())
    [s.extract() for s in soup('script')]   #remove javascriptlinks
    [s.extract() for s in soup('style')]    #remove css
    [s.extract() for s in soup('a')]    # remove links
    query = str(soup.title).strip("<title>")
    query = query.strip("</")
    htmlText = soup.get_text()
    htmlText = ' '.join(htmlText.split())   #remove unnecessary whitspace
    textFile = open("textFile.txt", mode = "w", encoding = "utf8")
    textFile.write(htmlText)    #save text file to use in memory friendly version
    textFile.close()
    #for now return the title query and the article text
    return (query, htmlText)




#edit for memory friendly version later
def summarizer(query, textList):
    dictionary = corpora.Dictionary(textList)   #conv

    corpus = [dictionary.doc2bow(i) for i in textList]

    tfidf = models.TfidfModel(corpus, normalize = True)
    myTfidf = tfidf[corpus]

    lsi = models.LsiModel(myTfidf,id2word = dictionary, num_topics =300)
    myLsi = lsi[myTfidf] #convert textList(List of Lists of strings) to gensim's lsi model

    query_bow = dictionary.doc2bow(query.lower().split())   #convert the query to gensim's bag of words model and next to the lsi model
    query_lsi = lsi[query_bow]

    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[query_lsi]

    return sorted(enumerate(sims), key = lambda item: -item[1]) # return a list of tuples, sorted from highest to lowest


def main():
    qry, htmlText = web_crawler()

    total_text = htmlText.lower().split('.')
    textList = []
    for i in total_text:
        i = i.split()
        textList.append(i)

    sentenceRanks = summarizer(qry, textList)
    #print(sentenceRanks)
    print("This is a 5 sentence summary of: \n")
    print(qry + "\n")
    for num in range(1,6):  #skipping the first sentence because it's just going to be the title
        ind = sentenceRanks[num][0]
        print(' '.join(textList[ind]) +'\n')




if __name__ == '__main__':
    main()
