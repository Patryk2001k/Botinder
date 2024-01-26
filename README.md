# Botinder ![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![](https://img.shields.io/badge/Postgresql-07405E?style=for-the-badge&logo=postgresql&logoColor=white) ![](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) 
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
4. Start huey with this command `huey_consumer.py app.huey`
5. Before running the app make sure that Botinder API is enabled, you can host it on your local machine and you can find it [here](https://github.com/Patryk2001k/Botinder-API/tree/main)
6. Run the app using `python run.py`.
7. Open your browser and go to `http://localhost:5000`.

## Live Demo

A live demo of Botinder can be found [here](https://botinder.onrender.com/home).

## How to Register

To register, simply fill in the blank fields. However, there are two important points to keep in mind:

- **Domicile Setting**: Your domicile must be set to "Kraków". Alternatively, if you are in Cracow, you need to grant the site permission to use your location. This is necessary because if the site detects that you are in a location with no available robot matches, like Berlin, it will start generating robots. This can be a time-consuming process, especially since the app is hosted on a slower, free server.

- **Account Information**: Ensure that your chosen username and login fields are different from each other.

## Example Account

If you don't want to register and would like to try the app, here is a test account:
- **Login:** Example
- **Password:** 444

## Site is slow and something cant load?
Please be aware that my site is hosted on a **free hosting service** on [render](https://render.com/), and as such, **resources are limited**. I ask for your **patience** if the site responds more slowly than expected. If you encounter an issue where content, such as potential new matches, does not load promptly after a short wait, a page refresh may resolve the issue.


