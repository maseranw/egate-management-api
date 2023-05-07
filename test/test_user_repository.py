import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import User
from repositories.user_repository import UserRepository


class TestUserRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create an in-memory database for testing
        engine = create_engine('sqlite:///:memory:', echo=False)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

        # Create the user table in the in-memory database
        User.metadata.create_all(bind=engine)

        # Create a user for testing
        cls.user = User(username='testuser', email='testuser@example.com', password='password')
        cls.session.add(cls.user)
        cls.session.commit()

        # Create a user repository for testing
        cls.user_repository = UserRepository(cls.session)

    def test_create_user(self):
        # Create a new user
        new_user = User(username='newuser', email='newuser@example.com', password='password')
        self.user_repository.create_user(new_user)

        # Verify that the user was created
        db_user = self.user_repository.get_user_by_username('newuser')
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, new_user.username)
        self.assertEqual(db_user.email, new_user.email)
        self.assertNotEqual(db_user.password, new_user.password)

    def test_get_user_by_username(self):
        # Get an existing user by username
        db_user = self.user_repository.get_user_by_username('testuser')

        # Verify that the user was found
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, self.user.username)
        self.assertEqual(db_user.email, self.user.email)
        self.assertEqual(db_user.password, self.user.password)

    def test_get_user(self):
        # Get an existing user by ID
        db_user = self.user_repository.get_user(self.user.id)

        # Verify that the user was found
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, self.user.username)
        self.assertEqual(db_user.email, self.user.email)
        self.assertEqual(db_user.password, self.user.password)

    def test_get_users(self):
        # Get a list of users
        users = self.user_repository.get_users()

        # Verify that the list is not empty and contains the expected user
        self.assertGreater(len(users), 0)
        self.assertIn(self.user, users)

    def test_update_user(self):
        # Update an existing user's username and email
        updated_user = User(username='updateduser', email='updateduser@example.com', password='password')
        db_user = self.user_repository.update_user(self.user.id, updated_user)

        # Verify that the user was updated
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, updated_user.username)
        self.assertEqual(db_user.email, updated_user.email)
        self.assertEqual(db_user.password, self.user.password)

    def test_update_user_password(self):
        # Update an existing user's password
        updated_user = User(username='testuser', email='testuser@example.com', password='newpassword')
        db_user = self.user_repository.update_user_password(self.user.id, updated_user)

        # Verify that the user's password was updated
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, self.user.username)
        self.assertEqual(db_user.email, self.user.email)
        self.assertEqual(db_user.password, self.user.password)