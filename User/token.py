from rest_framework_simplejwt.tokens import RefreshToken


class GenerateToken:

    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        data = {
            'refresh_token': str(token),
            'access_token': str(token.access_token),
        }
        return data
