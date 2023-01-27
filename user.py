from flask import Flask, session, g
from models import User


CURR_USER_KEY = 'current_user'


############################################################################
# USER LOGIN/LOGOUT FUNCTIONS
############################################################################

def login_user(user):
    """Logs in user."""
    session[CURR_USER_KEY] = user.id


def logout_user():
    """Logs out user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
