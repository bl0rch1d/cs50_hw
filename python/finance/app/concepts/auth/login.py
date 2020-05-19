from werkzeug.security import check_password_hash
from queries import USER_QUERY
from helpers import apology

class Login():
    def __init__(self, request, session, db):
        self.request  = request
        self.session  = session
        self.db       = db

        self.username = request.form.get("username")
        self.password = request.form.get("password")

        self.__clear_session()

    def call(self):
        self.__perform_login()

    def __clear_session(self):
        self.session.clear()

    def __perform_login(self):
        self.__validate_input()
        self.__fetch_user()
        self.__validate_credentials()
        self.__create_session()

    def __validate_input(self):
        if not self.username:
            return apology("must provide username", 403)
        elif not self.password:
            return apology("must provide password", 403)

    def __fetch_user(self):
        self.user = self.db.execute(USER_QUERY, username=self.username)[0]

        if len(self.user) != 1:
            self.__invalid_credentials()

    def __validate_credentials(self):
        encrypted_password = self.user["hash"]

        valid_password = check_password_hash(encrypted_password, self.password)

        if not valid_password:
            self.__invalid_credentials()

    def __create_session(self):
        self.session["user_id"] = self.user["id"]

    def __invalid_credentials(self):
        return apology("invalid username and/or password", 403)
