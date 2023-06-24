#!/usr/bin/env python3

"""
Module manages authentication and authorization
"""

import bcrypt
from models import storage
from models.user import User
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def hash_pwd(pswd: str) -> str:
    "Method hashes password"
    return bcrypt.hashpw(pswd.encode(), bcrypt.gensalt())

def generate_uuid() -> str:
    """Generates uuid4"""
    return str(uuid4())


class Auth:
    """Class implements authorization and authentication"""
    def register_user(self, name: str, age: int=None, gender: str, email: str, password: str,
                      contact: str=None, role: str=None) -> User:
        """Registers user"""
        try:
            user = storage.search(email, "User")
        except NoResultFound:
            password = hash_pwd(password)
            user = User(name=name, age=age, gender=gender, email=email, password=password,
                        contact=contact, role=role)
            return user
        raise ValueError(f"User {email} already exists")
    
    def valid_login(self, email: str, password: str):
        """Check if user exists"""
        try:
            user = storage.search(email, "User")
        except NoResultFound:
            pass
        
        if user:
            password = hash_pwd(password)
            if user.password = password:
                return True
        return False
    
    def create_session(self, email:str) -> str:
        """Creates session for user"""
        try:
            user = storage.search(email, "User")
        except NoResultFound:
            return None

        session_id = generate_uuid()
        key = "User" + user.id
        storage.update(key, session_id=session_id)
        return session_id
    
    def retrieve_user_by_session_id(self, session_id: str) -> User:
        """Returns user object via session_id"""
        try:
            user = storage.search(session_id, "User")
        except NoResultFound:
            return None
        return user

    def destroy_session(self, email: str) -> None:
        """Destroys session"""
        try:
            user = storage.search(email, "User")
        except NoResultFound:
            return None
        key = "User" + user.id
        storage.update(key, session_id=None)
        return None

    def password_reset_token(self, email: str) -> str:
        """Get reset token"""
        try:
            user = storage.search(email, "User")
        except NoResultFound:
            raise ValueError
        
        reset_token = generate_uuid()
        key = "User" + user.id
        storage.update(key, reser_token=reset_token)
        return reset_token
    
    def update_password(self, reset_token: str, password: str) -> None:
        """Update password"""
        if reset_token is None or password is None:
            return None
        try:
            user = storage.search(reset_token, "User")
        except NoResultFound:
            raise ValueError
        password = hash_pwd(password)
        key = "User" + user.id
        storage.update(key, password=password, reset_token=None)
        return None