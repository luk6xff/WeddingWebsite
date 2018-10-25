* Make sure you have Python3 installed

* Enable Google Drive API
# GD API setup instructions: https://developers.google.com/drive/api/v3/quickstart/python, gsheets handles it
Step 1: Turn on the Drive API
Click this button to create a new console project and automatically enable the Drive API:

ENABLE THE DRIVE API
This opens a new dialog. In the dialog, do the following:
Select + Create a new project.
Download the configuration file.
Move the downloaded file to your working directory and ensure it is named credentials.json.

* Install proper python packages
$ pip install twilio
$ pip install gsheets

* Test the GD API the scripts
$ python quickstart.py

* Create account on Twilio: https://www.twilio.com
Go https://www.twilio.com/console/phone-numbers/incoming and create your phone number.

* Modify wedding_utils_config.ini file according to your settings

* Create an excel file on your Google Drive in the format like: Wesele_27-10-2018.xlsx

* Open twilio_bot.py and modify:  msg_1 = 'Cześć, Tutaj wpisz swoja wiadomosc'

* Run:
$ python twilio_bot.py
