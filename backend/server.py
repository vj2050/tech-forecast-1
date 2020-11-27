import json
import os
import sys

import bq_helper
import pandas as pd
from flask import Flask
from flask import json
from flask_cors import CORS
from sklearn.linear_model import LinearRegression  # Linear model

# initialize flask application
from data_provider import DataProvider

app = Flask(__name__)
CORS(app)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sys.argv[1]
stackoverflow = bq_helper.BigQueryHelper("bigquery-public-data", "stackoverflow")

data_provider = DataProvider(sys.argv[1])

queryx = """select EXTRACT(year FROM creation_date) AS year, COUNT(*) AS posts 
        from `bigquery-public-data.stackoverflow.posts_questions`
        where extract(year from creation_date) >= 2008 and extract(year from creation_date) < 2021
        group by year
        order by year
        """

PostsCount = stackoverflow.query_to_pandas(queryx)



@app.route("/")
def hello():
    return "Hello World!"


@app.route('/tags', methods=['GET'])
def tags():
    tagList = data_provider.get_top_tags(limit=25)
    return json.dumps(tagList)



@app.route('/current-trends', methods=['POST', 'GET'])
def CurrentTrends():
    query1 = "select EXTRACT(year FROM creation_date) AS year, COUNT(id) as posts from `bigquery-public-data.stackoverflow.posts_questions` where extract(year from creation_date) >=2009 and extract(year from creation_date) < 2021 and tags like '%"
    query3 = "%' group by year order by year"
    df = []
    dfall = ["python", "hadoop"]

    labels = dfall

    l = len(dfall)
    ###### for every tag, execute the query separately
    for i in range(l):
        query2 = dfall[i]  # dfall = ['hadoop','spark','hive']
        query = query1 + query2 + query3
        Posts = stackoverflow.query_to_pandas(query)
        #Posts['posts'] = Posts['posts'] * 100 / PostsCount.posts
        pd.to_numeric(Posts['year'])
        Posts.rename(columns={'posts': dfall[i]}, inplace=True)
        df.append(Posts)

    trend = pd.merge(df[0], df[1], how='inner', on='year')
    trend = trend.set_index('year')

    if (l > 2):
        for i in range(2, l):
            trend = pd.merge(trend, df[i], how='outer', on='year')
            trend = trend.set_index('year')
            trend = trend.fillna(0)

    curr_trendsjson = trend.to_json(orient="index")

    ###################################################################################################################################################################
    #Reputation_Answered(), Reputation_unanswered(), Topviewed_questions(), Answered_questions() Function calls below :

 # ************ Need to pass keyword, waiting for harshil's updated current trends , future trends functions : 
    reputation_json1 = data_provider.user_reputation_answered('python')
    reputation_json2 = data_provider.user_reputation_unanswered('python')
    topviewed_questions = data_provider.top_viewed_questions('python', 10)
    answered_questions = data_provider.answered_questions('python')

    curr_trendsjson = json.loads(curr_trendsjson)         #converting JSON string to dictionary
    reputation_json1 = json.loads(reputation_json1)       #converting JSON string to dictionary
    reputation_json2 = json.loads(reputation_json2)       #converting JSON string to dictionary
    topviewed_questions = json.loads(topviewed_questions)
    answered_questions = json.loads(answered_questions)

    payload = {                                              # merged Dictionary
    'current_trends': curr_trendsjson,
    'reputation_answered': reputation_json1,
    'reputation_unanswered': reputation_json2,
    'Top_viewed_questions': topviewed_questions,
    'Answered_Questions': answered_questions
    }

    final_payload = json.dumps(payload)                  #converting dictionary back to JSON object

    return (final_payload)


