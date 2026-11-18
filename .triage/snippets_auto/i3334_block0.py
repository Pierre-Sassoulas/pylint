from sqlalchemy import Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import PrimaryKeyConstraint

Base = declarative_base()


class Table(Base):
    __tablename__ = 'table'
    __table_args__ = (PrimaryKeyConstraint('column1'),)
    _column1 = Column('column1', Boolean)
    column2 = Column('column2', Boolean)

    @hybrid_property
    def column1(self):
        return self._column1

    @column1.setter
    def column1(self, column1):
        self._column1 = column1


Table.column1.op('*')
Table.column2.op('*')
