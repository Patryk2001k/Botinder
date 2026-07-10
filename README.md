# Botinder ![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![](https://img.shields.io/badge/Postgresql-07405E?style=for-the-badge&logo=postgresql&logoColor=white) ![](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) 

Botinder is a tongue-in-cheek web application whose main purpose is connecting humans with robots, inspired by popular dating platforms. The project has undergone a thorough code refactoring in accordance with Clean Code principles and has been fully containerized using Docker, merging the legacy web application and a dedicated API module into a single, cohesive environment (Monorepo).

## Concept and Project Goals

The project was created as a humorous simulation of a dating app for humans and machines. The main features of the system include:
- User registration, login, and profile management (including profile picture uploads).
- Browsing profiles, rating them, and matching humans with robots based on location.
- Two-way communication and the ability to instantly exchange chat messages with matched bots.

# frameworks and technologies:
- <a href="https://www.sqlalchemy.org/" alt="sqlalchemy">sqlalchemy</a> (to store information in database i am using Postgresql)
- <a href="https://flask.palletsprojects.com/en/2.3.x/" alt="flask">flask</a> (simple python web framework)
- flask_login (and everything with login_authentication)
- flask_uploads
- <a href="https://docs.python.org/3/library/os.html" alt="os">os</a> library to create folders for current users and store images
- Bcrypt to hash password
- of course i use basic stuff like HTML, CSS, JS and jinja2, <a href="https://getbootstrap.com/" alt="Boostrap">Boostrap</a> 
- <a href="https://alpinejs.dev/" alt="alpine.js">alpine.js</a> (i used this js framework to simple stuff with html, in shortcut this framework can do dynamic html in simple way and i think it is good for small projects)
  
### Main Application (Flask)
Handles the user interface, sessions, authentication, and the entire relational logic for matches and messages.
- Web framework: Flask (along with flask_login and flask_uploads extensions)
- Frontend: HTML, CSS, JavaScript, Bootstrap, Jinja2, and Alpine.js (used for efficient, dynamic HTML manipulation in smaller components)
- Database and ORM: SQLAlchemy, PostgreSQL with the PostGIS spatial extension
- Security: Bcrypt for hashing user passwords

---

## How to Run (Docker Compose)

Thanks to full containerization, launching the entire environment along with the database and accompanying services comes down to executing basic commands. There is no need for local installation of libraries from the requirements.txt file or manual database configuration.

### Prerequisites
- Installed and running Docker and Docker Desktop.

### Startup Process

**1. Database cleanup and initialization (Recommended on first launch)**
To remove old database volumes from previous runs and allow PostgreSQL and PostGIS to spin up fresh with automatic test data seeding, run the following in your terminal:

```bash
docker-compose down -v
```

**2. Building and starting containers**
To force a clean build of the application images and start the services in the background, use the command:

```bash
docker-compose up --build
```

**3. Automatic code reload mode (Live-Reload)**
The docker-compose.yml configuration uses volume mapping in the `.:/app` format. This means that any modification made to Python source files (.py) or view templates (.html) on your local machine is immediately reflected in the running container. There is no need to rebuild images during development.

---

## Login Credentials and Test Environment

After successfully starting the containers and waiting about 15-20 seconds for table initialization and automatic data seeding, the main application becomes available at:
http://localhost:5000

The database automatically generates 100 robot profiles and two ready-made user accounts for demonstration purposes:

### Warsaw Profile (Jan Kowalski)
- Login: user_warszawa (alternatively first name: Jan)
- Password: password123

### Krakow Profile (Anna Nowak)
- Login: user_krakow (alternatively first name: Anna)
- Password: password123

Both test accounts already have an assigned and generated list of 250 matched robot candidates located within a 10-kilometer radius of the selected city. All interactions, chat mechanisms, and matching work instantly.
