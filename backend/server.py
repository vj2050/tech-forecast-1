import json
import sys

from flask import Flask, request
from flask import json
from flask_cors import CORS

from data_provider import DataProvider
from forecast_generator import ForecastGenerator
import pandas as pd

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
    trend.set_index('cdate', inplace=True)
    curr_trendsjson = trend.to_json(orient="index")

    reputation_json1 = data_provider.user_reputation_answered(tag)
    reputation_json2 = data_provider.user_reputation_unanswered(tag)
    topviewed_questions = data_provider.top_viewed_questions(tag, 10)
    answered_questions = data_provider.answered_questions(tag)

    curr_trendsjson = json.loads(curr_trendsjson)  # converting JSON string to dictionary
    reputation_json1 = json.loads(reputation_json1)  # converting JSON string to dictionary
    reputation_json2 = json.loads(reputation_json2)  # converting JSON string to dictionary
    topviewed_questions = json.loads(topviewed_questions)
    answered_questions = json.loads(answered_questions)

    payload = {  # merged Dictionary
        'current_trends': curr_trendsjson,
        'reputation_answered': reputation_json1,
        'reputation_unanswered': reputation_json2,
        'Top_viewed_questions': topviewed_questions,
        'Answered_Questions': answered_questions
    }

    final_payload = json.dumps(payload)  # converting dictionary back to JSON object

    return (final_payload)


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
    future_trendsjson = final.to_json(orient="index")
    return future_trendsjson


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
