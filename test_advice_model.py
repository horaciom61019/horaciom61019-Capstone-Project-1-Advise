""" Advice model tests """

# run these tests like:
#
#    python3 -m unittest test_advice_model.py


import imp
import os
from pickle import ADDITEMS
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Advice, Likes

os.environ['DATABASE_URL'] = "postgresql:///advice-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """ Test views for advice """

    def setUp(self):
        """ Create test client, add sample data """

        db.drop_all()
        db.create_all()

        self.user_id = 43678
        u = User.signup("usertesting", "password")
        u.id = self.user_id
        db.session.commit()

        self.u = User.query.get(self.user_id)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_advice_model(self):
        """ Model work """

        advice = Advice(
            text = "test advice",
            user_id = self.user_id
        )

        db.session.add(advice)
        db.session.commit()

        # User should only have 1 message 
        self.assertEqual(len(self.u.advice), 1)
        self.assertEqual(self.u.advice[0].text, "test advice")

    def test_advice_likes(self):
        """ Test likes """

        advice = Advice(
            text = "test advice one",
            user_id = self.user_id
        )

        advice2 = Advice(
            text = "test advice two",
            user_id = self.user_id
        )
        
        user = User.signup("testUser34349", "password")
        user_id = 34349
        user.id = user_id

        db.session.add_all([advice, advice2, user])
        db.session.commit()

        user.likes.append(advice)
        db.session.commit()

        like = Likes.query.filter(Likes.user_id == user_id).all()
        
        self.assertEqual(len(like), 1)
        self.assertEqual(like[0].advice_id, advice.id)
