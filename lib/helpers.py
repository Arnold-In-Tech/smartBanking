#!/usr/bin/env python3
from models.__init__ import CURSOR, CONN
from models.bank import Bank
from models.customer import Customer


def exit_program():
    print("Goodbye!")
    exit()


# ============== Bank functions
def list_banks():
    banks = Bank.get_all()
    for bank in banks:
        print(bank)


def find_bank_by_name():
    name = input("Enter the bank's name: ")
    bank = Bank.find_by_name(name)
    print(bank) if bank else print(
        f'Bank {name} not found')


def find_bank_by_id():
    id_ = input("Enter the bank's id: ")
    bank = Bank.find_by_id(id_)
    print(bank) if bank else print(f'Bank {id_} not found')


def create_bank():
    name = input("Enter the bank's name: ")
    bank_reserve = input("Enter the bank reserve amount: ")
    central_bank_id = input("Enter the central bank id : ")
    try:
        bank = Bank.create(name, bank_reserve, central_bank_id)
        print(f'Success: {bank}')
    except Exception as exc:
        print("Error creating bank: ", exc)


def update_bank():
    id_ = input("Enter the bank's id: ")
    if bank := Bank.find_by_id(id_):
        try:
            name = input("Enter the bank's new name: ")
            bank.name = name
            bank_reserve = input("Enter the bank's new reserve amount: ")
            bank.bank_reserve = bank_reserve
            central_bank_id = 1

            bank.update()
            print(f'Success: {bank}')
        except Exception as exc:
            print("Error updating bank: ", exc)
    else:
        print(f'Bank {id_} not found')


def delete_bank():
    id_ = input("Enter the bank's id: ")
    if bank := Bank.find_by_id(id_):
        bank.delete()
        print(f'Bank {id_} deleted')
    else:
        print(f'Bank {id_} not found')


# ============== Customer functions
def list_customers():
    customers = Customer.get_all()
    for customer in customers:
        print(customer)


def find_customer_by_name():
    name = input("Enter the customer's name: ")
    customer = Customer.find_by_name(name)
    print(customer) if customer else print(
        f'Customer {name} not found')


def find_customer_by_id():
    id_ = input("Enter the Customer's id: ")
    customer = Customer.find_by_id(id_)
    print(customer) if customer else print(
        f'Customer {id_} not found')
    

def create_customer():
    # first_name, last_name, email, address,
    first_name = input("Enter the customer's first name: ")
    last_name = input("Enter the customer's last name: ")
    email = input("Enter the customer's email: ")
    address = input("Enter the customer's address: ")
    try:
        customer = Customer.create(first_name, last_name, email, address)
        print(f'Success: {customer}')
    except Exception as exc:
        print("Error creating customer: ", exc)



def update_customer():
    id_ = input("Enter the customer's id: ")
    if customer := Customer.find_by_id(id_):
        try:
            first_name = input("Enter the customer's new first_name: ")
            customer.first_name = first_name
            last_name = input("Enter the customer's new last_name: ")
            customer.last_name = last_name
            email = input("Enter the customer's new email: ")
            customer.email = email 
            address = input("Enter the customer's new address: ")
            customer.address = address

            customer.update()
            print(f'Success: {customer}')

        except Exception as exc:
            print("Error updating customer: ", exc)
    else:
        print(f'Customer {id_} not found')


def delete_customer():
    id_ = input("Enter the customer's id: ")
    if customer := Customer.find_by_id(id_):
        customer.delete()
        print(f'customer {id_} deleted')
    else:
        print(f'customer {id_} not found')


# ============= Accounts functions/Utilities

# in order to create an a/c, a bank and a customer have to exist first
def add_an_account():
    bank_name = input("Enter the bank name: ")
    id_ = input("Enter the customer's id: ")    
    acc_type = input("Enter the account type you would like to open: ")
    bank_ins = Bank.find_by_name(bank_name) # bank instance
    customer_ins = Customer.find_by_id(id_)     # customer instance
    new_acc = customer_ins.add_account(bank_ins, acc_type)
    print(f"\nSuccess! {new_acc}") if new_acc else None


# list all accounts associated with a particular bank
def list_all_bank_accounts():
    name = input("Enter the bank's name: ")
    bank_ins = Bank.find_by_name(name)    # bank instance
    print(bank_ins.all_accounts())

# list all accounts and banks associated with a particular customer
def list_all_customer_accounts():
    id_ = input("Enter the customer's id: ")
    customer_ins = Customer.find_by_id(id_)    # customer instance
    print(customer_ins.all_accounts())


# Check balance in all accounts and banks a particular customer holds
def list_all_customer_accounts_balances():
    id_ = input("Enter the customer's id: ")
    customer_ins = Customer.find_by_id(id_)    # customer instance
    [print(item) for item in customer_ins.customer_banks_balance()]


def customer_net_worth():
    id_ = input("Enter the customer's id: ")
    customer_ins = Customer.find_by_id(id_)    # customer instance
    print(customer_ins.net_worth())
