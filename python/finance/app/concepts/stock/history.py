from ..interactor import Interactor

from queries import USER_CONTRACTS_QUERY

class History(Interactor):
  def __init__(self, session, db):
    self.session  = session
    self.db       = db
    self.user_id  = session["user_id"]

    super().__init__()

  def call(self):
    steps = [
      self.__fetch_user_contracts
    ]

    self._interact(steps)

  def __fetch_user_contracts(self):
    self.contracts = self.db.execute(USER_CONTRACTS_QUERY, user_id=self.user_id)