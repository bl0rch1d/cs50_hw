from ..interactor import Interactor

from helpers import lookup
from queries import USER_STOCK_QUERY, USER_CASH_QUERY, CONTRACT_CREATE_QUERY, USER_UPDATE_CASH_QUERY

class Sell(Interactor):
  def __init__(self, request, session, db):
    self.request    = request
    self.session    = session
    self.db         = db

    self.symbol     = request.form.get("symbol")
    self.shares     = request.form.get("shares")

    self.user_id    = session["user_id"]

    super().__init__()

  def call(self):
    steps = [
      self.__validate_input,
      self.__fetch_symbol_data,
      self.__validate_shares_count,
      self.__fetch_user_cash,
      self.__calculate_expenses,
      self.__build_data_payload,
      self.__create_contract,
      self.__update_user
    ]

    self._interact(steps)

  def __validate_input(self):
    if not self.symbol:
      self.operation_message = 'must provide symbol'
      self.operation_status = 422
      return

    elif not self.shares:
      self.operation_message = 'must provide shares'
      self.operation_status = 422
      return

  def __fetch_symbol_data(self):
    self.symbol = self.symbol.upper()
    self.symbol_data = lookup(self.symbol)

    if not self.symbol_data:
      self.operation_message = 'invalid symbol'
      self.operation_status = 422
      return

  def __validate_shares_count(self):
    self.shares = int(self.shares)
    stock = self.db.execute(USER_STOCK_QUERY, user_id=self.user_id, symbol=self.symbol)[0]

    if stock["total_shares"] - self.shares < 0:
      self.operation_message = 'too many shares'
      self.operation_status = 400
      return

  def __fetch_user_cash(self):
    cash = self.db.execute(USER_CASH_QUERY, user_id=self.user_id)[0]["cash"]

    self.__user_cash = round(float(cash), 2)

  def __calculate_expenses(self):
    self.__cash_after_contract = self.__user_cash + (self.symbol_data["price"] * self.shares)

    self.company_name = self.symbol_data["name"]
    self.price = round(float(self.symbol_data["price"]), 2)
    self.total = round(float(self.symbol_data["price"] * self.shares), 2)
    self.__contract_shares = self.shares - self.shares * 2

  def __build_data_payload(self):
    self.__user_update_payload = {
      'cash_after_contract': self.__cash_after_contract,
      'user_id': self.user_id
    }

    self.__contract_payload = {
      'user_id': self.user_id,
      'company_name': self.company_name,
      'price': self.price,
      'symbol': self.symbol,
      'shares': self.__contract_shares,
      'total': self.total
    }

  def __create_contract(self):
    self.db.execute(CONTRACT_CREATE_QUERY, **self.__contract_payload)

  def __update_user(self):
    self.db.execute(USER_UPDATE_CASH_QUERY, **self.__user_update_payload)