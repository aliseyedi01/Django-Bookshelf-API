from rest_framework_simplejwt.tokens import RefreshToken , AccessToken

def get_tokens_for_user(user):
    access_token = str(AccessToken.for_user(user))
    refresh_token = str(RefreshToken.for_user(user))

    return {
        'access_token':  access_token,
        'refresh_token': refresh_token,
    }