import sqlite3
import pdb

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed
        
    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
        )
        """
        CURSOR.execute(sql)
        
    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        
    def save(self):
        sql = "INSERT INTO dogs (name, breed) VALUES (?,?)"
        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.lastrowid
        
    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        # pdb.set_trace()
        dog = Dog(row[1], row[2], row[0])
        return dog
    
    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        dogs = CURSOR.execute(sql)
        doggys = [cls.new_from_db(dog) for dog in dogs.fetchall()]
        return doggys
    
    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        # pdb.set_trace()
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        # pdb.set_trace()
        dog = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(dog)
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = "SELECT * FROM dogs WHERE name =? AND breed =?"
        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        if dog:
            return cls.new_from_db(dog)
        else:
            dog = Dog(name, breed)
            dog.save()
            return dog
        
    def update(self):
        # found = Dog.find_by_id(self.id)
        sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
        dog = CURSOR.execute(sql, (self.name, self.breed, self.id)).fetchone()
        pdb.set_trace()
        
        
        