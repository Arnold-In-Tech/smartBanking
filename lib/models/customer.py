# lib/models/customer.py
from models.__init__ import CURSOR, CONN

class Customer:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, first_name, last_name, email, address, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address

    def __repr__(self):
        return (
            f"<Customer {self.id}: {self.first_name}, {self.last_name}, {self.email}, {self.address}>"
        )
    
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if isinstance(first_name, str) and len(first_name):
            self._first_name = first_name
        else:
            raise ValueError(
                "first_name must be a non-empty string"
            )
                
    
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if isinstance(last_name, str) and len(last_name):
            self._last_name = last_name
        else:
            raise ValueError(
                "last_name must be a non-empty string"
            )


    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if isinstance(email, str) and len(email):
            self._email = email
        else:
            raise ValueError(
                "email must be a non-empty string"
            )


    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if isinstance(address, str) and len(address):
            self._address = address
        else:
            raise ValueError(
                "address must be a non-empty string"
            )


    @classmethod
    def create_table(cls):
        """ 
        Create a new table to persist the attributes of Customer instances 
        """
        sql = """
            CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name VARCHAR(300),
            email VARCHAR(300),
            address VARCHAR(300))
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        """ 
        Drop the table that persists Customer instances 
        """
        sql = """
            DROP TABLE IF EXISTS customers;
        """
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        """ Insert a new row with the first_name, last_name, emmail, address, values of the current Customer object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
                INSERT INTO customers (first_name, last_name, email, address)
                VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.first_name, self.last_name, self.email, self.address))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    def update(self):
        """
        Update the table row corresponding to the current Customer instance.
        """
        sql = """
            UPDATE customers
            SET first_name = ?, last_name = ?, email = ?, address = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.first_name, self.last_name, self.email,
                            self.address, self.id))
        CONN.commit()


    def delete(self):
        """
        Delete the table row corresponding to the current Customer instance,
        delete the dictionary entry, and reassign id attribute
        """

        sql = """
            DELETE FROM customers
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None


    @classmethod
    def create(cls, first_name, last_name, email, address):
        """ 
        Initialize a new Customer instance and save the object to the database 
        """
        customer = cls(first_name, last_name, email, address)
        customer.save()
        return customer


    @classmethod
    def instance_from_db(cls, row):
        """
        Return a Customer object having the attribute values from the table row.
        """

        # Check the dictionary for an existing instance using the row's primary key
        customer = cls.all.get(row[0])
        if customer:
            # ensure attributes match row values in case local instance was modified
            customer.first_name = row[1]
            customer.last_name = row[2]
            customer.email = row[3]
            customer.address = row[4]
        else:
            # not in dictionary, create new instance and add to dictionary
            customer = cls(row[1], row[2], row[3], row[4])
            customer.id = row[0]
            cls.all[customer.id] = customer
        return customer


    @classmethod
    def find_by_id(cls, id):
        """Return a Customer object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM customers
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None


    @classmethod
    def get_all(cls):
        """Return a list containing all Customer objects per row in the table"""
        sql = """
            SELECT *
            FROM customers
        """

        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

