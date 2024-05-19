from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import *

# Подключение к базе данных SQLite
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)  # Для SQLite важно добавить check_same_thread=False

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)  # Индексируем, если часто ищем по названию
    description = Column(String)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)  # Создание таблицы в базе данных

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Создание сессии для работы с базой данных
