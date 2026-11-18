from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import String, Integer


class RoleReaction(Base):
    __tablename__ = 'user_roles_reactions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String)
    reaction_name: Mapped[str] = mapped_column(String)
    group_id: Mapped[int] = mapped_column(ForeignKey('user_roles_groups.id'))
    group: Mapped[RoleGroup] = relationship(RoleGroup)
