from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer)
    phone: Mapped[String] = mapped_column(String(50), nullable=True, unique=True)
    username: Mapped[String] = mapped_column(String(50), nullable=True, unique=True)
    name: Mapped[String] = mapped_column(String(50), nullable=True)
    is_active: Mapped[Boolean] = mapped_column(Boolean, nullable=False)


    orders: Mapped[List["Orders"]] = relationship("Orders", back_populates="user")
    # invites: Mapped[List["ReferalLinks"]] = relationship("ReferalLinks", back_populates="user")
    admins: Mapped["Admins"] = relationship("Admins", back_populates="user")

    def __init__(self, phone: str | None, username: str, name: str, tg_id: int):
        self.telegram_id = tg_id
        self.phone = phone
        self.username = username
        self.name = name
        self.is_active = True

    def __repr__(self):
        return f"Пользователь с username = {self.username}"


class Admins(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, unique=True)

    user: Mapped["Users"] = relationship("Users", back_populates="admins")

    def __init__(self, user_id: int):
        self.user_id = user_id


class ReferalLinks(Base):
    __tablename__ = "ref_links"

    user_who_invite_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    invited_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, primary_key=True)

    def __init__(self, user_who_invite_id: int, invited_user: int):
        self.user_who_invite_id = user_who_invite_id
        self.invited_user = invited_user


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    people_count: Mapped[int] = mapped_column(Integer, nullable=False)
    tariff: Mapped[String] = mapped_column(String(50), nullable=False)
    order_time: Mapped[String] = mapped_column(String(6), nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="orders")

    def __init__(self, user_id: int, people_count: int, tariff: str, order_time = str):
        self.user_id = user_id
        self.people_count = people_count
        self.tariff = tariff
        self.order_time = order_time

    def __repr__(self):
        return f"Заказ сделал пользователь {self.user_id}"




