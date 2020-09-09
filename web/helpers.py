from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import models
from datetime import datetime
import pytz


db = SQLAlchemy()

def init_app(app):
  db.app = app
  db.init_app(app)
  return db


@contextmanager
def session_scope():
  """Provide a transactional scope around a series of operations."""
  s = get_session()
  s.expire_on_commit = False
  try:
    yield s
    s.commit()
  except:
    s.rollback()
    raise
  finally:
    s.close()

def get_session():
  return sessionmaker(bind=db.engine)()

def dt_now(timezone='America/Sao_Paulo'):
  dt = datetime.now(pytz.timezone(timezone))
  return dt

def check_exists_image(filename):
  with session_scope() as s:
    exists = s.query(db.exists().where(models.Image.filename == filename)).scalar()
  return exists

def insert_image(filename):
  with session_scope() as s:
    img = None
    if not check_exists_image(filename):
      img = models.Image(filename=filename, created_at=dt_now(), updated_at=dt_now())
      s.add(img)
      s.commit()
    return img

def insert_boundingbox(img, class_name, top, left, width, height):
  with session_scope() as s:
    values = {
      'image': img,
      'class_name': class_name,
      'top': top,
      'left': left,
      'width': width,
      'height': height,
      'updated_at': dt_now(),
      'created_at': dt_now()
    }
    bb = models.Boundingbox(**values)
    s.add(bb)
    s.commit()
    return bb

def remove_boundingboxes_from_image(img):
  with session_scope() as s:
    bb = s.query(models.Boundingbox).filter(models.Boundingbox.image == img)
    bb.delete()
    s.commit()

def remove_and_insert_boundingboxes(image_id, boundingboxes):
  with session_scope() as s:
    img = s.query(models.Image).filter(models.Image.id == image_id).first()
    img.updated_at = dt_now()
    bb = s.query(models.Boundingbox).filter(models.Boundingbox.image == img)
    bb.delete()
    for e in boundingboxes:
      values = {
        'image': img,
        'class_name': e['class_name'],
        'top': e['top'],
        'left': e['left'],
        'width': e['width'],
        'height': e['height'],
        'updated_at': dt_now(),
        'created_at': dt_now()
      }
      bb = models.Boundingbox(**values)
      s.add(bb)

    try:
      s.commit()
      return True
    except exc.SQLAlchemyError:
      return False

def get_image(filename):
  with session_scope() as s:
    return s.query(models.Image).filter(models.Image.filename == filename).first()

def get_next_image_and_boundingboxes(image_id=-1, direction='forward'):
  with session_scope() as s:
    img = None
    bblist = []
    if direction == 'forward':
      img = s.query(models.Image).\
        filter(
          models.Image.created_at == models.Image.updated_at,
          models.Image.removed_at == None,
          models.Image.id > image_id
        ).\
        order_by(models.Image.updated_at.asc(), models.Image.id.asc()).first()
      bblist = s.query(models.Boundingbox).filter(models.Boundingbox.image == img).all()
    elif direction == 'back':
      img = s.query(models.Image).\
        filter(
          models.Image.removed_at == None,
          models.Image.id < image_id
        ).\
        order_by(models.Image.updated_at.desc(), models.Image.id.desc()).first()
      bblist = s.query(models.Boundingbox).filter(models.Boundingbox.image == img).all()
    return img, bblist
