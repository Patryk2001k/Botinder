# Botinder ![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![](https://img.shields.io/badge/Postgresql-07405E?style=for-the-badge&logo=postgresql&logoColor=white) ![](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) 
Botinder to aplikacja internetowa stworzona z przymrużeniem oka, której głównym zadaniem jest łączenie ludzi z robotami w sposób inspirowany popularnymi platformami randkowymi. Projekt przeszedł gruntowną refaktoryzację kodu zgodnie z zasadami Clean Code i został w pełni skonteneryzowany za pomocą Dockera, łącząc dawną aplikację webową oraz dedykowany moduł API w jedno spójne środowisko (Monorepo).

## Koncepcja i cele projektu

Projekt powstał jako humorystyczna symulacja aplikacji randkowej dla ludzi i maszyn. Do głównych założeń systemu należą:
- Możliwość rejestracji, logowania oraz zarządzania profilem użytkownika (w tym przesyłanie zdjęcia profilowego).
- Przeglądanie profili, ocenianie ich i dopasowywanie ludzi z robotami na podstawie lokalizacji.
- Dwukierunkowa komunikacja i możliwość natychmiastowej wymiany wiadomości czatowych z dopasowanymi botami.

# frameworks and technologies:
- <a href="https://www.sqlalchemy.org/" alt="sqlalchemy">sqlalchemy</a> (to store information in database i am using Postgresql)
- <a href="https://flask.palletsprojects.com/en/2.3.x/" alt="flask">flask</a> (simple python web framework)
- flask_login (and everything with login_authentication)
- flask_uploads
- <a href="https://docs.python.org/3/library/os.html" alt="os">os</a> library to create folders for current users and store images
- Bcrypt to hash password
- of course i use basic stuff like HTML, CSS, JS and jinja2, <a href="https://getbootstrap.com/" alt="Boostrap">Boostrap</a> 
- <a href="https://alpinejs.dev/" alt="alpine.js">alpine.js</a> (i used this js framework to simple stuff with html, in shortcut this framework can do dynamic html in simple way and i think it is good for small projects)
  
### 1. Aplikacja Główna (Flask)
Obsługuje interfejs użytkownika, sesje, uwierzytelnianie oraz całą logikę relacyjną dopasowań i wiadomości.
- Framework webowy: Flask (wraz z rozszerzeniami flask_login oraz flask_uploads)
- Frontend: HTML, CSS, JavaScript, Bootstrap, Jinja2 oraz Alpine.js (użyty do sprawnej, dynamicznej manipulacji warstwą HTML w mniejszych komponentach)
- Baza danych i ORM: SQLAlchemy, PostgreSQL z rozszerzeniem przestrzennym PostGIS
- Bezpieczeństwo: Bcrypt do hashowania haseł użytkowników

### 2. Moduł Botinder API (FastAPI)
Wewnętrzna, bezstanowa usługa pomocnicza, która została scalona z głównym projektem i ukryta w prywatnej strukturze. Odpowiada za operacje matematyczno-geograficzne.
- Framework: FastAPI
- Główne funkcjonalności: Geokodowanie (konwersja nazw miast na współrzędne geograficzne szerokości i długości) oraz precyzyjne obliczanie dystansu między użytkownikiem a robotem.
- Bezpieczeństwo: Biblioteka Jose (obsługa tokenów JWT) oraz Bcrypt.

---

## Instrukcja uruchomienia (Docker Compose)

Dzięki pełnej konteneryzacji uruchomienie całego środowiska wraz z bazą danych i usługami towarzyszącymi sprowadza się do wykonania podstawowych poleceń. Nie jest wymagana lokalna instalacja bibliotek z pliku requirements.txt ani ręczna konfiguracja bazy danych.

### Wymagania wstępne
- Zainstalowane i uruchomione oprogramowanie Docker oraz Docker Desktop.

### Proces uruchomienia

**1. Czyszczenie i inicjalizacja bazy danych (Zalecane przy pierwszym starcie)**
Aby usunąć stare wolumeny baz danych z poprzednich uruchomień i pozwolić, aby PostgreSQL oraz PostGIS postawiły się na nowo z automatycznym zasileniem danymi testowymi, wykonaj w terminalu:

```bash
docker-compose down -v
```

**2. Budowanie i uruchomienie kontenerów**
Aby wymusić czyste zbudowanie obrazów aplikacji i uruchomić usługi w tle, użyj komendy:

```bash
docker-compose up --build
```

**3. Tryb automatycznego odświeżania kodu (Live-Reload)**
W konfiguracji pliku docker-compose.yml zastosowano mapowanie wolumenów w formacie .:/app. Oznacza to, że każda modyfikacja wprowadzona w plikach źródłowych Pythona (.py) lub szablonach widoku (.html) na komputerze lokalnym jest natychmiast przenoszona do działającego kontenera. Nie ma potrzeby ponownego budowania obrazów podczas prac programistycznych.

---

## Dane logowania i środowisko testowe

Po poprawnym uruchomieniu kontenerów i odczekaniu około 15-20 sekund na inicjalizację tabel oraz automatyczne zasianie danych (seeding), aplikacja główna staje się dostępna pod adresem:
http://localhost:5000

W bazie danych automatycznie generowanych jest 100 profili robotów oraz dwa gotowe konta użytkowników do celów demonstracyjnych:

### Profil Warszawa (Jan Kowalski)
- Login: user_warszawa (alternatywnie imię: Jan)
- Hasło: password123

### Profil Kraków (Anna Nowak)
- Login: user_krakow (alternatywnie imię: Anna)
- Hasło: password123

Oba konta testowe posiadają już przypisaną i wygenerowaną listę 250 dopasowanych kandydatów-robotów, którzy znajdują się w promieniu do 10 kilometrów od wskazanego miasta. Wszystkie interakcje, mechanizmy czatu oraz dopasowania działają natychmiastowo.
