import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)


def get_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
    else:
        session.commit()
    finally:
        session.close()
