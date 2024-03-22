# lib/models/current.py
from models.__init__ import CURSOR, CONN
from models.bank import Bank
from models.customer import Customer


class Current:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, account_no, balance, bank_id, customer_id, id=None):
        self.id = id
        self.account_no = account_no
        self.balance = balance
        self.bank_id = bank_id
        self.customer_id = customer_id

    def __repr__(self):
        return (
            f"<Current {self.id}: Acc/No: {self.account_no}, Balance: {self.balance}" +
            f" Bank ID: {self.bank_id}, " +
            f" Customer ID: {self.customer_id}>\n"
        )

    @property
    def account_no(self):
        return self._account_no

    @account_no.setter
    def account_no(self, account_no):
        if isinstance(account_no, int) and len(str(account_no))==7:
            self._account_no = account_no
        else:
            raise ValueError(
                "Account number must be an integer of 7 seven numbers"
            )


    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        if isinstance(balance, float):
            self._balance = balance
        else:
            raise ValueError(
                "Account balance must be a float"
            )


    @property
    def bank_id(self):
        return self._bank_id

    @bank_id.setter
    def bank_id(self, bank_id):
        if type(bank_id) is int and Bank.find_by_id(bank_id):
            self._bank_id = bank_id
        else:
            raise ValueError(
                "Bank_id must reference a bank in the database")


    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        if type(customer_id) is int and Customer.find_by_id(customer_id):
            self._customer_id = customer_id
        else:
            raise ValueError(
                "customer_id must reference a customer in the database")


    @classmethod
    def create_table(cls):
        """ 
        Create a new table to persist the attributes of Current instances 
        """
        sql = """
            CREATE TABLE IF NOT EXISTS currents (
            id INTEGER PRIMARY KEY,
            account_no VARCHAR(300),
            balance FLOAT,
            bank_id INTEGER,
            customer_id INTEGER,
            FOREIGN KEY (bank_id) REFERENCES banks(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id))
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        """ 
        Drop the table that persists Currents instances 
        """
        sql = """
            DROP TABLE IF EXISTS currents;
        """
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        """ 
        Insert a new row with the account_no, balance, bank_id, customer_id values of the current Current a/c object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key
        """
        sql = """
                INSERT INTO currents (account_no, balance, bank_id, customer_id)
                VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.account_no, self.balance, self.bank_id, self.customer_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    def update(self):
        """
        Update the table row corresponding to the current Current a/c instance.
        """
        sql = """
            UPDATE currents
            SET account_no = ?, balance = ?, bank_id = ?, customer_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.account_no, self.balance, self.bank_id,
                             self.customer_id, self.id))
        CONN.commit()


    def delete(self):
        """
        Delete the table row corresponding to the current Current a/c instance,
        delete the dictionary entry, and reassign id attribute
        """

        sql = """
            DELETE FROM currents
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None


    @classmethod
    def create(cls, account_no, balance, bank_id, customer_id):
        """
        Initialize a new Current a/c instance and save the object to the database 
        """
        current_acc = cls(account_no, balance, bank_id, customer_id)
        current_acc.save()
        return current_acc


    @classmethod
    def instance_from_db(cls, row):
        """
        Return a Current a/c object having the attribute values from the table row.
        """

        # Check the dictionary for  existing instance using the row's primary key
        current_acc = cls.all.get(row[0])
        if current_acc:
            # ensure attributes match row values in case local instance was modified
            current_acc.account_no = int(row[1])
            current_acc.balance = float(row[2])
            current_acc.bank_id = row[3]
            current_acc.customer_id = row[4]
        else:
            # not in dictionary, create new instance and add to dictionary
            current_acc = cls(int(row[1]), float(row[2]), row[3], row[4])
            current_acc.id = row[0]
            cls.all[current_acc.id] = current_acc
        return current_acc


    @classmethod
    def find_by_id(cls, id):
        """Return Current a/c object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM currents
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None


    @classmethod
    def get_all(cls):
        """
        Return a list containing all Current a/c objects per row in the table
        """
        sql = """
            SELECT *
            FROM currents
        """

        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

