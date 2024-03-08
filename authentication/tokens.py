# from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

# def get_tokens_for_user(user):
#     access_token = str(AccessToken.for_user(user))
#     refresh_token = str(RefreshToken.for_user(user))

#     return {
#         'access_token':  access_token,
#         'refresh_token': refresh_token,
#     }


from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from datetime import datetime, timedelta


def get_tokens_for_user(user):
    access_token_expire = datetime.utcnow() + timedelta(hours=12)
    refresh_token_expire = datetime.utcnow() + timedelta(days=4)

    access_token = str(AccessToken.for_user(user))
    refresh_token = str(RefreshToken.for_user(user))

    access_token_expire_in_seconds = int((access_token_expire - datetime.utcnow()).total_seconds())
    refresh_token_expire_in_seconds = int((refresh_token_expire - datetime.utcnow()).total_seconds())

    return {
        'access_token':  {
            'token': access_token,
            'expire_in_seconds': access_token_expire_in_seconds,
        },
        'refresh_token': {
            'token': refresh_token,
            'expire_in_seconds': refresh_token_expire_in_seconds,
        }
    }