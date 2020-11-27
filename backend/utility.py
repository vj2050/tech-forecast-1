# def CurrentTrends_merge():
#     query1 = "select EXTRACT(year FROM creation_date) AS year, COUNT(id) as posts from `bigquery-public-data.stackoverflow.posts_questions` where extract(year from creation_date) >=2009 and extract(year from creation_date) < 2021 and tags like '%"
#     query3 = "%' group by year order by year"
#     df = []
#     labels = []
#
#     dfall = ["html", "kubernetes"]
#
#     if labels == None:
#         labels = dfall  # the keywords list
#
#     l = len(dfall)
#     ###### for every tag, execute the query separately
#     for i in range(l):
#         query2 = dfall[i]  # dfall = ['hadoop','spark','hive']
#         query = query1 + query2 + query3
#         Posts = stackoverflow.query_to_pandas(query)
#         Posts['posts'] = Posts['posts'] * 100 / PostsCount.posts
#         pd.to_numeric(Posts['year'])
#         Posts.rename(columns={'posts': dfall[i]}, inplace=True)
#         df.append(Posts)
#
#     trend = pd.DataFrame(df[0])
#     trend = trend.set_index('year')
#
#     if (l > 1):
#         for i in range(1, l):
#             trend = pd.merge(trend, df[i], how='outer', on='year')
#             trend = trend.set_index('year')
#             trend = trend.fillna(0)
#
#     return trend

## Should be displayed as TABLE **** Use below function for email notifications part : Top trending tags from 1st Jan 2020 to 6th September 2020
### (last date of updation..  next quarterly update in December)


# def top_tags():
#     query_testing = """SELECT tag, COUNT(*) c
#     FROM (
#       SELECT SPLIT(tags, '|') tags
#       FROM `bigquery-public-data.stackoverflow.posts_questions` a
#       WHERE EXTRACT(DATE FROM creation_date)>= '2020-01-01' AND EXTRACT(DATE FROM creation_date)<= '2020-09-06'
#     ), UNNEST(tags) tag
#     GROUP BY 1
#     ORDER BY 2 DESC
#     LIMIT 10
#     """
#
#     query_toptags = stackoverflow.query_to_pandas(query_testing)
#     toptags_json = query_toptags.to_json(orient='index')
#     return toptags_json
#
#
# # Display as TABLE (For Notifications Email Functionality) Top 10 most viewed Questions in general in current year 2020
# def Topviewed_general():
#     query_topGen = """SELECT id, title, answer_count answers, favorite_count favs,
#                         view_count views, score votes
#                         FROM `bigquery-public-data.stackoverflow.posts_questions`
#                         WHERE EXTRACT(YEAR FROM creation_date)= 2020
#                         order by views DESC
#                         LIMIT 10
#                         """
#
#     topGen = stackoverflow.query_to_pandas(query_topGen)
#     topGen = topGen.fillna(0.0)
#     topGen_JSON = topGen.to_json(orient='index')
#     print(topGen)
#     return topGen_JSON

def del_order_mark(df):
    new_Reputation = []
    for i in range(len(df)):  # delete the order mark in "repulation"
        new_Reputation.append(df['Reputation'][i][1:])
    df.Reputation = new_Reputation
    return df

