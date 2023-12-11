# Botinder ![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![](https://img.shields.io/badge/Postgresql-07405E?style=for-the-badge&logo=postgresql&logoColor=white) ![](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![]([https://img.shields.io/badge/Postgresql-F7DF1E?style=for-the-badge&logo=postgresql&logoColor=white])
Botinder is simple app where you can join people with robots.

# Goal of this project :books::
This is my project to cv. Goal of this project is to create simple app where user can log in, send his profile picture and match with robots. 


# App must be:
- funny and simmilar to tinder (thats why name Botinder :) )
- connect people with robots (like match on tinder)
- people and robots can send messages with each other

# frameworks and technologies:
- <a href="https://www.sqlalchemy.org/" alt="sqlalchemy">sqlalchemy</a> (to store information in database i am using Postgresql)
- <a href="https://flask.palletsprojects.com/en/2.3.x/" alt="flask">flask</a> (simple python web framework)
- flask_login (and everything with login_authentication)
- flask_uploads
- <a href="https://docs.python.org/3/library/os.html" alt="os">os</a> library to create folders for current users and store images
- Bcrypt to hash password
- of course i use basic stuff like HTML, CSS, JS and jinja2, <a href="https://getbootstrap.com/" alt="Boostrap">Boostrap</a> 
- <a href="https://alpinejs.dev/" alt="alpine.js">alpine.js</a> (i used this js framework to simple stuff with html, in shortcut this framework can do dynamic html in simple way and i think it is good for small projects)

## How to start on your local machine:
To use this app, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up your PostgreSQL database and configure the connection in `__init__.py` in models module.
4. Run the app using `python run.py`.
5. Open your browser and go to `http://localhost:5000`.

## Live Demo:
A live demo of Botinder can be found at https://botinder.onrender.com/home

How to register:

Just fill the blank parts but there are two important things.
a) Domicile must be set for "Kraków" or if you are in Cracow you just need to accept that site will use your location. Answer why is that needed because if site will detect that you are in Berlin and there is no robots to match with then it will generate robots 
and the problem in that is can take some time. Since i hosted in on free machine it is very slow.
b) Username and login blanks must be diffrent from themselves

Example account:
If you dont want to register and want to just try the app this is test account:
Login: Example
Password: 444


