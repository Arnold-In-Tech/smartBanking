# smartBanking Application

## Project problem statement 
Customers want a friction-less working relationship with their financial institutions. Often, they find it difficult to connect to various banking channels resulting in frustrating experiences.

## Solution statement 
Developing a tool that establishes links between banking channels will allow customers to seamlessly access their various bank accounts from a single access point. Information access will also improve a customers financial awareness and can consequntly help the banks provide better services, increase assets, and drive profitability.

## Technology stack
![Static Badge](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Static Badge](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Static Badge](https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white)

# Entity relationship diagram 
![Entity Relationship Diagram](./images/smartBanking.png?raw=true)


# Features
We have 6 models: `Central_bank`, `Bank`, `Current`, `Saving`, `Loan` and `Customer`. 

The `Central_bank` has many `Bank`s ; a `Bank` has many account types (`Current`, `Saving`, `Loan`); a `Customer` has many account types (`Current`, `Saving`, `Loan`). The account types (`Current`, `Saving`, `Loan`) belong to a `bank` and to a `customer`. `Bank` - `Customer` is a many-to-many relationship.  
## Application features
- Create, Read, Update, Delete banks, customers and accounts from the database.
- Add new banks accounts to new and existing customers to the database.
- View a list of all banks, customers, and accounts.
- View accounts related to a specific bank.
- View accounts related to a specific customer.
- View accounts balance related to a specific customer.
- Calculate a customers' Net-worth based balances existing in all bank accounts. N/B (Net-worth = (Current balance + Savings balance) - Loan balance)


# Instructions
## Installation

Clone the repository
```bash
git clone git@github.com:Arnold-In-Tech/smartBanking.git
```


## Install dependencies

To get started, run `pipenv install` while inside of this directory. Then run
`pipenv shell` to jump into the shell.


## Program execution

On the terminal:
#### 1. Seed the database
```bash
python3 ./lib/seed.py
```

#### 2. To execute the program, run the command line interface
```bash
python3 ./lib/cli.py
```

## CLI Commands
1. Bank utilities
- List all banks
- Find bank by name
- Find bank by id
- Create bank
- Update bank
- Delete bank

2. Customer utilities
- List all customers
- Find customer by name
- Find customer by id
- Create customer
- Update customer
- Delete customer

3. Account utilities
- Add/Register an account
- List all accounts registered with a specific bank
- List all accounts registered to a specific customer
- Display customer's balance in all bank accounts
- Calculate a customers' Net-worth


## Future enhancements
- Add feature to calculate interest on loans
- Add cash withdrawal and deposit methods
- Add feature to auto-update balance on cash withdrawal, deposit, and loan payment


# Author
Arnold .A.


# Licence
All assets and code are under the [MIT](https://choosealicense.com/licenses/mit/) LICENSE and in the public domain unless specified otherwise.

