import numpy as np # linear algebra import pandas as pd # data processing
import matplotlib.pyplot as plt # graphs and charts import pandas.testing as
from io import BytesIO
import sklearn
from sklearn.model_selection import train_test_split # data splitting
import statsmodels.api as sm
from sklearn import metrics
from sklearn.linear_model import LinearRegression # Linear model
from flask import Flask, render_template, request, json, send_file
import json
import pandas as pd
import os
import bq_helper
from flask import Flask, jsonify, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# initialize flask application
app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\Vrindavan\\Downloads\\Demand forecasting-13015a608bb5.json"
stackoverflow = bq_helper.BigQueryHelper("bigquery-public-data","stackoverflow")

queryx = """select EXTRACT(year FROM creation_date) AS year, COUNT(*) AS posts 
        from `bigquery-public-data.stackoverflow.posts_questions`
        where extract(year from creation_date) >= 2008 and extract(year from creation_date) < 2021
        group by year
        order by year
        """

PostsCount = stackoverflow.query_to_pandas(queryx)

def CurrentTrends_merge():
    query1 = "select EXTRACT(year FROM creation_date) AS year, COUNT(id) as posts from `bigquery-public-data.stackoverflow.posts_questions` where extract(year from creation_date) >=2009 and extract(year from creation_date) < 2021 and tags like '%"
    query3 ="%' group by year order by year"
    df = []
    labels = []

    dfall = ["html", "kubernetes"]
    
    if labels==None:
        labels = dfall    #the keywords list
        
    l = len(dfall)
    ###### for every tag, execute the query separately
    for i in range(l):
        query2 = dfall[i]    # dfall = ['hadoop','spark','hive']
        query = query1+query2+query3
        Posts = stackoverflow.query_to_pandas(query)
        Posts['posts']= Posts['posts']*100/PostsCount.posts
        pd.to_numeric(Posts['year'])
        Posts.rename(columns = {'posts':dfall[i]}, inplace = True) 
        df.append(Posts)
        
    trend = pd.DataFrame(df[0])
    trend = trend.set_index('year')
    
    if(l>1):
        for i in range(1,l):
            trend = pd.merge(trend, df[i], how='outer', on = 'year')
            trend = trend.set_index('year')
            trend = trend.fillna(0)
    
    return trend

@app.route("/")
def hello():
  return "Hello World!"


@app.route('/tags', methods = ['GET'])
def tags():
    query1 = """select tags from `bigquery-public-data.stackoverflow.posts_questions` LIMIT 100000"""
    df = stackoverflow.query_to_pandas(query1)
    llist = df['tags'].to_list()
    new_list = [i.split('|') for i in llist]
    flat_list = []
    for sublist in new_list:
        for item in sublist:
            flat_list.append(item)
    setflat_list = set(flat_list)
    final = json.dumps(list(setflat_list))
    return final 

@app.route('/api/current-trends', methods = ['POST', 'GET'])
def CurrentTrends():
    query1 = "select EXTRACT(year FROM creation_date) AS year, COUNT(id) as posts from `bigquery-public-data.stackoverflow.posts_questions` where extract(year from creation_date) >=2009 and extract(year from creation_date) < 2021 and tags like '%"
    query3 ="%' group by year order by year"
    df = []
    dfall = ["hadoop","python"]
    

    labels = dfall
   
    l = len(dfall)
    ###### for every tag, execute the query separately
    for i in range(l):
        query2 = dfall[i]    # dfall = ['hadoop','spark','hive']
        query = query1+query2+query3
        Posts = stackoverflow.query_to_pandas(query)
        Posts['posts']= Posts['posts']*100/PostsCount.posts
        pd.to_numeric(Posts['year'])
        Posts.rename(columns = {'posts':dfall[i]}, inplace = True)
        df.append(Posts)
        

    trend = pd.merge(df[0], df[1], how='inner', on = 'year')
    trend = trend.set_index('year')
    
    
    if(l>2):
        for i in range(2,l):
            trend = pd.merge(trend, df[i], how='outer', on = 'year')
            trend = trend.set_index('year')
            trend = trend.fillna(0)


    #return 	jsonify(trend)

    curr_trendsjson = trend.to_json(orient="index")

    return curr_trendsjson



@app.route('/api/future-trends', methods = ['POST', 'GET'])
def FutureTrends():

    #plt.figure(figsize=(20,10))
    
    query1 = "select EXTRACT(year FROM creation_date) AS year, COUNT(id) as posts from `bigquery-public-data.stackoverflow.posts_questions` where extract(year from creation_date) >=2009 and extract(year from creation_date) < 2021 and tags like '%"
    query3 ="%' group by year order by year"
    df = []
    new = []
    
    years = [2021, 2022, 2023] 
    dfall = ["html", "kubernetes"]  
    labels= []

    l = len(dfall) 
    
    if (labels==None):
        labels = dfall
        
    for i in range(l):
        query2 = dfall[i]
        query = query1+query2+query3
        Posts = stackoverflow.query_to_pandas(query)
        Posts['posts']= Posts['posts']*100/PostsCount.posts
        pd.to_numeric(Posts['year'])
        
        X_train=Posts['year'].values.reshape(-1,1)
        y_train=Posts['posts'].values.reshape(-1,1)
        reg=LinearRegression()
        
        X_test = [[2021], [2022], [2023]]     #hardcoded 3 years
        reg.fit(X_train,y_train)
        predictions = reg.predict(X_test)
        #new.append(predictions)
        
        dummy = pd.DataFrame(columns = ['year', dfall[i]])
        dummy['year']= years
        dummy[dfall[i]] = predictions
        
        new.append(dummy)
        #predictions.reshape((1,len(X_test))
    
    trendfuture = pd.DataFrame(new[0])            #first keyword data + predictions
    trendfuture = trendfuture.set_index('year')
    
    if(l>1):                  # if more than 1 keyword
        for i in range(1,l):
            #print()
            trendfuture = pd.merge(trendfuture, new[i], how='outer', on = 'year')
            trendfuture = trendfuture.set_index('year')
    #print(trendfuture)
    
    curr_trendmerge = CurrentTrends_merge()
    
    #print(curr_trendmerge)
    final = pd.concat([curr_trendmerge, trendfuture])
    future_trendsjson = final.to_json(orient="index")
    return future_trendsjson

"""
    
    final.plot(kind='line')
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Posts %', fontsize=15)
    y_pos=[2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]
    plt.xticks(y_pos,fontsize=9)
    plt.yticks(fontsize=9)
    plt.title(title)return future_trendsjson

    plt.legend(labels, loc=[1.0,0.5])
    plt.show()

## Converting to JSON :

    future_trendsjson = final.to_json(orient="index")
    
    #parsed = json.loads(curr_result1)
    #json.dumps(parsed, indent=4)
    
    return future_trendsjson
"""    

"""
    fig, ax = plt.subplots()
    #fig = trend.plot(kind='line')
    y_pos=[2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
    plt.plot(trend)
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Posts %', fontsize=15)
    
    plt.xticks(y_pos,fontsize=8)
    plt.yticks(fontsize=8)
    #plt.title(title)
    plt.legend(labels, loc=[1.0,0.5])
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)


    return send_file(img, mimetype = 'image/png')
    
    
    #parsed = json.loads(curr_result1)
    #json.dumps(parsed, indent=4)
    #print(trend)
    
    #return trend

"""

if __name__ == "__main__":
	app.run(debug=True)