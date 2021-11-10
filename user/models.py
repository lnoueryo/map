from sqlalchemy.orm import relationship
from sqlalchemy import (Table, Column, Integer, String, ForeignKey, DateTime, text, Float, and_)
from sqlalchemy.dialects.mysql.base import BIGINT, LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from datetime import timedelta

from django.conf import settings
engine = settings.ENGINE

Base = declarative_base()

class User(Base):
    """
    Userテーブルクラス
    """

    # テーブル名
    __tablename__ = 'users'

    # 個々のカラムを定義
    id = Column(BIGINT, primary_key=True)
    name = Column(String(20))
    email = Column(String(40))
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    password  = Column(String(255))