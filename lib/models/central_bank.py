# lib/models/central_bank.py
from models.__init__ import CURSOR, CONN


# N/B: There will only be a single central bank responsible for regulating money supply

class Central_bank:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, central_reserve, id=None):
        self.id = id
        self.name = name
        self.central_reserve = central_reserve

    def __repr__(self):
        return f"<Central bank {self.id}: {self.name}, {self.central_reserve}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def central_reserve(self):
        return self._central_reserve

    @central_reserve.setter
    def central_reserve(self, central_reserve):
        if isinstance(central_reserve, float):
            self._central_reserve = central_reserve
        else:
            raise ValueError(
                "Central_reserve must be a float"
            )


    @classmethod
    def create_table(cls):
        """ 
        Create a new table to persist the attributes of Central bank instances 
        """
        sql = """
            CREATE TABLE IF NOT EXISTS central_banks (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            central_reserve FLOAT)
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Central_bank instances """
        sql = """
            DROP TABLE IF EXISTS central_banks;
        """
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        """
        Insert a new row with the name, central_reserve values of the current Central_bank object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key
        """

        sql = """
            INSERT INTO central_banks (name, central_reserve)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.central_reserve))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    @classmethod
    def create(cls, name, central_reserve):
        """
        Initialize a new Central_bank instance and save the object to the database 
        """
        central_bank = cls(name, central_reserve)
        central_bank.save()
        return central_bank


    @classmethod
    def instance_from_db(cls, row):
        """Return an Central_bank object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        central_bank = cls.all.get(row[0])
        if central_bank:
            # ensure attributes match row values in case local instance was modified
            central_bank.name = row[1]
            central_bank.central_reserve = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            central_bank = cls(row[1], row[2])
            central_bank.id = row[0]
            cls.all[central_bank.id] = central_bank
        return central_bank


    @classmethod
    def find_by_id(cls, id):
        """
        Return Central_bank object corresponding to the table row matching the specified primary key
        """
        sql = """
            SELECT *
            FROM central_banks
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None




