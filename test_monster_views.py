"""Monster view tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test__views.py


import os
from unittest import TestCase
from unittest import TestCase
from flask import Flask, session, g
from models import db, connect_db, User, Monster, Encounter


# BEFORE we import our app, set an environmental variable
# to use a different database for tests (do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///initiative-role-test"

# Now we can import app

from app import app, CURR_USER_KEY

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Turn off debugtoolbar intercept redirects
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class EncounterViewTestCase(TestCase):
    def setUp(self):
        db.create_all()
        self.client = app.test_client()
        self.user = User.signup('testuser', 'test@example.com', 'password', 'test.jpg')
        db.session.commit()
        
        self.login()
        
def tearDown(self):
        db.session.remove()
        db.drop_all()
    
def login(self):
    with self.client:
        self.client.post('/', data={'username': 'testuser', 'password': 'password'})
        
def test_stat_block_route(self):
        with self.client:
            response = self.client.get('/stats/monster_name')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/')
    
def test_stat_block_route_unauthorized(self):
    self.logout()
        
    with self.client:
        response = self.client.get('/stats/monster_name')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')
    
def test_add_monster_route(self):
    with self.client:
        response = self.client.post('/monster/add', json={'monsterName': 'Test Monster'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/')
        
        encounter_id = session.get('encounter_id')
        user_id = g.user.id

        monster = Monster.query.filter_by(monster_name='Test Monster',
                                          encounter_id=encounter_id,
                                          user_id=user_id).first()

        self.assertIsNotNone(monster)
        
def test_remove_monster_route(self):
    encounter = Encounter(name='Test Encounter', user=self.user)
    monster = Monster(monster_name='Test Monster', encounter=encounter, user=self.user)
    db.session.add_all([encounter, monster])
    db.session.commit()
        
    with self.client:
        response = self.client.post('/monster/remove', data={'encounter_id': encounter.id, 'monster_id': monster.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, f'http://localhost/encounter/{encounter.id}')
        
        monster = Monster.query.get(monster.id)
        
        self.assertIsNone(monster)
        
    def logout(self):
        with self.client:
            self.client.get('/logout')