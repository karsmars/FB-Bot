### app.py

This file contains our flask app which has two routes. One is to handle the initial check Facebook does to check to make sure that there is a webhook (the GET request) and the other parses, responds, and logs messages registering new English unit Leaders (the POST request).

https://developers.facebook.com/docs/messenger-platform


### client_secrets.json

This file allows a new user to authenticate their Google account to our application if there are no active credentials in credentials.json. In our current implementation it is not used often, since credential generation is only required once and the Google account that our referral files are in never changes. This will never be used in deploy and will be replaced with the contents of the Verify folder if the Google account ever does need to change.


### credentials.json

This file contains login credentials for our application that allow us to connect to Google Drive using OAuth 2.0. This is used by the GoogleAuth package inside of pydrive.


### Procfile

A file for Heroku. It lets Heroku know that there is an application that it's supposed to run and how it's supposed to run it. In this case the command contained in the Procfile is "web: gunicorn app:app --log-file=-". Breaking the contents down, it means that the type of dyno that Heroku needs to run is a web Dyno and to start it with gunicorn, targeting a Python app named app.py and logging any errors to the standard error stream. Eventually another clock process will be added to this file which will run the local application for us. For further reading on the contents of the Procfile:

https://devcenter.heroku.com/articles/procfile

http://docs.gunicorn.org/en/stable/settings.html

https://devcenter.heroku.com/articles/scheduler#dyno-hour-costs

https://devcenter.heroku.com/articles/clock-processes-python


### requirements.txt

A file for Heroku. Lists the dependencies that need to be installed for the app to run. Requirements are installed using the command "pip install -r requirements.txt".


### runtime.txt

A file for Heroku. Specifies that the app should be run using Python 3.6.4.


### settings.yaml

This file configures the settings for our authentication flow, allowing us to refresh our access token on the server for our app and defining the scope in which we can work. For further reading see:

https://pythonhosted.org/PyDrive/oauth.html