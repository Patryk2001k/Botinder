
# Botinder API ![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/Postgresql-07405E?style=for-the-badge&logo=postgresql&logoColor=white) ![](https://img.shields.io/badge/Fastapi-07405E?style=for-the-badge&logo=fastapi&logoColor=white)
This API was built in FastAPI framework and was created for Botinder app

Github: https://github.com/Patryk2001k/Botinder

This API was created specially for calculate distance and to generate latitude and longitude from city name.

# frameworks and technologies:
- <a href="https://www.sqlalchemy.org/" alt="sqlalchemy">sqlalchemy</a> (to store information in database i am using Postgresql)
- fastapi
- jose library (jwt)
- Bcrypt to hash password


## Deployment on your local machine

To use this app, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up your PostgreSQL database and configure the connection in `__init__.py` in models module.
4. Run the app using `uvicorn app.main:app`.
5. Open your browser and go to `http://localhost:5000`.
