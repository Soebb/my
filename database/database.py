from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

import threading
import asyncio

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, UniqueConstraint, func


from config import Config


def start() -> scoped_session:
    engine = create_engine(Config.DB_URL, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class custom_mode(BASE):
    __tablename__ = "mode"
    id = Column(Integer, primary_key=True)
    mode = Column(String)

    def __init__(self, id, mode):
        self.id = id
        self.mode = mode

custom_mode.__table__.create(checkfirst=True)


async def update_mode(id, mode):
    with INSERTION_LOCK:
        mod = SESSION.query(custom_mode).get(id)
        if not mod:
            mod = custom_caption(id, mode)
            SESSION.add(mod)
            SESSION.flush()
        else:
            SESSION.delete(mod)
            mod = custom_mode(id, mode)
            SESSION.add(mod)
        SESSION.commit()

async def del_mode(id):
    with INSERTION_LOCK:
        msg = SESSION.query(custom_mode).get(id)
        SESSION.delete(msg)
        SESSION.commit()

async def get_mode(id):
    try:
        mode = SESSION.query(custom_mode).get(id)
        return mode
    finally:
        SESSION.close()

