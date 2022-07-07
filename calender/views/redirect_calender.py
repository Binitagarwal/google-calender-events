from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from calender.models import *
import json


class GoogleCalendarRedirectView(APIView):

    def getCredsFromState(self, user:CustomUser):
        if user.credentials_json is None:
            return None
        token = user.credentials_json['access_token']
        refresh_token = user.credentials_json['refresh_token']
        scopes = user.credentials_json['scope']
        with open(settings.CREDS_PATH, 'r') as f:
            data = json.load(f)
            client_id = data['web']['client_id']
            client_secret = data['web']['client_secret']
        creds = Credentials(
            token=token, 
            refresh_token=refresh_token, 
            token_uri=settings.REDIRECT_URI, 
            client_id=client_id, 
            client_secret=client_secret, 
            scopes=scopes
        )
        return creds

    def get(self, request, *args, **kwargs):
        try:
            code = request.query_params.get('code')
            state = request.query_params.get('state')
            if CustomUser.objects.filter(state=state).exists():
                user = CustomUser.objects.get(state=state)
            else:
                return Response({"error": "Invalid state"}, status=400)

            creds = self.getCredsFromState(user)

            response = {}
            if creds is None:
                flow = Flow.from_client_secrets_file(settings.CREDS_PATH, settings.SCOPES)
                flow.redirect_uri = settings.REDIRECT_URI
                token = flow.fetch_token(code=code)
                user.credentials_json = token
                user.save()
                user.resolved = True
                user.save()
                credentials = flow.credentials
            else:
                credentials = creds

            service = build('calendar', 'v3', credentials=credentials)
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                 singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            if events == []:
                response['events'] = 'No upcoming events found.'
            else:
                response['events'] = events

        except Exception as e:
            return Response({"error": str(e)}, status=400)

        response['status'] = 'success'
        return Response(response, status=200)