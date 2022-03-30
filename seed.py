from app import app
from models import  db, User, Advice, Follows, Likes

db.drop_all()
db.create_all()

# user1 = User(username='Test01', password='password')

# db.session.add(user1)
# db.session.commit()