from ..interactor import Interactor

from werkzeug.security import generate_password_hash
from queries import USER_QUERY, USER_CREATE_QUERY

class Register(Interactor):
  def __init__(self, request, session, db):
    self.request = request
    self.session = session
    self.db      = db

    self.username       = request.form.get("username")
    self.password       = request.form.get("password")
    self.confirmation   = request.form.get("confirmation")

    super().__init__()

  def call(self):
    steps = [
      self.__validate_input,
      self.__check_user_uniqueness,
      self.__generate_password,
      self.__persist,
      self.__create_session
    ]

    self._interact(steps)

  def __validate_input(self):
    if not self.username:
      self.operation_message = 'must provide username'
      self.operation_status = 422
      return

    elif not self.password:
      self.operation_message = 'must provide password'
      self.operation_status = 422
      return

    elif not self.confirmation or not self.password == self.confirmation:
      self.operation_message = 'must provide correct confiration'
      self.operation_status = 422
      return

  def __check_user_uniqueness(self):
    user_exists = self.db.execute(USER_QUERY, username=self.username)

    if user_exists:
      self.operation_message = 'such username already exists'
      self.operation_status = 422
      return

  def __generate_password(self):
    self.encrypted_password = generate_password_hash(self.password)

  def __persist(self):
    self.db.execute(USER_CREATE_QUERY, username=self.username, password=self.encrypted_password)

  def __create_session(self):
    user_id = self.db.execute(USER_QUERY, username=self.username)[0]["id"]

    self.session["user_id"] = user_id
