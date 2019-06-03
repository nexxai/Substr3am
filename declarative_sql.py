####################
#   Substr3am v1.0
#
#   @nexxai
#   github.com/nexxai/Substr3am
####################


from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String

Base = declarative_base()

class Subdomain(Base):
    __tablename__ = 'subdomains'
    id = Column(Integer, primary_key=True)
    subdomain = Column(String(250), nullable=False)
    count = Column(Integer)

subdomains_db = 'sqlite:///subdomains.db'
engine = create_engine(subdomains_db)

Base.metadata.create_all(engine)
