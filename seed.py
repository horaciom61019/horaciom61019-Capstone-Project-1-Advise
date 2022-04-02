from app import app
from models import  db, User, Advice, Likes

db.drop_all()
db.create_all()
