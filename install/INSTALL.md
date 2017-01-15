How to Deploy Budgeteer Application @ Local Server
=================================================
# Install Python
You need to have Python installed

## Install and Create Virtual Environment

- First you need to install pip.
- After installing pip you have to install virtualenv with ```pip install virtualenv```
- After installing virtualenv, create your virtual environment ```virtualenv venv```

## Clone this app from github
You need git for this step
Clone this app from https://github.com/tomascarvalho/Budgeteer
``` git clone https://github.com/tomascarvalho/Budgeteer ```
Now you have the source code and the requirements.txt file that tells pip all the requirements needed to run this app.

## Install the requirements with pip
Run ```pip install -r requirements.txt```

## Run the Application
Run the application with ``` python manage.py runserver ```

How to Deploy Budgeteer Application @ Heroku
============================================

## Install Python
You need to have Python installed

## Install and Create Virtual Environment
- First you need to install pip.
- After installing pip you have to install virtualenv with ```pip install virtualenv```
- After installing virtualenv, create your virtual environment ```virtualenv venv```

## Install Heroku Command Line Interface and Login
You have to have an account at Heroku for this step
Create your Heroku account and download the Heroku Command Line Interface (CLI)
Once installed, you can use the heroku command from your command shell.
Log in using the email address and password you used when creating your Heroku account with ```heroku login```

## Clone this app from github
You need git for this step
Clone this app from https://github.com/tomascarvalho/Budgeteer
``` git clone https://github.com/tomascarvalho/Budgeteer ```
Now you have the source code and the requirements.txt file that tells pip all the requirements needed to run this app.

## Create an app at Heroku
Create an app at Heroku with ```heroku create```

## Deploy this Application
Deploy this application with ```git push heroku master```
