from flask import Flask, jsonify, request, abort

STOCKS = {
    "NFLX": {
        'companyName': "Netflix",
        'latestPrice': 353.16,
        'symbol': "NFLX"
    },

    "TSLA": {
        'companyName': "Tesla",
        'latestPrice': 564.82,
        'symbol': "TSLA"
    },

    "GOOGL": {
        'companyName': "Alphabet Inc Class A",
        'latestPrice': 1477.17,
        'symbol': "GOOGL"
    },

    "AAPL": {
        'companyName': "Apple",
        'latestPrice': 318.31,
        'symbol': "AAPL"
    }
}

app = Flask(__name__)


@app.route("/")
def index():
    symbol = request.args.get('quote')

    if not symbol:
        return abort(400)

    symbol = symbol.upper()

    if symbol not in STOCKS:
        return abort(404)

    return jsonify(STOCKS[symbol])
