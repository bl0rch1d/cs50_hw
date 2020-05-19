import os
import pdb

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, fetch_user_cash
from queries import (USER_STOCKS_QUERY, CONTRACT_CREATE_QUERY, USER_UPDATE_CASH_QUERY,
                     USER_CONTRACTS_QUERY, USER_QUERY, USER_CREATE_QUERY, USER_STOCK_QUERY,
                     SYMBOLS_QUERY, USER_CASH_QUERY)

from app.concepts.auth.login import Login
from app.concepts.auth.register import Register
from app.concepts.stock.index import Index


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db", connect_args={'check_same_thread': False})


@app.route("/")
@login_required
def index():
    cash, stocks = Index(session, db).call()

    return render_template("index.html", stocks=stocks, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("missing symbol", 422)
        elif not shares:
            return apology("missing shares", 422)

        data = lookup(symbol)

        if not data:
            return apology("invalid symbol", 422)

        user_id = session["user_id"]
        company_name = data["name"]
        price = round(float(data["price"]), 2)
        total = round(float(data["price"] * float(shares)), 2)

        cash = fetch_user_cash(db, user_id)
        cash_after_contract = round((cash - total), 2)

        if cash_after_contract < 0:
            return apology("insufficient funds", 422)

        db.execute(
            CONTRACT_CREATE_QUERY,
            user_id=user_id,
            company_name=company_name,
            price=price,
            symbol=symbol,
            shares=shares,
            total=total
        )

        db.execute(
            USER_UPDATE_CASH_QUERY,
            cash_after_contract=cash_after_contract,
            user_id=user_id
        )

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    contracts = db.execute(USER_CONTRACTS_QUERY, user_id=session["user_id"])

    return render_template("history.html", contracts=contracts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        Login(request, session, db).call()
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        quote_result = lookup(symbol)

        if not quote_result:
            return apology("invalid symbol", 422)

        return render_template("quoted.html", quote_result=quote_result)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == 'GET':
        return render_template("register.html")
    else:
        Register(request, session, db).call

    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("must provide symbol", 422)
        elif not shares:
            return apology("must provide shares", 422)

        stock = db.execute(USER_STOCK_QUERY, user_id=user_id, symbol=symbol)[0]

        user_cash = db.execute(USER_CASH_QUERY, user_id=user_id)[0]["cash"]

        if stock["total_shares"] - shares < 0:
            return apology("too many shares ", 400)

        current_data = lookup(symbol)

        cash_after_contract = user_cash + (current_data["price"] * shares)
        company_name = current_data["name"]
        price = round(float(current_data["price"]), 2)
        total = round(float(current_data["price"] * shares), 2)
        contract_shares = shares - shares * 2

        db.execute(
            USER_UPDATE_CASH_QUERY,
            cash_after_contract=cash_after_contract,
            user_id=user_id
        )

        db.execute(
            CONTRACT_CREATE_QUERY,
            user_id=user_id,
            company_name=company_name,
            price=price,
            symbol=symbol,
            shares=contract_shares,
            total=total
        )

        return redirect("/")
    else:
        symbols = []

        symbols_query = db.execute(SYMBOLS_QUERY, user_id=user_id)

        for symbol in symbols_query:
            if not symbol["symbol"] in symbols:
                symbols.append(symbol["symbol"])

        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
