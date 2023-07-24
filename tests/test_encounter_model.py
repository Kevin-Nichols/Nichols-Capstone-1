"""Encounter model tests."""

# run these tests like:
#
#    python -m unittest test_encounter_model.py


import os
from unittest import TestCase

from models import db, User, Monster, Encounter
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///initiative-role-test"


# Now we can import app

from app import app

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


USER_DATA = {
    "email":"test@test.com",
    "username":"testuser",
    "password":"HASHED_PASSWORD"
}

ENCOUNTER_DATA = {
    "name":"test-encounter",
    "monster_id":1,
    "user_id":1
}

MONSTER_DATA = {
    "encounter_id":1,
    "user_id":1,
    "monster_name":"dire-wolf"
}


class EncounterModelTestCase(TestCase):
    """Test for encounter model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Monster.query.delete()
        Encounter.query.delete()

        self.client = app.test_client()
        
        u = User(**USER_DATA)
        e = Encounter(**ENCOUNTER_DATA)
        m = Monster(**MONSTER_DATA)
        
        db.session.add(u)
        db.session.add(e)
        db.session.add(m)
        db.session.commit()
        
        self.user = u
        self.encounter = e
        self.monster = m

    def tearDown(self):
        """ Clean up fouled transactions """

        db.session.rollback()
        
    def test_encounter_model(self):
        """Does basic model work?"""
        
        self.assertEqual(
            str(self.encounter), 
            f"<Encounter #{self.encounter.id}: test-encounter, 1, 1")