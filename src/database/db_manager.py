import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    full_name = Column(String, unique=True)
    alias = Column(String)  # Temporarily assigned name if unknown
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profiles = relationship("Profile", back_populates="person", cascade="all, delete-orphan")
    detections = relationship("Detection", back_populates="person")
    transcripts = relationship("Transcript", back_populates="person")

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    category = Column(String)  # Interests, Context, Personal Data, etc.
    content = Column(Text)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    person = relationship("Person", back_populates="profiles")

class Detection(Base):
    __tablename__ = 'detections'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float)
    image_path = Column(String)  # Path to saved face image
    
    person = relationship("Person", back_populates="detections")

class Transcript(Base):
    __tablename__ = 'transcripts'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    text = Column(Text)
    processed = Column(Integer, default=0) # 0: raw, 1: processed by AI
    
    person = relationship("Person", back_populates="transcripts")

class DBManager:
    def __init__(self, db_url=None):
        if not db_url:
            db_path = os.getenv("DB_PATH", "data/argos.db")
            # Ensure data directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            db_url = f"sqlite:///{db_path}"
            
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def get_or_create_person(self, full_name=None, alias=None):
        session = self.get_session()
        try:
            if full_name:
                person = session.query(Person).filter_by(full_name=full_name).first()
                if person:
                    return person
            
            if alias:
                person = session.query(Person).filter_by(alias=alias).first()
                if person:
                    return person
            
            # Create new
            new_person = Person(full_name=full_name, alias=alias)
            session.add(new_person)
            session.commit()
            # Refresh to get ID
            session.refresh(new_person)
            return new_person
        finally:
            session.close()

    def add_detection(self, person_id, confidence, image_path=None):
        session = self.get_session()
        try:
            detection = Detection(person_id=person_id, confidence=confidence, image_path=image_path)
            session.add(detection)
            session.commit()
        finally:
            session.close()

    def add_transcript(self, person_id, text):
        session = self.get_session()
        try:
            transcript = Transcript(person_id=person_id, text=text)
            session.add(transcript)
            session.commit()
        finally:
            session.close()

    def update_profile(self, person_id, category, content):
        session = self.get_session()
        try:
            profile = session.query(Profile).filter_by(person_id=person_id, category=category).first()
            if profile:
                profile.content = content
            else:
                profile = Profile(person_id=person_id, category=category, content=content)
                session.add(profile)
            session.commit()
        finally:
            session.close()
