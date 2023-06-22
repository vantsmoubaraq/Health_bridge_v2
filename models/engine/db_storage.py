#!/usr/bin/python3

"""Module implements database storage"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel
from models.patients import Patient, patient_drug
from models.drugs import Drug
from models.payments import Payment
from models.base_model import Base
from os import getenv

classes = {"Patient": Patient, "Drug": Drug, "Payment": Payment, "patient_drug": patient_drug}


class DB_Storage:
    """Class Implements Database Storage"""
    __engine = None
    __session = None

    def __init__(self):
        environment = getenv("HB_ENV")
        database = getenv("HB_DB")
        user = getenv("HB_USER")
        password = getenv("HB_PWD")
        host = getenv("HB_HOST")
        dialct = "mysql+mysqldb"

        self.__engine = create_engine("{}://{}:{}@localhost:3306/{}".
                                      format(dialct, user, password, database))
    #if DB_Storage.environment == "test":
     #   Base.metadata.drop_all(self.__engine)

    def create(self, obj):
        """Stage object"""
        self.__session.add(obj)

    def save(self):
        """save to database"""
        self.__session.commit()

    def all(self, cls=None):
        """retrieves objects from storage"""
        if cls:
            objs = {}
            class_objs = self.__session.query(classes[cls]).all()
            for obj in class_objs:
                key = obj.__class__.__name__ + "." + obj.id
                objs[key] = obj
            return objs

        all_objects = {}

        for cls in classes:
            objs = self.__session.query(classes[cls]).all()
            for obj in objs:
                key = obj.__class__.__name__ + "." + obj.id
                all_objects[key] = obj
        return all_objects

    def delete(self, obj):
        """Delete object"""
        self.__session.delete(obj)
        self.__session.commit()

    def update(self, key, **kwargs):
        """Update instance"""
        obj_id = key.split(".")[1]
        class_name = key.split(".")[0]
        obj = self.__session.query(classes[class_name
                                           ]).filter_by(id=obj_id).first()
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.__session.commit()

    def get(self, class_name,  obj_id):
        """gets single instance based on id"""
        for key in self.all(class_name).keys():
            oid = key.split(".")[1]
            if obj_id == oid:
                obj = self.__session.query(classes[class_name
                                                   ]).filter_by(id=oid).first()
                return (obj)
        return None

    def reload(self):
        """starts session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def count(self, cls=None):
        """returns number of all objects"""
        if cls:
            return len(self.all(cls))
        return len(self.all())

    def close(self):
        """Closes transaction"""
        self.__session.close()

    def search(self, query, cls):
        """searchs against a query string"""
        results = self.__session.query(classes[cls]).filter(classes[cls].name.ilike(f'%{query}%')).all()
        return results
