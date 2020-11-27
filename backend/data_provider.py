import os

import bq_helper


class DataProvider(object):
    def __init__(self, credential_file_path):
        self.credential_file = credential_file_path

    def getEScoreDataForTag(self, tag_name):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credential_file
        stackoverflow = bq_helper.BigQueryHelper("bigquery-public-data", "stackoverflow")
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
            where 
            extract(year from creation_date) >= 2012 
            and extract(year from creation_date) < 2020 
            and tags LIKE '%|{tag_name}|%'
            group by cdate
            order by cdate
            """
        return stackoverflow.query_to_pandas(query)