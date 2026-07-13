from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
<<<<<<< HEAD
    autocommit = False,
    autoflush = False,
    bind = engine
=======
    autocommit=False,
    autoflush=False,
    bind=engine
>>>>>>> develop
)