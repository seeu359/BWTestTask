import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

load_dotenv()

if os.getenv('CI') is None:
    DATABASE_URL = os.getenv('DATABASE_URL')
else:
    DATABASE_URL = 'sqlite:///' + str(settings.BASE_DIR) + '/db.sqlite'


engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)


def get_session():
    session = Session()
    try:
        yield session
    except: # noqa E722
        session.rollback()
    else:
        session.commit()
    finally:
        session.close()
