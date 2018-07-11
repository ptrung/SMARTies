from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(80), nullable=False)
    is_admin = Column(Boolean, default=False)
    access = Column(Boolean, default=False)
    picture = Column(String(160))

class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship(Topic)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship(Question)
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship(Topic)
    box = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Correction(Base):
    __tablename__ = 'correction'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship(Question)
    new_question = Column(String)
    new_answer = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


engine = create_engine('<database-url>')

Base.metadata.create_all(engine)
