from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from src.TTC import TTC as tictactoe

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def hello():
    output = tictactoe(request.args.get("state"))
    return jsonify(output)