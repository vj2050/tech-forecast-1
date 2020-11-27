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


def del_order_mark(df):
    new_Reputation = []
    for i in range(len(df)):  # delete the order mark in "repulation"
        new_Reputation.append(df['Reputation'][i][1:])
    df.Reputation = new_Reputation
    return df

