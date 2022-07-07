from django.urls import path
from calender.views import *

urlpatterns = [
    path('init',GoogleCalenderInitView.as_view()),
    path('redirect',GoogleCalendarRedirectView.as_view()),
]