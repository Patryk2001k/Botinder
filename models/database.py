from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    ForeignKey,
    exists,
    Enum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_login import UserMixin, LoginManager

Base = declarative_base()

from app import app
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    return session.query(User).get(int(user_id))

class User(Base, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    lastname = Column(String(40), nullable=False)
    email = Column(String(120), nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)
    messages = relationship('Messages', backref='author', lazy=True)
    profile = relationship("Profile", uselist=False, back_populates="user")
    user_criteria = relationship("UserCriteria", uselist=False, back_populates="user")

    def __repr__(self):
        return f"User('{self.name}', '{self.lastname}','{self.email}', '{self.password}', '{self.image_file}')"

class Messages(Base, UserMixin):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    email = Column(String(120), unique=True, nullable=False )
    message = Column(String(400), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Messages('{self.name}', {self.email}, '{self.message}')"

class Profile(Base, UserMixin):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("male", "female", "custom"), nullable=False)
    profile_description = Column(String(500), nullable=False)
    domicile = Column(String(80), nullable=False)
    education = Column(String(120), nullable=False)
    employment_status = Column(Enum("hired", "unemployed", "student"), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"Profile('{self.user}', '{self.age}', '{self.gender}', '{self.profile_description}', '{self.domicile}', '{self.education}', '{self.employment_status}')"

class UserCriteria(Base, UserMixin):
    __tablename__ = "user_criteria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_of_robot = Column(Enum("humanoid", "non-humanoid", "all"), nullable=False)
    distance = Column(Integer, nullable=False)
    employment_status = Column(Enum("working robot", "disabled", "all"), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="user_criteria")

    def __repr__(self):
        return f"Profile('{self.user}', '{self.type_of_robot}', '{self.distance}', '{self.employment_status}')"

#Poniższe bazy danych dotyczą robotów (NPC) na stronie

class UserRobot(Base, UserMixin):
    __tablename__ = "user_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    image_file = Column(String(40), nullable=False, default='default.jpg')
    messages = relationship('RobotMessages', backref='author', lazy=True)
    profile_robot = relationship("RobotProfile", uselist=False, back_populates="user_robot")

    def __repr__(self):
        return f"UserRobot('{self.name}', '{self.image_file}')"

class RobotMessages(Base, UserMixin):
    __tablename__ = "messages_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    message = Column(String(400), nullable=False)
    user_id = Column(Integer, ForeignKey('user_robot.id'), nullable=False)

    def __repr__(self):
        return f"RobotMessages('{self.message}')"

class RobotProfile(Base, UserMixin):
    __tablename__ = "profile_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_of_robot = Column(Enum("humanoid", "non-humanoid", "all"), nullable=False)
    name = Column(String(20), nullable=False)
    profile_description = Column(String(500), nullable=False)
    domicile = Column(String(80), nullable=False)
    procesor_unit = Column(String(120), nullable=False)
    employment_status = Column(Enum("working robot", "disabled", "all"), nullable=False)

    user_id = Column(Integer, ForeignKey("user_robot.id"), unique=True)
    user_robot = relationship("UserRobot", back_populates="profile_robot")

    def __repr__(self):
        return f"RobotProfile('{self.user_robot}', '{self.type_of_robot}', '{self.name}', '{self.profile_description}', '{self.domicile}', '{self.procesor_unit}', '{self.employment_status}')"


engine = create_engine("sqlite:///Botinder.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()

#Poniżej niepatrzeć bo to są komentarze przechowujące funkcje sqlalchemy itd.

    #user = session.query(User).filter_by(username='butelka').first()
    #profile = Profile(age=30, user=user)
    #session.add(profile)
    #session.commit()

#    all_messages = session.query(Messages).all()
#    all_users = session.query(User).all()
#    users = session.query(User).with_entities(User.id, User.username).all()
#    user_messages = session.query(Messages).join(User).filter(User.username == 'mdamowiec').all()
#    all_profiles = session.query(Profile).all()
#    profile = session.query(Profile).filter_by(age=30).first()

 #   username = "butelka1"  # zmienna z nazwą użytkownika, dla k#tórego chcemy wyświetlić dane z tabeli Profile

    # Wyszukaj użytkownika o podanym nicku w tabeli User
  #  user = session.query(User).filter_by(username=username).first()

   # if user:
        # Jeśli znaleziono użytkownika, wyświetl dane z tabeli Profile związane z tym użytkownikiem
    #    profile = session.query(Profile).filter_by(user_id=user.id).first()
     #   if profile:
            #print(f"Wiek użytkownika {username}: {profile.age}")
      #  else:
       #     print(f"Brak danych profilowych dla użytkownika {username}")
    #else:
     #   print(f"Nie znaleziono użytkownika o nazwie {username}")

    #print(profile)
    #print("------")
    #print(all_messages)
    #print("------")
    #print(all_users)
    #print("------")
    #print(users)
    #rint("------")
    #print(user_messages)
    #print("-------")
    #print(all_profiles)

#user1 = User(username='Jan Kowalski', email='jan.kowalski@example.com', password='password123')
#session.add(user1)
#session.commit()

# Dodanie wpisów
#post1 = Post(title='Pierwszy wpis', content='To jest treść pierwszego wpisu', author=user1)
#post2 = Post(title='Drugi wpis', content='To jest treść drugiego wpisu', author=user1)
#session.add(post1)
#session.add(post2)
#session.commit()

# Pobranie wpisów użytkownika
#user_posts = session.query(User).all() #dodatkowa metoda to filter_by(username='Corey') albo coś takiego i w środku to przykład
#for post in user_posts: #Wyświetlenie ich w konsolce
#    print(post)
#    print(post.username)
#    #print(post.content)
#    print('---')

#    new_user = User(username='mdamowiec', email='madamowiec@example.com', password='password')
 ##   session.add(new_user)
   # session.commit()

    #message = "Siema co tam jak tam"
    #new_message = Messages(username=new_user.username, email=new_user.email, message=message, author=new_user)
    #session.add(new_message)
    #session.commit()
    