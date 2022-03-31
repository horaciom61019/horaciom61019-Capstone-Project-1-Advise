""" User model tests """

# run these tests like:
#
#    python3 -m unittest test_user_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Advice

os.environ['DATABASE_URL'] = "postgresql:///advice-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """ Test views for advice """

    def setUp(self):
        """ Create test client, add sample data """

        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "password")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "password")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    ##########################################################################
    # Signup Tests

    def test_valid_signup(self):
        u_test = User.signup("testtesttest", "password")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertNotEqual(u_test.password, "password")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "password")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "")
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", None)

    
    ##########################################################################
    # Authentication Tests

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

    ##########################################################################
    # Hash Test

    def test_vaid_hashpwd(self):
        pw_test = User.hash_pwd("password")

        self.assertTrue(pw_test.startswith("$2b$"))
    