# Google Calender events from Google Oauth2 authentication 
## Steps to run the project

 - Get the required credentials for google oauth2 server client refer to this [link](https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred) 
-	download the json file from google cloud console or fill the credentials.json file in the root directory with fields mentioned in the file.
-	run the following commands in root directory
	create environment
 ``` python -m venv env ```
	download dependencies
``` pip install -r requirements.txt ```
	run migrations 
<code> python manage.py makemigrations
python manage.py migrate </code>
	run server 
``` python manage.py runserver localhost:8001```
- Now the sever is active and running

## Endpoints

1. /rest/v1/calendar/init 
	This endpoint initiate a Oauth flow and generates a authorization url which the user uses to provide consent to the application.

2. /rest/v1/calendar/redirect
	This endpoint is the redirected endpoint tht is opened after oauth step 1 is completed and  returns all the upcoming events for the chosen google account in the oauth step.
