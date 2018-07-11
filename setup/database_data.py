#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_scheme import Base, User, Topic, Question, Status

engine = create_engine('<database-url>')

Base. metadata. bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Delete table content
session.query(Status).delete()
session.query(Question).delete()
session.query(Topic).delete()
session.query(User).delete()

# User
user = User(name = "Pauline Trung", email="pauline.trung@gmail.com", is_admin=True, picture="https://lh5.googleusercontent.com/-glODJqBWIT0/AAAAAAAAAAI/AAAAAAAAAAA/AB6qoq0PuSJI3N-xZJ1QUHteDTKLEPcvKw/mo/photo.jpg")
session.add(user)
session.commit()

# Topic Englische Zahlen
k = Topic(name="English numbers (1-10)")
session.add(k)
session.commit()

f = Question(topic=k, question='eins', answer='one')
session.add(f)
session.commit()

f = Question(topic=k, question='zwei', answer='two')
session.add(f)
session.commit()

f = Question(topic=k, question='drei', answer='three')
session.add(f)
session.commit()

f = Question(topic=k, question='vier', answer='four')
session.add(f)
session.commit()

f = Question(topic=k, question='fuenf', answer='five')
session.add(f)
session.commit()

f = Question(topic=k, question='sechs', answer='six')
session.add(f)
session.commit()

f = Question(topic=k, question='sieben', answer='seven')
session.add(f)
session.commit()

f = Question(topic=k, question='acht', answer='eight')
session.add(f)
session.commit()

f = Question(topic=k, question='neun', answer='nein')
session.add(f)
session.commit()

f = Question(topic=k, question='zehn', answer='ten')
session.add(f)
session.commit()

# Topic Italinische Zahlen
k = Topic(name="Numeri italiani (1-10)")
session.add(k)
session.commit()

f = Question(topic=k, question='eins', answer='uno')
session.add(f)
session.commit()

f = Question(topic=k, question='zwei', answer='due')
session.add(f)
session.commit()

f = Question(topic=k, question='drei', answer='tre')
session.add(f)
session.commit()

f = Question(topic=k, question='vier', answer='quattro')
session.add(f)
session.commit()

f = Question(topic=k, question='fuenf', answer='cinque')
session.add(f)
session.commit()

f = Question(topic=k, question='sechs', answer='sei')
session.add(f)
session.commit()

f = Question(topic=k, question='sieben', answer='sette')
session.add(f)
session.commit()

f = Question(topic=k, question='acht', answer='otto')
session.add(f)
session.commit()

f = Question(topic=k, question='neun', answer='nove')
session.add(f)
session.commit()

f = Question(topic=k, question='zehn', answer='dieci')
session.add(f)
session.commit()


print "added items!"
