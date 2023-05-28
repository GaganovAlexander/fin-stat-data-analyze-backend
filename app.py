import flask
from flask_cors import CORS

from data_analysis import analyze_excel

# Creating app with CORS added, due to the fact that project has non-monolithic structure
app = flask.Flask(__name__)
CORS(app)


@app.post('/api/excel')
def excel_upload():
    # Getting buffered excel file from frontend request
    data = flask.request.files['file'].read()
    try:
        # And trying to analyze it
        result = analyze_excel(data)
    except Exception as e:
        print(e)
        # If there is any error, that means that the file is corrupted or invalidly structured
        return "Invalid or corrupted excel file", 400
    # If everything is OK, return the result with jsonify(because json.dumps just create json-like string)
    return flask.jsonify(result)


if __name__ == '__main__':
    # For local testing and debugging, in product use gunicorn or other WSGI server
    app.run(host='localhost', port=8001, debug=False)
