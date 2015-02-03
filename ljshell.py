from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

config_uri = 'development.ini'
setup_logging(config_uri)
settings = get_appsettings(config_uri)
engine = engine_from_config(settings, 'sqlalchemy.')
Session = sessionmaker(bind=engine)
session = Session()

from learning_journal.models import Entry
print session.query(Entry).all()

query = session.query(Entry)
print '\n*** break ***\n'
print type(query)
print query.count()