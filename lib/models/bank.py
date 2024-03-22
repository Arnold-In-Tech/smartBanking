# lib/models/bank.py
from models.__init__ import CURSOR, CONN
from models.central_bank import Central_bank


class Bank:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, bank_reserve, central_bank_id, id=None):
        self.id = id
        self.name = name
        self.bank_reserve = bank_reserve
        self.central_bank_id = central_bank_id

    def __repr__(self):
        return (
            f"<Bank {self.id}: Name: {self.name}, Bank reserve (Kshs): {self.bank_reserve} " +
            f" Central_bank ID: {self.central_bank_id}>"
        )

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
    def bank_reserve(self):
        return self._bank_reserve

    @bank_reserve.setter
    def bank_reserve(self, bank_reserve):
        if isinstance(bank_reserve, float):
            self._bank_reserve = bank_reserve
        else:
            raise ValueError(
                "bank_reserve must be a float"
            )


    @property
    def central_bank_id(self):
        return self._central_bank_id

    @central_bank_id.setter
    def central_bank_id(self, central_bank_id):
        if type(central_bank_id) is int and Central_bank.find_by_id(central_bank_id):
            self._central_bank_id = central_bank_id
        else:
            raise ValueError(
                "central_bank_id must reference the central bank in the database")


    @classmethod
    def create_table(cls):
        """ 
        Create a new table to persist the attributes of Bank instances 
        """
        sql = """
            CREATE TABLE IF NOT EXISTS banks (
            id INTEGER PRIMARY KEY,
            name VARCHAR(300),
            bank_reserve FLOAT,
            central_bank_id INTEGER,
            FOREIGN KEY (central_bank_id) REFERENCES central_bank(id))
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        """ 
        Drop the table that persists Employee instances 
        """
        sql = """
            DROP TABLE IF EXISTS banks;
        """
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        """ 
        Insert a new row with the name, bank_reserve, and central_bank_id values of the current Bank object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key
        """
        sql = """
                INSERT INTO banks (name, bank_reserve, central_bank_id)
                VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.bank_reserve, self.central_bank_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    def update(self):
        """
        Update the table row corresponding to the current Employee instance.
        """
        sql = """
            UPDATE banks
            SET name = ?, bank_reserve = ?, central_bank_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.bank_reserve,
                             self.central_bank_id, self.id))
        CONN.commit()


    def delete(self):
        """
        Delete the table row corresponding to the current Bank instance,
        delete the dictionary entry, and reassign id attribute
        """

        sql = """
            DELETE FROM banks
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None


    @classmethod
    def create(cls, name, bank_reserve, central_bank_id):
        """ 
        Initialize a new Bank instance and save the object to the database 
        """
        bank = cls(name, bank_reserve, central_bank_id)
        bank.save()
        return bank


    @classmethod
    def instance_from_db(cls, row):
        """
        Return a Bank object having the attribute values from the table row.
        """

        # Check the dictionary for  existing instance using the row's primary key
        bank = cls.all.get(row[0])
        if bank:
            # ensure attributes match row values in case local instance was modified
            bank.name = row[1]
            bank.bank_reserve = row[2]
            bank.central_bank_id = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            bank = cls(row[1], row[2], row[3])
            bank.id = row[0]
            cls.all[bank.id] = bank
        return bank


    @classmethod
    def get_all(cls):
        """
        Return a list containing one Bank object per table row
        """
        sql = """
            SELECT *
            FROM banks
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]


    @classmethod
    def find_by_id(cls, id):
        """
        Return Bank object corresponding to the table row matching the specified primary key
        """
        
        sql = """
            SELECT *
            FROM banks
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None


    @classmethod
    def find_by_name(cls, name):
        """
        Return Bank object corresponding to first table row matching specified name
        """

        sql = """
            SELECT *
            FROM banks
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None


    # === for list_all_bank_accounts
    def current_accounts(self):
        """
        returns a collection of all the accounts for the `Bank`
        """
        from models.current import Current
        sql = """
            SELECT * FROM currents
            WHERE bank_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Current.instance_from_db(row) for row in rows
        ]


    def saving_accounts(self):
        """
        returns a collection of all the accounts for the `Bank`
        """
        from models.saving import Saving
        sql = """
            SELECT * FROM savings
            WHERE bank_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Saving.instance_from_db(row) for row in rows
        ]


    def loan_accounts(self):
        """
        returns a collection of all the accounts for the `Bank`
        """
        from models.loan import Loan
        sql = """
            SELECT * FROM loans
            WHERE bank_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Loan.instance_from_db(row) for row in rows
        ]


    def all_accounts(self):
        """
        should return a list of strings with all the accounts for this bank :
        """
        current_accs = [acc for acc in self.current_accounts()]
        saving_accs = [acc for acc in self.saving_accounts()]
        loan_accs = [acc for acc in self.loan_accounts()]
        return current_accs + saving_accs + loan_accs 
    
