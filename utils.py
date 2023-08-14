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



from kavenegar import *
from datetime import datetime, timedelta, timezone
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code):
    # try:
    #     api = KavenegarAPI(
    #         '70504E2B5A593946534677652F365455676858767438547043773248567A5872616578474B4E76784A50383D'
    #     )

    #     params = {
    #         'sender': '',
    #         'receptor': phone_number,
    #         'message': f'کد تایید شما\n {code}'
    #     }

    #     response = api.sms_send(params)
    #     print('*'*90)
    #     print(response)

    # except APIException as e:
    #     print(e)
    # except HTTPException as e:
    #     print(e)
    pass



def check_code_expire(code_time, minutes=2, success_callback=None, error_callback=None):
    if (datetime.now(timezone.utc) - code_time <= timedelta(minutes=minutes)):
        if success_callback: success_callback()
        print('True')
        return True
    else:
        if error_callback: error_callback()
        print('False')
        return False
        
        

class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin