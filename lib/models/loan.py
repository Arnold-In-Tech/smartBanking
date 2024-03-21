# lib/models/loan.py
from models.__init__ import CURSOR, CONN
from models.bank import Bank
from models.customer import Customer


class Loan:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, account_no, loan_type, loan_amount, duration, paid_amount, bank_id, customer_id, id=None):
        self.id = id
        self.account_no = account_no
        self.loan_type = loan_type
        self.loan_amount = loan_amount
        self.duration = duration
        self.paid_amount = paid_amount
        self.bank_id = bank_id
        self.customer_id = customer_id

    def __repr__(self):
        return (
            f"<Current {self.id}: {self.account_no}, {self.loan_type}, 
            {self.loan_amount}, {self.duration}, {self.paid_amount}" +
            f"Bank ID: {self.bank_id}, " +
            f"Customer ID: {self.customer_id}>"
        )

    @property
    def account_no(self):
        return self._account_no

    @account_no.setter
    def account_no(self, account_no):
        if isinstance(account_no, int) and len(account_no)==7:
            self._account_no = account_no
        else:
            raise ValueError(
                "Account number must be an integer of 7 seven numbers"
            )

    @property
    def loan_type(self):
        return self._loan_type

    @loan_type.setter
    def loan_type(self, loan_type):
        if isinstance(loan_type, str) and len(loan_type):
            self._loan_type = loan_type
        else:
            raise ValueError(
                "loan_type must be a non-empty string"
            )

    @property
    def loan_amount(self):
        return self._loan_amount

    @loan_amount.setter
    def loan_amount(self, loan_amount):
        if isinstance(loan_amount, float):
            self._loan_amount = loan_amount
        else:
            raise ValueError(
                "Loan amount must be a float"
            )

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        if isinstance(duration, str) and len(duration):
            self._duration = duration
        else:
            raise ValueError(
                "duration must be a non-empty string"
            )

    @property
    def paid_amount(self):
        return self._paid_amount

    @paid_amount.setter
    def paid_amount(self, paid_amount):
        if isinstance(paid_amount, float):
            self._paid_amount = paid_amount
        else:
            raise ValueError(
                "Paid amount must be a float"
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
            CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY,
            account_no VARCHAR(300),
            loan_type VARCHAR(300),
            loan_amount FLOAT,
            duration VARCHAR(300)
            paid_amount FLOAT,
            bank_id INTEGER,
            customer_id INTEGER,
            FOREIGN KEY (bank_id) REFERENCES banks(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)))
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        """ 
        Drop the table that persists Loans instances 
        """
        sql = """
            DROP TABLE IF EXISTS loans;
        """
        CURSOR.execute(sql)
        CONN.commit()


    def save(self):
        """ 
        Insert a new row with the account_no, loan_type, loan_amount, duration, paid_amount, 
        bank_id, customer_id values of the current Loan a/c object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key
        """
        sql = """
                INSERT INTO currents (account_no, loan_type, loan_amount, duration, paid_amount, bank_id, customer_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.account_no, self.loan_type, self.loan_amount, self.duration,
                              self.paid_amount, self.bank_id, self.customer_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self


    def update(self):
        """
        Update the table row corresponding to the current Loan instance.
        """
        sql = """
            UPDATE loans
            SET account_no = ?, loan_type = ?, loan_amount = ?, duration = ?, paid_amount = ?, bank_id = ?, customer_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.account_no, self.loan_type, self.loan_amount, self.duration,
                              self.paid_amount, self.bank_id, self.customer_id, self.id))
        CONN.commit()


    def delete(self):
        """
        Delete the table row corresponding to the current Loan instance,
        delete the dictionary entry, and reassign id attribute
        """

        sql = """
            DELETE FROM loans
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None


    @classmethod
    def create(cls, account_no, loan_type, loan_amount, duration, paid_amount, bank_id, customer_id):
        """
        Initialize a new Loan instance and save the object to the database 
        """
        loan_acc = cls(account_no, loan_type, loan_amount, duration, paid_amount, bank_id, customer_id)
        loan_acc.save()
        return loan_acc


    @classmethod
    def instance_from_db(cls, row):
        """
        Return a Loan object having the attribute values from the table row.
        """

        # Check the dictionary for  existing instance using the row's primary key
        loan_acc = cls.all.get(row[0])
        if loan_acc:
            # ensure attributes match row values in case local instance was modified
            loan_acc.account_no = row[1]
            loan_acc.loan_type = row[2]
            loan_acc.loan_amount = row[3]
            loan_acc.duration = row[4]
            loan_acc.paid_amount = row[5]
            loan_acc.bank_id = row[6]
            loan_acc.customer_id = row[7]
        else:
            # not in dictionary, create new instance and add to dictionary
            loan_acc = cls(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            loan_acc.id = row[0]
            cls.all[loan_acc.id] = loan_acc
        return loan_acc


    @classmethod
    def find_by_id(cls, id):
        """
        Return Loan object corresponding to the table row matching the specified primary key
        """
        sql = """
            SELECT *
            FROM loans
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None


    @classmethod
    def get_all(cls):
        """
        Return a list containing all Loan objects per row in the table
        """
        sql = """
            SELECT *
            FROM loans
        """

        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

