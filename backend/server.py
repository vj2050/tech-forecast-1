import json
import sys

from flask import Flask, request
from flask import json
from flask_cors import CORS


from data_provider import DataProvider
from forecast_generator import ForecastGenerator
import pandas as pd
import numpy as np
app = Flask(__name__)
CORS(app)

data_provider = DataProvider(credential_file_path=sys.argv[1])
forecast_generator = ForecastGenerator(predict_years=2)


@app.route('/tags', methods=['GET'])
def tags():
    tagList = sorted(data_provider.get_top_tags(limit=50))
    return json.dumps(tagList)


@app.route('/current-trends', methods=['POST', 'GET'])
def current_trends():
    tag = "java"
    trend = data_provider.escore_data_for_tag(tag)
    trend['cdate'] = pd.to_datetime(trend['cdate'])
    trend.set_index('cdate', inplace=True)
    trend = trend.resample('MS').sum()
    curr_trendsjson = trend.to_json(orient="index")
    return curr_trendsjson


@app.route('/current-trends/rep/answered', methods=['POST', 'GET'])
def userRepForAnswered():
    tag = "java"
    reputation = data_provider.user_reputation_answered(tag)
    return reputation.to_json(orient='index')


@app.route('/current-trends/rep/unanswered', methods=['POST', 'GET'])
def userRepForUnAnswered():
    tag = "java"
    reputation = data_provider.user_reputation_unanswered(tag)
    return reputation.to_json(orient='index')


@app.route('/current-trends/ques/top', methods=['POST', 'GET'])
def topQuestions():
    tag = "java"
    questions = data_provider.top_viewed_questions(tag, 10)
    return questions.to_json(orient='index')


@app.route('/current-trends/ques/answered', methods=['POST', 'GET'])
def answeredQuestions():
    tag = "java"
    questions = data_provider.answered_questions(tag)
    return questions.to_json(orient='index')


@app.route('/future-trends', methods=['POST', 'GET'])
def future_trends():
    tags = request.args.get("name").split(',')
    final = pd.DataFrame()
    for tag in tags:
        print(tag)
        data = data_provider.escore_data_for_tag(tag)
        forecast = forecast_generator.forecast(data)
        forecast.rename({"val": tag}, axis='columns', inplace=True)
        print(forecast.keys())
        if final.empty:
            final = forecast
        else:
            final = pd.concat([final, forecast], axis=1, sort=False)
    return final.to_json(orient="index")


@app.route('/comparison', methods=['GET', 'POST'])
def compare_trends():
    # TODO: Make calls for multiple keywords for comparison
    tag = "java"
    trend = data_provider.escore_data_for_tag(tag)
    trend.set_index('cdate', inplace=True)
    curr_trendsjson = trend.to_json(orient="index")

    return curr_trendsjson


if __name__ == "__main__":
    app.run(debug=True)
