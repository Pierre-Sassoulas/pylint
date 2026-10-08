from sqlalchemy import Column, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)

    @hybrid_property
    def name_lower(self):
        return self.name.lower()

    @name_lower.expression
    def name_lower(cls, value):     # this line has the issue
        return func.lower(cls.name)
