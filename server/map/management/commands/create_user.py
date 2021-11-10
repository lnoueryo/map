import uuid
import hashlib
from datetime import datetime as dt
import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy.orm import sessionmaker, scoped_session
from user.models import *
from django.conf import settings

def execute():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    password = password = hashlib.sha256(settings.SECRET_KEY.encode() + b'admin').hexdigest()
    user = User()
    user.name = 'admin'
    user.email = 'admin@jounetsism.biz'
    user.password = password
    session.add(user)
    session.commit()
class Command(BaseCommand):
    def handle(self, *args, **options):
        execute()