from ..interactor import Interactor

from werkzeug.security import check_password_hash
from queries import USER_QUERY
from helpers import apology

class Login(Interactor):
  def __init__(self, request, session, db):
    self.request  = request
    self.session  = session
    self.db       = db

    self.username = request.form.get("username")
    self.password = request.form.get("password")

    self.__clear_session()

    super().__init__()

  def call(self):
    steps = [
      self.__validate_input,
      self.__fetch_user,
      self.__validate_credentials,
      self.__create_session
    ]

    self._interact(steps)

  def __clear_session(self):
    self.session.clear()

  def __validate_input(self):
    if not self.username:
      self.operation_message = 'must provide username'
      self.operation_status = 403 
      return

    elif not self.password:
      self.operation_message = 'must provide password'
      self.operation_status = 403 
      return

  def __fetch_user(self):
    user_query = self.db.execute(USER_QUERY, username=self.username)

    if len(user_query) != 1:
      return self.__invalid_credentials()

    self.user = user_query[0]

  def __validate_credentials(self):
    encrypted_password = self.user["hash"]

    valid_password = check_password_hash(encrypted_password, self.password)

    if not valid_password:
      return self.__invalid_credentials()

  def __create_session(self):
    self.session["user_id"] = self.user["id"]

  def __invalid_credentials(self):
    self.operation_message = 'invalid username and/or password'
    self.operation_status = 403 
