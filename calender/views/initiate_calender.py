from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from calender.models import *
from google_auth_oauthlib.flow import Flow

creds_path = settings.CREDS_PATH
redirect_uri = settings.REDIRECT_URI
SCOPES = settings.SCOPES

class GoogleCalenderInitView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            flow = Flow.from_client_secrets_file(creds_path, SCOPES)
            flow.redirect_uri = redirect_uri
            authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
            user = CustomUser.objects.create(state=state)
        except Exception as e:
            return Response({"error": str(e)})
        return Response({
            'authorization_url': authorization_url,
            'user_id': user.id
        },status = 200)