"""Encounter view tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test__views.py


import os
from unittest import TestCase
from flask import Flask, session
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
        
def test_create_encounter_route(self):
        response = self.client.get('/encounter/new')
        self.assertEqual(response.status_code, 200)
        
def test_create_encounter_success(self):
    response = self.client.post('/encounter/new', data={'name': 'Test Encounter'})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.location, 'http://localhost/encounter/1')
        
    encounter = Encounter.query.get(1)
    self.assertEqual(encounter.name, 'Test Encounter')
    self.assertEqual(encounter.user_id, self.user.id)
    
def test_show_encounter_route(self):
    encounter = Encounter(name='Test Encounter', user=self.user)
    db.session.add(encounter)
    db.session.commit()
        
    response = self.client.get(f'/encounter/{encounter.id}')
    self.assertEqual(response.status_code, 200)
        
def test_show_encounter_unauthorized(self):
    self.logout()
        
    response = self.client.get('/encounter/1')
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.location, 'http://localhost/')
        
def test_show_encounter_invalid_id(self):
    response = self.client.get('/encounter/999')
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.location, 'http://localhost/encounter/new')
        
def test_show_all_encounters_route(self):
    response = self.client.get('/encounter/all')
    self.assertEqual(response.status_code, 200)
        
def test_show_all_encounters_unauthorized(self):
    self.logout()
        
    response = self.client.get('/encounter/all')
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.location, 'http://localhost/')
        
def test_remove_encounter_route(self):
    encounter = Encounter(name='Test Encounter', user=self.user)
    db.session.add(encounter)
    db.session.commit()
        
    response = self.client.post('/encounter/remove', data={'encounter_id': encounter.id})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.location, 'http://localhost/encounter/all')
        
    self.assertIsNone(Encounter.query.get(encounter.id))
        
def test_remove_encounter_unauthorized(self):
    self.logout()
        
    response = self.client.post('/encounter/remove', data={'encounter_id': 1})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.location, 'http://localhost/')
        
def logout(self):
    with self.client:
        self.client.get('/logout')