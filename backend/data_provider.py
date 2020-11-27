import os

import bq_helper


class DataProvider(object):
    def __init__(self, credential_file_path):
        self.credential_file = credential_file_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credential_file
        self.stackoverflow = bq_helper.BigQueryHelper("bigquery-public-data", "stackoverflow")

    def escore_data_for_tag(self, tag_name):
        h1 = 0.1
        h2 = 0.000001
        h3 = 0.005
        h4 = 0.001
        h5 = 0.1
        query = f"""select 
            DATE(creation_date) AS cdate, 
            (({h1}) * (COUNT(*) ) +
            ({h2}) * (SUM(view_count)/COUNT(*) ) +
            ({h3}) * (SUM(score)/COUNT(*) ) +
            ({h4}) * (SUM(IFNULL(favorite_count,0))/COUNT(*) ) +
            ({h5}) * (COUNT(DISTINCT accepted_answer_id)/COUNT(*) ) ) as eScore,
            
            from `bigquery-public-data.stackoverflow.posts_questions`
            where post_type_id=1 and
            extract(year from creation_date) >= 2012 
            and extract(year from creation_date) < 2020 
            and tags LIKE '%|{tag_name}|%'
            group by cdate
            order by cdate
            """
        return self.stackoverflow.query_to_pandas(query)

    def get_top_tags(self, limit):
        queryFetchTopTags = f"""SELECT Category, COUNT(*) AS TagsTotal 
        FROM `bigquery-public-data.stackoverflow.posts_questions` 
        CROSS JOIN UNNEST(SPLIT(tags, '|')) AS Category 
        GROUP BY Category 
        Order By TagsTotal Desc 
        LIMIT {limit}"""
        df = self.stackoverflow.query_to_pandas(queryFetchTopTags)
        tagList = df['Category'].to_list()
        return tagList