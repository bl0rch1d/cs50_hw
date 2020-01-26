import os
import pdb

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
    """Show portfolio of stocks"""

    user_id = session["user_id"]

    cash = round(float(db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)[0]["cash"]), 2)

    stocks = db.execute(
        """
        SELECT symbol, company_name, SUM(shares) AS total_shares, price, SUM(total) AS total_price
        FROM contracts
        WHERE user_id = :user_id
        GROUP BY symbol
        HAVING total_shares > 0
        """,
        user_id=user_id
    )

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

        cash = round(float(db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)[0]["cash"]), 2)

        cash_after_contract = round((cash - total), 2)

        if cash_after_contract < 0:
            return apology("insufficient funds", 422)

        db.execute(
            """INSERT INTO contracts (user_id, company_name, price, symbol,
            shares, total) VALUES (:user_id, :company_name, :price,
            :symbol, :shares, :total)""",
            user_id=user_id,
            company_name=company_name,
            price=price,
            symbol=symbol,
            shares=shares,
            total=total
        )

        db.execute(
            "UPDATE users SET cash = :cash_after_contract WHERE id = :user_id",
            cash_after_contract=cash_after_contract,
            user_id=user_id
        )

        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    contracts = db.execute("SELECT * FROM contracts WHERE user_id = :user_id ORDER BY created_at DESC", user_id=session["user_id"])

    return render_template("history.html", contracts=contracts)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
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
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 422)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 422)

        # Ensure confiration was submitted with the same value as password
        elif not confirmation or not password == confirmation:
            return apology("must provide correct confiration", 422)

        # Query database for username
        user_exists = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)

        # Check username for uniqueuness
        if user_exists:
            return apology("such username already exists", 422)

        # Encrypt password
        encrypted_password = generate_password_hash(password)

        # Create db record for new user
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",
            username=username, password=encrypted_password)

        # Get user_id from db
        user_id = db.execute("SELECT id FROM users WHERE username == :username", username=username)[0]["id"]

        # Remember which user has logged in
        session["user_id"] = user_id

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

        stock = db.execute("SELECT SUM(shares) AS total_shares, SUM(total) AS total_price, company_name FROM contracts WHERE user_id = :user_id AND symbol = :symbol",
            user_id=user_id, symbol=symbol)[0]

        user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)[0]["cash"]

        if stock["total_shares"] - shares < 0:
            return apology("too many shares ", 400)

        current_data = lookup(symbol)

        user_cash = user_cash + (current_data["price"] * shares)
        company_name = current_data["name"]
        price = round(float(current_data["price"]), 2)
        total = round(float(current_data["price"] * shares), 2)
        contract_shares = shares - shares * 2

        db.execute(
            "UPDATE users SET cash = :user_cash WHERE id = :user_id",
            user_cash=user_cash,
            user_id=user_id
        )

        db.execute(
            """INSERT INTO contracts (user_id, company_name, price, symbol,
            shares, total) VALUES (:user_id, :company_name, :price,
            :symbol, :shares, :total)""",
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

        symbols_query = db.execute(
            """
            SELECT symbol, SUM(shares) AS total_shares
            FROM contracts
            WHERE user_id = :user_id
            GROUP BY symbol
            HAVING total_shares > 0
            """,
            user_id=user_id
        )

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
