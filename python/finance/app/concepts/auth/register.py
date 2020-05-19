from werkzeug.security import generate_password_hash
from helpers import apology
from queries import USER_QUERY, USER_CREATE_QUERY

class Register():
    def __init__(self, request, session, db):
        self.request = request
        self.session = session
        self.db      = db

        self.username       = request.form.get("username")
        self.password       = request.form.get("password")
        self.confirmation   = request.form.get("confirmation")

    def call(self):
        self.__perform_register()

    def __perform_register(self):
        self.__validate_input()
        self.__check_user_uniqueness()
        self.__generate_password()
        self.__persist()
        self.__create_session()

    def __validate_input(self):
        if not self.username:
            return apology("must provide username", 422)

        elif not self.password:
            return apology("must provide password", 422)

        elif not self.confirmation or not self.password == self.confirmation:
            return apology("must provide correct confiration", 422)

    def __check_user_uniqueness(self):
        user_exists = self.db.execute(USER_QUERY, username=self.username)

        if user_exists:
            return apology("such username already exists", 422)

    def __generate_password(self):
        self.encrypted_password = generate_password_hash(self.password)

    def __persist(self):
        self.db.execute(USER_CREATE_QUERY, username=self.username, password=self.encrypted_password)

    def __create_session(self):
        user_id = self.db.execute(USER_QUERY, username=self.username)[0]["id"]

        self.session["user_id"] = user_id
