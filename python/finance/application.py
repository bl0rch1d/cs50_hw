import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology, login_required, usd

from app.concepts.auth.login import Login
from app.concepts.auth.register import Register
from app.concepts.stock.index import Index
from app.concepts.stock.buy import Buy
from app.concepts.stock.quote import Quote
from app.concepts.stock.sell import Sell
from app.concepts.stock.sell_index import SellIndex
from app.concepts.stock.history import History

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
  operation = Index(session, db)
  operation.call()

  if operation.operation_status != 0:
    return apology(operation.operation_message, operation.operation_status)

  return render_template("index.html", stocks=operation.user_stocks, cash=operation.user_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
  if request.method == "POST":
    operation = Buy(request, session, db)
    operation.call()

    if operation.operation_status != 0:
      return apology(operation.operation_message, operation.operation_status)

    return redirect("/")

  return render_template("buy.html")


@app.route("/history")
@login_required
def history():
  operation = History(session, db)
  operation.call()

  return render_template("history.html", contracts=operation.contracts)


@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    operation = Login(request, session, db)
    operation.call()

    if operation.operation_status != 0:
      return apology(operation.operation_message, operation.operation_status)

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
  if request.method == "POST":
    operation = Quote(request)
    operation.call()

    if operation.operation_status != 0:
      return apology(operation.operation_message, operation.operation_status)

    return render_template("quoted.html", quote_result=operation.quote_result)

  else:
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == 'GET':
    return render_template("register.html")
  else:
    operation = Register(request, session, db)
    operation.call()

    if operation.operation_status != 0:
      return apology(operation.operation_message, operation.operation_status)

  return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
  if request.method == "POST":
    operation = Sell(request, session, db)
    operation.call()

    if operation.operation_status != 0:
      return apology(operation.operation_message, operation.operation_status)

    return redirect("/")
  else:
    operation = SellIndex(session, db)
    operation.call()

    if operation.operation_status != 0:
      return apology(operation.operation_message, operation.operation_status)

    return render_template("sell.html", symbols=operation.symbols)


def errorhandler(e):
  if not isinstance(e, HTTPException):
    e = InternalServerError()
  return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
  app.errorhandler(code)(errorhandler)
