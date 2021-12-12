#Gaurdian API: https://content.guardianapis.com/search?q=" + queryStr + "&api-key=56053666-9614-43e9-b99f-fbdabb55c3e4
#BBC News API: e31cc908fb3d4ec38bc0d58a46d1836b
#News API: https://newsapi.org/v2/everything?q='tesla'&from=2021-07-27&sortBy=publishedAt&apiKey=e31cc908fb3d4ec38bc0d58a46d1836b
import urllib.request, urllib.parse, urllib.error
import json

def newsAPI(query):
    base_url='https://newsapi.org/v2/everything?q='+ query +'&from=2021-07-27&sortBy=publishedAt&apiKey=e31cc908fb3d4ec38bc0d58a46d1836b'
    response=urllib.request.urlopen(base_url)
    data = response.read().decode()
    json_res=json.loads(data)
    print(json_res)

def gaurdianAPI(query):
    base_url='https://content.guardianapis.com/search?q='+ query +'&api-key=56053666-9614-43e9-b99f-fbdabb55c3e4'
    response=urllib.request.urlopen(base_url)
    data = response.read().decode()
    json_res=json.loads(data)
    print(json_res)

def containsSpace(query):
    str=''
    for ch in query:
        if ch == ' ':
            str+='-'
        else:
            str+=ch
    return str
print('Enter News Query: ')
query=input()
query=containsSpace(query)
print('Searching for ', query)
print('Gaurdian: ')
gaurdianData=gaurdianAPI(query)
print('News API: ')
newsData=newsAPI(query)

