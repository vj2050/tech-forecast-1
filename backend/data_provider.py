import os

import bq_helper

from utility import del_order_mark


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


    def user_reputation_answered(self, tag_name):
        # Reputation of the user making comments to answered questions for given tag.
        query = f"""
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
                where answer_count > 0 and tags like '%{tag_name}%') q
            on post_id = q.id)
        on id = user_id
        group by reputation
        order by reputation asc) uc
        group by Reputation
        order by Reputation
        """

        reputation = self.stackoverflow.query_to_pandas(query)
        reputation = del_order_mark(reputation)

        reputation_json1 = reputation.to_json(orient='index')

        return reputation_json1

    def user_reputation_unanswered(self, tag_name):
        # Reputation of the user making comments to answered questions for given tag.
        query = f"""
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
                where answer_count = 0 and tags like '%{tag_name}%') q
            on post_id = q.id)
        on id = user_id
        group by reputation
        order by reputation asc) uc
        group by Reputation
        order by Reputation
        """
        reputation = self.stackoverflow.query_to_pandas(query)
        reputation = self.del_order_mark(reputation)
        reputation_json2 = reputation.to_json(orient='index')

        return reputation_json2

    # Display as Table in UI*****Top 10 most viewed questions in 2020 for Given 1 tag only: (Current Trends)
    def top_viewed_questions(self, tag_name, count):  ## takes 1 parameter only
        # keyword = 'python'
        query = f"""SELECT id, title, answer_count answers, favorite_count favs,
                            view_count views, score votes
                            FROM `bigquery-public-data.stackoverflow.posts_questions` 
                            WHERE EXTRACT(YEAR FROM creation_date)= 2020 AND tags like '%{tag_name}%'
                            order by views DESC 
                            LIMIT {count}
                            """
        topques = self.stackoverflow.query_to_pandas(query)
        topques = topques.fillna(0.0)
        topques_JSON = topques.to_json(orient='index')
        return topques_JSON

    ### (Current Trends page) Number of questions posted & number of questions been answered for given 1 Tag Only :
    # @app.route('/answered-ques', methods=['GET', 'POST'])
    def answered_questions(self, tag_name):  # takes 1 parameter
        # keyword = 'python'
        query = f"""SELECT
          EXTRACT(YEAR FROM creation_date) AS Year,
          COUNT(*) AS Number_of_Questions,
          SUM(IF(answer_count > 0, 1, 0)) AS Number_Questions_with_Answers
        FROM
          `bigquery-public-data.stackoverflow.posts_questions` where tags like '%{tag_name}%'
        GROUP BY
          Year
        ORDER BY
          Year;
                """
        answer_rate = self.stackoverflow.query_to_pandas(query)
        answer_rate = answer_rate.set_index('Year')
        answer_rate_json = answer_rate.to_json(orient='index')

        return answer_rate_json
