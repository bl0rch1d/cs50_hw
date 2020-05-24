from ..interactor import Interactor

from queries import SYMBOLS_QUERY

class SellIndex(Interactor):
  def __init__(self, session, db):
    self.session  = session
    self.db       = db
    self.user_id  = session['user_id']

    super().__init__()

  def call(self):
    steps = [
      self.__fetch_user_symbols
    ]

    self._interact(steps)

  def __fetch_user_symbols(self):
    self.symbols = []

    symbols_query = self.db.execute(SYMBOLS_QUERY, user_id=self.user_id)

    for symbol in symbols_query:
      if not symbol["symbol"] in self.symbols:
        self.symbols.append(symbol["symbol"])