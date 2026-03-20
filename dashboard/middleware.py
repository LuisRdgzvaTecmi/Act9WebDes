from dashboard.models import AuthToken


class TokenAuthMiddleware:
    """
    Middleware that checks for an auth token in the session.
    If valid, attaches the corresponding CustomUser to request.custom_user.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.custom_user = None
        token_key = request.session.get('auth_token')
        if token_key:
            try:
                token = AuthToken.objects.select_related('user').get(key=token_key)
                request.custom_user = token.user
            except AuthToken.DoesNotExist:
                # Token is invalid – clean up the session
                del request.session['auth_token']
        response = self.get_response(request)
        return response
