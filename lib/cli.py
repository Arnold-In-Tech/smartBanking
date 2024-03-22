
from helpers import (
    exit_program,
    list_banks,
    find_bank_by_name,
    find_bank_by_id,
    create_bank,
    update_bank,
    delete_bank,
    list_customers,
    find_customer_by_first_name,
    find_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
    add_an_account,
    list_all_bank_accounts,
    list_all_customer_accounts,
    list_all_customer_accounts_balances,
    customer_net_worth
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            while choice:
                print("#======================#")
                print("#    Bank Utilities    #")
                print("#======================#\n")
                bank_menu()
                new_choice = input("> ")
                if new_choice == "0":
                    choice = ""
                    print("\n#==== Back to main menu! ====#")
                elif new_choice == "1":
                    list_banks()
                elif new_choice == "2":
                    find_bank_by_name()
                elif new_choice == "3":
                    find_bank_by_id()
                elif new_choice == "4":
                    create_bank()
                elif new_choice == "5":
                    update_bank()
                elif new_choice == "6":
                    delete_bank()
                else:
                    print("Invalid choice")

        elif choice == "2":
            while choice:
                print("#======================#")
                print("#  Customer Utilities  #")
                print("#======================#\n")
                customer_menu()
                new_choice = input("> ")
                if new_choice == "0":
                    choice = ""
                    print("\n#==== Back to main menu! ====#")
                elif new_choice == "1":
                    list_customers()
                elif new_choice == "2":
                    find_customer_by_first_name()
                elif new_choice == "3":
                    find_customer_by_id()
                elif new_choice == "4":
                    create_customer()
                elif new_choice == "5":
                    update_customer()
                elif new_choice == "6":
                    delete_customer()
                else:
                    print("Invalid choice")
            
        elif choice == "3":
            while choice:
                print("#======================#")
                print("#  Accounts Utilities  #")
                print("#======================#\n")
                accounts_menu()
                new_choice = input("> ")
                if new_choice == "0":
                    choice = ""
                    print("\n#==== Back to main menu! ====#")
                elif new_choice == "1":
                    add_an_account()
                elif new_choice == "2":
                    list_all_bank_accounts()
                elif new_choice == "3":
                    list_all_customer_accounts()
                elif new_choice == "4":
                    list_all_customer_accounts_balances()
                elif new_choice == "5":
                    customer_net_worth()
                else:
                    print("Invalid choice")
            


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Bank utilities")
    print("2. Customer utilities")
    print("3. Account utilities")
    
def bank_menu():
    print("Please select an option:")
    print("0. Go back")
    print("1. List all banks")
    print("2. Find bank by name")
    print("3. Find bank by id")
    print("4: Create bank")
    print("5: Update bank")
    print("6: Delete bank")
 

def customer_menu():
    print("Please select an option:")
    print("0. Go back")
    print("1. List all customers")
    print("2. Find customer by first name")
    print("3. Find customer by id")
    print("4: Create customer")
    print("5: Update customer")
    print("6: Delete customer")



def accounts_menu():
    print("Please select an option:")
    print("0. Go back")
    print("1. Add/Register an account")
    print("2. List all accounts registered with a specific bank")
    print("3. List all accounts registered to a specific customer")
    print("4. Display customer's balance in all bank accounts")
    print("5. Calculate a customers' Networth")
    



if __name__ == "__main__":
    main()
