#!/usr/bin/env python3
from models.__init__ import CURSOR, CONN
from models.central_bank import Central_bank
from models.bank import Bank
from models.current import Current
from models.saving import Saving
from models.loan import Loan
from models.customer import Customer
import ipdb


def reset_database():
    Central_bank.drop_table()
    Bank.drop_table()
    Current.drop_table()
    Saving.drop_table()
    Loan.drop_table()
    Customer.drop_table()
    
    Central_bank.create_table()
    Bank.create_table()
    Current.create_table()
    Saving.create_table()
    Loan.create_table()
    Customer.create_table()


    # Create seed data
    # central bank
    cbk = Central_bank.create("CBK", 8500500500.00)

    # Banks
    absa = Bank.create("ABSA", 5500500.00, cbk.id)
    equity = Bank.create("Equity", 6500500.00, cbk.id)
    santander = Bank.create("Santander", 4500500.00, cbk.id)
    kcb = Bank.create("KCB", 8500500.00, cbk.id)
    stanbic = Bank.create("Stanbic", 5500500.00, cbk.id)
    hsbc = Bank.create("HSBC", 5500500.00, cbk.id)

    # customers
    maru = Customer.create("Maru","Scot", "MaruScot@marmail.com", "Nairobi")
    hana = Customer.create("Hana","Tabby", "HanaTabby@hanmail.com", "Mombasa")
    lily = Customer.create("Lilian","Pam","LilianPam@lilmail.com", "Kisumu")
    violet = Customer.create("Violet","Brown","VioletBrown@viomail.com", "Voi")
    james = Customer.create("James","Koli","JamesKoli@jammail.com ", "Eldoret")

    # current a/c
    # account_no, balance, bank_id, customer_id,
    Current.create(1234567, 200500.00, absa.id, maru.id)
    Current.create(7654321, 300500.00, equity.id, hana.id)
    Current.create(5678910, 100500.00, santander.id, lily.id)
    Current.create(9876543, 900500.00, kcb.id, violet.id)
    Current.create(8877665, 400500.00, stanbic.id, james.id)
    Current.create(6655773, 600500.00, hsbc.id, maru.id)       # maru has another a/c with hsbc
    Current.create(2373441, 700500.00, absa.id, hana.id)
    Current.create(9333333, 880500.00, absa.id, maru.id)       # maru has 2 accounts with absa

    # saving a/c
    Saving.create(1200067, 80500.00, absa.id, maru.id)
    Saving.create(7600021, 90500.00, equity.id, hana.id)
    Saving.create(5600010, 70500.00, santander.id, lily.id)


    # loan a/c
    Loan.create(1211167, "mortgage", 55550.00, "2 years", 600.00, absa.id, maru.id)
    Loan.create(7611121, "car_loan", 77770.00, "5 years", 8000.00, equity.id, hana.id)
    Loan.create(5611110, "business", 99990.00, "3 years", 7500.00, santander.id, lily.id)
    Loan.create(8811165, "personal", 88880.00, "1 year", 1200.00, stanbic.id, james.id)

reset_database()
ipdb.set_trace()


# ==================================== Test cases ============================== #

# 1). add_account(bank, acc_type):
absa = Bank.find_by_name('ABSA')    # bank instance
customer_3 = Customer.find_by_id(3)     # customer instance
customer_3.add_account(absa, 'current')         # add review using customer instance

# 2). all_accounts_per bank
absa = Bank.find_by_name('ABSA')    # restaurant instance
absa.all_accounts()

# 3). all_accounts_per cutomer
customer_1 = Customer.find_by_id(1)    # restaurant instance
customer_1.all_accounts()
