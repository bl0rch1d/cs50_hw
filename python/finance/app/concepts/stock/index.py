from queries import USER_CASH_QUERY, USER_STOCKS_QUERY

class Index():
    def __init__(self, session, db):
        self.session = session
        self.db      = db

        self.user_id = session["user_id"]

    def call(self):
        cash    = self.__fetch_user_cash()
        stocks  = self.__fetch_user_stocks()

        return [cash, stocks]

    def __fetch_user_cash(self):
        cash = self.db.execute(USER_CASH_QUERY, user_id=self.user_id)[0]["cash"]
        return round(float(cash), 2)

    def __fetch_user_stocks(self):
        return self.db.execute(USER_STOCKS_QUERY, user_id=self.user_id)
