from flask import Flask
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"

    ssn = Column("ssn", Integer, primary_key = True)
    firstname = Column("firstname", String)
    lastname = Column("lastname", String)
    gender = Column("gender", CHAR)
    age = Column("age", Integer)

    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"{self.ssn}\t {self.firstname}\t {self.lastname}\t {self.gender}\t {self.age}"


class Fortune(Base):
    __tablename__ = "fortune"

    id = Column("id", Integer, primary_key = True)
    description = Column("description", String)
    owner = Column("owner", Integer, ForeignKey("people.ssn"))

    def __init__(self, id, descrition, owner):
        self.id = id
        self.description = descrition
        self.owner = owner

    def __repr__(self):
        return f"{self.id}\t {self.description} owned by {self.owner}"


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

p1 = Person(1435, "Timothy", "Moscaliuc", "m", 21)
p2 = Person(1654, "Alex", "Smecher", 'm', 20)
p3 = Person(2154, "Ana", "Popescu", "f", 25)
session.add(p1)
session.add(p2)
session.add(p3)
session.commit()

f1 = Fortune(1, "car", p1.ssn)
f2 = Fortune(2, "phone", p3.ssn)
f3 = Fortune(3, "laptop", p2.ssn)
f4 = Fortune(4, "bike", p1.ssn)
session.add(f1)
session.add(f2)
session.add(f3)
session.add(f4)
session.commit()

results = session.query(Fortune, Person).filter(Fortune.owner == Person.ssn).filter(Person.firstname == "Timothy").all()
for person in results:
    print(person)
