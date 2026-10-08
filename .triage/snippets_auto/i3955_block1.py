from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declared_attr

from app import db

class Transaction(db.Model):
   
    @declared_attr
    def account_id(cls):
        return Column(Integer, ForeignKey("account.id", ondelete='CASCADE'))

    @classmethod
    def get_transaction_ids_for_account(cls, account_id):
        return {x[0] for x in cls.query.with_entities('transaction_id').filter(cls.account_id == account_id).all()}  # comparison-with-callable
