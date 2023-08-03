# NOTE 
### how using SESSIONS ###

# >>> # initial assignment
# >>> request.session[0] = "bar"
# >>> # subsequent requests following serialization & deserialization
# >>> # of session data
# >>> request.session[0]  # KeyError
# >>> request.session["0"]
# 'bar'


### when modified ###

# # Session is modified.
# request.session["foo"] = "bar"

# # Session is modified.
# del request.session["foo"]

# # Session is modified.
# request.session["foo"] = {}

# # Gotcha: Session is NOT modified, because this alters
# # request.session['foo'] instead of request.session.
# request.session["foo"]["bar"] = "baz"


def send_otp_code(phone_number, code):
    pass
