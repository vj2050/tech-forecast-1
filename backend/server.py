import sys

import numpy as np  # linear algebra import pandas as pd # data processing
import matplotlib.pyplot as plt  # graphs and charts import pandas.testing as
from io import BytesIO
import sklearn
from flask_cors import CORS
from sklearn.model_selection import train_test_split  # data splitting
import statsmodels.api as sm
from sklearn import metrics
from sklearn.linear_model import LinearRegression  # Linear model
from flask import Flask, render_template, request, json, send_file
import json
import pandas as pd
import os
import bq_helper
from flask import Flask, jsonify, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# initialize flask application
app = Flask(__name__)
CORS(app)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sys.argv[1]
stackoverflow = bq_helper.BigQueryHelper("bigquery-public-data", "stackoverflow")

queryx = """select EXTRACT(year FROM creation_date) AS year, COUNT(*) AS posts 
        from `bigquery-public-data.stackoverflow.posts_questions`
        where extract(year from creation_date) >= 2008 and extract(year from creation_date) < 2021
        group by year
        order by year
        """

PostsCount = stackoverflow.query_to_pandas(queryx)


def CurrentTrends_merge():
    query1 = "select EXTRACT(year FROM creation_date) AS year, COUNT(id) as posts from `bigquery-public-data.stackoverflow.posts_questions` where extract(year from creation_date) >=2009 and extract(year from creation_date) < 2021 and tags like '%"
    query3 = "%' group by year order by year"
    df = []
    labels = []

    dfall = ["html", "kubernetes"]

    if labels == None:
        labels = dfall  # the keywords list

    l = len(dfall)
    ###### for every tag, execute the query separately
    for i in range(l):
        query2 = dfall[i]  # dfall = ['hadoop','spark','hive']
        query = query1 + query2 + query3
        Posts = stackoverflow.query_to_pandas(query)
        Posts['posts'] = Posts['posts'] * 100 / PostsCount.posts
        pd.to_numeric(Posts['year'])
        Posts.rename(columns={'posts': dfall[i]}, inplace=True)
        df.append(Posts)

    trend = pd.DataFrame(df[0])
    trend = trend.set_index('year')

    if (l > 1):
        for i in range(1, l):
            trend = pd.merge(trend, df[i], how='outer', on='year')
            trend = trend.set_index('year')
            trend = trend.fillna(0)

    return trend


### This function is required for reputation functions :
def del_order_mark(df):
    new_Reputation = []
    for i in range(len(df)): # delete the order mark in "repulation"
        new_Reputation.append(df['Reputation'][i][1:])
    df.Reputation = new_Reputation
    return df


def Reputation_answered(keyword):
    # Reputation of the user making comments to answered questions for given tag.
    query_testing1 = """
    select 
        case
            when uc.reputation between 1 and 100 then '11- 100'
            when uc.reputation between 101 and 1000 then '2101- 1000'
            when uc.reputation between 1001 and 10000 then '31001- 10000'
            when uc.reputation between 10001 and 100000 then '410001- 100000'
            when uc.reputation > 100000 THEN '5> 100000'
        end as Reputation,
        sum(uc.num) as num
    from(    
    select u.reputation, count(*) as num
    from `bigquery-public-data.stackoverflow.users` u
    inner join(
        select c.user_id
        from `bigquery-public-data.stackoverflow.comments` c
        inner join (
            select id from `bigquery-public-data.stackoverflow.posts_questions`
            where answer_count > 0 and tags like '%"""

    query_testing2 = keyword

    query_testing3 = """%') q
        on post_id = q.id)
    on id = user_id
    group by reputation
    order by reputation asc) uc
    group by Reputation
    order by Reputation
    """
    final_query = query_testing1+query_testing2+query_testing3
    df_reputation1 = stackoverflow.query_to_pandas(final_query)
    df_reputation1 = del_order_mark(df_reputation1)
    
    reputation_json1 = df_reputation1.to_json(orient = 'index')
    #print(df_reputation1)
    
#     labels = df_reputation1.Reputation
#     sizes = round(100 * df_reputation1.num / df_reputation1.num.sum(),2)
#     colors = ['#EC7063','#3498DB','#F7DC6F','#BB8FCE','#2ECC71']
#     explode = (0.05,0.05,0.05,0.05,0.05)

#     fig1, ax1 = plt.subplots()
#     ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode)
#     ax1.axis('equal')  
#     plt.tight_layout()
#     plt.title("Reputation of the user making comments to answered questions associated with given Tag", fontsize = 14)
    
    return reputation_json1    


