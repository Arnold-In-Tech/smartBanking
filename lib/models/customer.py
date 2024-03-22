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
            f"<Customer {self.id}: first name- {self.first_name}, last name- {self.last_name}, email- {self.email}, address- {self.address}>"
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
            first_name VARCHAR(300),
            last_name VARCHAR(300),
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


    def add_account(self, bank, acc_type):
   
        """
        takes a bank (an instance of the `Bank` class) and an account type
        creates a new account with the bank given the `bank_id`
        """
        from models.bank import Bank
        from models.current import Current
        from models.saving import Saving
        from models.loan import Loan

        if acc_type == "current":
            if isinstance(bank, Bank):
                account_no = input("Enter the account number: ")
                balance = float(input("Enter the opening balance: "))
                bank_id = bank.id
                new_acc = Current.create(int(account_no), balance, bank_id, self.id)
                return new_acc
            else:
                raise TypeError("bank must be an instance of Bank class;",
                                "balance must be a float")

        elif acc_type == "saving":
            if isinstance(bank, Bank):
                account_no = input("Enter the account number: ")
                balance = float(input("Enter the opening balance: "))
                bank_id = bank.id
                new_acc = Saving.create(int(account_no), balance, bank_id, self.id)
                return new_acc
            else:
                raise TypeError("bank must be an instance of Bank class;",
                                "balance must be a float")            

        elif acc_type == "loan":
            if isinstance(bank, Bank):
                account_no = input("Enter the account number: ")
                loan_type = input("Enter the loan type: ")
                loan_amount = float(input("Enter the loan amount: "))
                duration = input("Enter the duration of the loan: ")
                paid_amount = float(input("Enter the amount paid: "))
                bank_id = bank.id
                new_acc = Loan.create(int(account_no), loan_type, loan_amount, duration, paid_amount, bank_id, self.id)
                return new_acc
            else:
                raise TypeError("bank must be an instance of Bank class;",
                                "balance must be a float")
        else:
            raise TypeError("You can only open a current, saving, or loan account")

        
    # === for list_all_bank_accounts
    def current_accounts(self):
        """
        returns a collection of all the accounts for the `Bank`
        """
        from models.current import Current
        sql = """
            SELECT * FROM currents
            WHERE customer_id = ?
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
            WHERE customer_id = ?
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
            WHERE customer_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Loan.instance_from_db(row) for row in rows
        ]


    def all_accounts(self):
        """
        should return a list of strings with all the accounts for this customer :
        """
        current_accs = [acc for acc in self.current_accounts()]
        saving_accs = [acc for acc in self.saving_accounts()]
        loan_accs = [acc for acc in self.loan_accounts()]
        return current_accs + saving_accs + loan_accs 


    def customer_banks_balance(self):
        """
        Display customer's balance in all bank accounts
        """
        from models.bank import Bank
        current_accs = [acc for acc in self.current_accounts()]
        saving_accs = [acc for acc in self.saving_accounts()]
        loan_accs = [acc for acc in self.loan_accounts()]

        curr = [f"Acc/No: {i.account_no} | Acc/Type: Current | Name: {self.full_name()} | Balance: {i.balance} | Bank: {Bank.find_by_id(i.bank_id).name}" for i in current_accs]
        sav = [f"Acc/No: {i.account_no} | Acc/Type: Saving | Name: {self.full_name()} | Balance: {i.balance} | Bank: {Bank.find_by_id(i.bank_id).name}" for i in saving_accs]
        loa = [f"Acc/No: {i.account_no} | Acc/Type: Loan | Name: {self.full_name()} | Balance: {i.loan_amount - i.paid_amount} | Bank: {Bank.find_by_id(i.bank_id).name} \n" for i in loan_accs]
        return curr + sav + loa


    def full_name(self):
        """
        returns the full name of the customer, with the first name and the last name  concatenated, Western style.
        """
        return f"{self.first_name} {self.last_name}"


    def net_worth(self):
        print("\nNet-worth = (Current balance + Savings balance) - Loan balance")
        from models.bank import Bank
        current_accs = [acc for acc in self.current_accounts()]
        saving_accs = [acc for acc in self.saving_accounts()]
        loan_accs = [acc for acc in self.loan_accounts()]

        curr = sum([i.balance if len(current_accs) > 0 else 0 for i in current_accs ])
        sav = sum([i.balance if len(saving_accs) > 0 else 0 for i in saving_accs ])
        loa = sum([(i.loan_amount - i.paid_amount) if len(loan_accs) > 0 else 0 for i in loan_accs ])
        return f"{self.full_name()}'s Net-worth is KSh. {curr + sav + loa} \n"
