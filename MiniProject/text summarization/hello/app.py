from flask import Flask, jsonify, request
import urllib.request, urllib.parse, urllib.error
import json

app=Flask(__name__)

@app.route("/api",methods=['GET'])

def index():
    # jsondata={}
    # jsondata['result']= str(request.args['query'])
    # print(jsondata)
    # return jsondata
    qry_str=request.args['query']
    print('Got This',qry_str)
    temp_ls=[]
    temp_ls=qry_str.split(' ')
    qry_str='%20'.join(temp_ls)
    print('Legal Query: ', qry_str)
    #return qry_str
    loadedNews=gaurdianAPI(qry_str)
    print(loadedNews)
    return loadedNews

def gaurdianAPI(query):
    base_url='https://content.guardianapis.com/search?q='+ query +'&api-key=56053666-9614-43e9-b99f-fbdabb55c3e4'
    response=urllib.request.urlopen(base_url)
    data = response.read().decode()
    json_res=json.loads(data)
    print(str(json_res['response']['results'][0]))
    return str(json_res['response']['results'][0])


if __name__ == '__main___':
    app.run()