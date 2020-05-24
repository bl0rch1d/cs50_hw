from ..interactor import Interactor

from queries import USER_CASH_QUERY, USER_STOCKS_QUERY

class Index(Interactor):
  def __init__(self, session, db):
    self.session = session
    self.db      = db

    self.user_id = session["user_id"]

    self.user_cash = 0
    self.user_stocks = []

    super().__init__()

  def call(self):
    steps = [
      self.__fetch_user_cash,
      self.__fetch_user_stocks
    ]

    self._interact(steps)

  def __fetch_user_cash(self):
    cash = self.db.execute(USER_CASH_QUERY, user_id=self.user_id)[0]["cash"]

    self.user_cash = round(float(cash), 2)

  def __fetch_user_stocks(self):
    self.user_stocks = self.db.execute(USER_STOCKS_QUERY, user_id=self.user_id)