def Reputation_unanswered(keyword):
    # Reputation of the user making comments to answered questions for given tag.
    query_unanswered1 = """
    select 
        case
            when uc.reputation between 1 and 100 then '11- 100'
            when uc.reputation between 101 and 1000 then '2101- 1000'
            when uc.reputation between 1001 and 10000 then '31001- 10000'
            when uc.reputation between 10001 and 100000 then '410001- 100000'
            when uc.reputation > 100000 THEN '5> 100000'
        end as Reputation,
        sum(uc.num) as num
    from(    
    select u.reputation, count(*) as num
    from `bigquery-public-data.stackoverflow.users` u
    inner join(
        select c.user_id
        from `bigquery-public-data.stackoverflow.comments` c
        inner join (
            select id from `bigquery-public-data.stackoverflow.posts_questions`
            where answer_count = 0 and tags like '%"""

    query_unanswered2 = keyword

    query_unanswered3 = """%') q
        on post_id = q.id)
    on id = user_id
    group by reputation
    order by reputation asc) uc
    group by Reputation
    order by Reputation
    """
    aggregated = query_unanswered1+query_unanswered2+query_unanswered3
    df_reputation2 = stackoverflow.query_to_pandas(aggregated)
    df_reputation2 = del_order_mark(df_reputation2)
    
    reputation_json2 = df_reputation2.to_json(orient = 'index')
    #print(df_reputation2)
    
#     labels = df_reputation2.Reputation
#     sizes = round(100 * df_reputation2.num / df_reputation2.num.sum(),2)
#     #colors = ['#EC7063','#3498DB','#F7DC6F','#BB8FCE','#2ECC71']
#     colors = ['#AEB6BF', '#A569BD','#CD5C5C', '#F39C12', '#27AE60']
#     explode = (0.05,0.05,0.05,0.05,0.05)

#     fig1, ax1 = plt.subplots()
#     ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode)
#     ax1.axis('equal')  
#     plt.tight_layout()
#     plt.title("Reputation of the user making comments to unanswered questions associated with given Tag", fontsize = 14)
    
    return reputation_json2  


# Display as Table in UI*****Top 10 most viewed questions in 2020 for Given 1 tag only: (Current Trends)
def Topviewed_questions(keyword):                                   ## takes 1 parameter only
    #keyword = 'python'
    query_topques1 = """SELECT id, title, answer_count answers, favorite_count favs,
                        view_count views, score votes
                        FROM `bigquery-public-data.stackoverflow.posts_questions` 
                        WHERE EXTRACT(YEAR FROM creation_date)= 2020 AND tags like '%"""
    query_topques2 = keyword
    query_topques3 = """%'
                        order by views DESC 
                        LIMIT 10
                        """
    query_topques = query_topques1+query_topques2+query_topques3
    topques = stackoverflow.query_to_pandas(query_topques)
    topques = topques.fillna(0.0)
    topques_JSON = topques.to_json(orient = 'index')
    #print(topques)
    return topques_JSON


### (Current Trends page) Number of questions posted & number of questions been answered for given 1 Tag Only :
#@app.route('/answered-ques', methods=['GET', 'POST'])
def Answered_questions(keyword):                       #takes 1 parameter
    #keyword = 'python'
    query_answer1  = """SELECT
      EXTRACT(YEAR FROM creation_date) AS Year,
      COUNT(*) AS Number_of_Questions,
      SUM(IF(answer_count > 0, 1, 0)) AS Number_Questions_with_Answers
    FROM
      `bigquery-public-data.stackoverflow.posts_questions` where tags like '%"""
    query_answer2 = keyword
    query_answer3 = """%'
    GROUP BY
      Year
    ORDER BY
      Year;
            """
    query_answer = query_answer1+query_answer2+query_answer3
    answer_rate = stackoverflow.query_to_pandas(query_answer)
    answer_rate = answer_rate.set_index('Year')
    #print(answer_rate)
    answer_rate_json = answer_rate.to_json(orient= 'index')
    
    return answer_rate_json


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/tags', methods=['GET'])
def tags():
    queryFetchTopTags = """SELECT Category, COUNT(*) AS TagsTotal 
    FROM `bigquery-public-data.stackoverflow.posts_questions` 
    CROSS JOIN UNNEST(SPLIT(tags, '|')) AS Category 
    GROUP BY Category 
    Order By TagsTotal Desc 
    LIMIT 25"""
    df = stackoverflow.query_to_pandas(queryFetchTopTags)
    tagList = df['Category'].to_list()
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
    reputation_json1 = Reputation_answered('python')   
    reputation_json2 = Reputation_unanswered('python')
    topviewed_questions = Topviewed_questions('python')
    answered_questions = Answered_questions('python')

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
