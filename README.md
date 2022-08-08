# Capstone

This is my final project on the course CS50 Web Development using Python & Javascript, created entirely from scratch.
This project will still require some minor improvements and more feature addition soon :D

## Distinctiveness and Complexity

This project is mainly a live quiz website where creators can create a game with multiple questions, then challenge multiple people by entering a code to enter a game session and compete with other people live. For now, the question is only of a multiple choice (4 options) type, where the administrator has control to start a game session, close a question or move on to the next question. The players will then be able to answer the question before it is closed. Most of the interaction here happens asynchronously with JavaScript and backend API routes, so the user does not have to refresh the page every time.

The backend (using Django) is complex and distinct enough from the other projects, as there are 7 various models with different relations, fields, meta tags, and methods built into it, along with a custom admin page and backend testing. The views.py also involve multiple routes with multiple error checking scenarios and 3 different API routes that each supports multiple request method. The frontend interactivity that uses JavaScript is complex enough as there is a lot of logic to be handled, the creation of multiple elements, and a lot of periodic API calls to the server. The styling itself uses CSS and Bootstrap, including a responsive sidebar & content page, CSS animation, jQuery, and many more.

## What's contained in each file

First, '.github' folder contains CI testing using Github Action. This capstone project currently contains 3 different app, namely livequiz, news, and sso.

Playquiz is the main app of this project, where all the questions, games, gamesessions, user answers, user sessions are stored, and rendering the other main views and API routes required for the livegame. In models.py, you can see all the 5 different models defined here using various models features from Django (differ from the previous projects), and admin.py are where all those models are registered. There are 2 extra files here, namely util.py to create helper function (used in views.py) of dynamic pagination feature and displaying question count, and forms.py to define all the forms that will be passed on to the frontend (from views.py). The views.py file contain 7 different routes and 3 API routes for various request methods. All the javascript interactivity and css are defined in the static folder.

News app is preety simple and only contain a place to view news written in markdown, similar to project 2, but currently is stored in a real backend database.

SSO app contains everything relating to templates (navbar, root layout), and views & models & templates regarding logging the user in or out. Here you can see the model 'User' and extra logic regarding to logging the user in or out (for example, in views.py there is extra checking to ensure password entered is not too simple, when there is error do not reset the whole form, etc), along with all html, css, and images files regarding to sso templates (login, logout, register). The sidebar (or top navbar, if open in small screen) is also defined here, including various links and logic of the navbar.

## How to run your application

Assuming python and pip installed, please run the following:

```python
pip install -r requirements.txt
```

```python
python manage.py makemigrations
```

```python
python manage.py migrate
```

```python
python manage.py runserver
```
