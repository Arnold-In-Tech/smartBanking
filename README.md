# smartBanking

## Project problem statement 
- Customers want a friction-less working relationship with their financial institutions. Often, they find it difficult to connect to various banking channels resulting in frustrating experiences.

## Solution statement 
- Developing a tool that establishes links between banking channels will allow customers to seamlessly access their various bank accounts from a single access point. Information access will also improve a customers financial awareness and can consequntly help the banks provide better services, increase assets, and drive profitability.

![Static Badge](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Static Badge](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)


## Application features

We have 6 models: `Central_bank`, `Bank`, `Current`, `Saving`, `Loan` and `Customer`. 

The `Central_bank` has many `Bank`s; a `Bank` has many account types (`Current`, `Saving`, `Loan`); a `Customer` has many account types (`Current`, `Saving`, `Loan`). The account types (`Current`, `Saving`, `Loan`) belong to a `bank` and to a `customer`. `Bank` - `Customer` is a many-to-many relationship.  


# Database/Entity Relationship Diagram 
![Entity Relationship Diagram](./images/smartBanking.png?raw=true)


## Instructions

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

# Author
Arnold .A.

# Licence
All assets and code are under the [MIT](https://choosealicense.com/licenses/mit/) LICENSE and in the public domain unless specified otherwise.