@app.route('/future-trends', methods=['POST', 'GET'])
def FutureTrends():
    # plt.figure(figsize=(20,10))

    query1 = "select EXTRACT(year FROM creation_date) AS year, COUNT(id) as posts from `bigquery-public-data.stackoverflow.posts_questions` where extract(year from creation_date) >=2009 and extract(year from creation_date) < 2021 and tags like '%"
    query3 = "%' group by year order by year"
    df = []
    new = []

    years = [2021, 2022, 2023]
    dfall = ["html", "kubernetes"]
    labels = []

    l = len(dfall)

    if (labels == None):
        labels = dfall

    for i in range(l):
        query2 = dfall[i]
        query = query1 + query2 + query3
        Posts = stackoverflow.query_to_pandas(query)
        Posts['posts'] = Posts['posts'] * 100 / PostsCount.posts
        pd.to_numeric(Posts['year'])

        X_train = Posts['year'].values.reshape(-1, 1)
        y_train = Posts['posts'].values.reshape(-1, 1)
        reg = LinearRegression()

        X_test = [[2021], [2022], [2023]]  # hardcoded 3 years
        reg.fit(X_train, y_train)
        predictions = reg.predict(X_test)
        # new.append(predictions)

        dummy = pd.DataFrame(columns=['year', dfall[i]])
        dummy['year'] = years
        dummy[dfall[i]] = predictions

        new.append(dummy)
        # predictions.reshape((1,len(X_test))

    trendfuture = pd.DataFrame(new[0])  # first keyword data + predictions
    trendfuture = trendfuture.set_index('year')

    if (l > 1):  # if more than 1 keyword
        for i in range(1, l):
            # print()
            trendfuture = pd.merge(trendfuture, new[i], how='outer', on='year')
            trendfuture = trendfuture.set_index('year')
    # print(trendfuture)

    curr_trendmerge = CurrentTrends_merge()

    # print(curr_trendmerge)
    final = pd.concat([curr_trendmerge, trendfuture])
    future_trendsjson = final.to_json(orient="index")
    return future_trendsjson

@app.route('/comparison', methods=['GET', 'POST'])
def CurrentTrends_compare():
    query1 = "select EXTRACT(year FROM creation_date) AS year, COUNT(id) as posts from `bigquery-public-data.stackoverflow.posts_questions` where extract(year from creation_date) >=2009 and extract(year from creation_date) < 2021 and tags like '%"
    query3 = "%' group by year order by year"
    df = []
    dfall = ["java", "hive"]

    labels = dfall

    l = len(dfall)
    ###### for every tag, execute the query separately
    for i in range(l):
        query2 = dfall[i]  # dfall = ['hadoop','spark','hive']
        query = query1 + query2 + query3
        Posts = stackoverflow.query_to_pandas(query)
        #Posts['posts'] = Posts['posts'] * 100 / PostsCount.posts
        pd.to_numeric(Posts['year'])
        Posts.rename(columns={'posts': dfall[i]}, inplace=True)
        df.append(Posts)

    trend = pd.merge(df[0], df[1], how='inner', on='year')
    trend = trend.set_index('year')

    if (l > 2):
        for i in range(2, l):
            trend = pd.merge(trend, df[i], how='outer', on='year')
            trend = trend.set_index('year')
            trend = trend.fillna(0)

    curr_trendsjson = trend.to_json(orient="index")

    return curr_trendsjson


## Should be displayed as TABLE **** Use below function for email notifications part : Top trending tags from 1st Jan 2020 to 6th September 2020 
### (last date of updation..  next quarterly update in December)

@app.route('/top-tags', methods=['GET'])
def top_tags():
    
    query_testing = """SELECT tag, COUNT(*) c
    FROM (
      SELECT SPLIT(tags, '|') tags
      FROM `bigquery-public-data.stackoverflow.posts_questions` a
      WHERE EXTRACT(DATE FROM creation_date)>= '2020-01-01' AND EXTRACT(DATE FROM creation_date)<= '2020-09-06'
    ), UNNEST(tags) tag
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10
    """

    query_toptags = stackoverflow.query_to_pandas(query_testing)
    toptags_json = query_toptags.to_json(orient = 'index')
    return toptags_json



# Display as TABLE (For Notifications Email Functionality) Top 10 most viewed Questions in general in current year 2020 
@app.route('/gen-top-ques', methods=['GET'])
def Topviewed_general():
    query_topGen = """SELECT id, title, answer_count answers, favorite_count favs,
                        view_count views, score votes
                        FROM `bigquery-public-data.stackoverflow.posts_questions` 
                        WHERE EXTRACT(YEAR FROM creation_date)= 2020 
                        order by views DESC 
                        LIMIT 10
                        """
    
    topGen = stackoverflow.query_to_pandas(query_topGen)
    topGen = topGen.fillna(0.0)
    topGen_JSON = topGen.to_json(orient = 'index')
    print(topGen)
    return topGen_JSON






   


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
