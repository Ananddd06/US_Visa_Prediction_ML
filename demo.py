# i need a banking sysytem using class and object and it need to perform withdraw , deposit , available balance before that i need to do the login password and username and use a def main function to get the while loop and get these result
class BankAccount:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance

    def login(self, username, password):
        return self.username == username and self.password == password

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance

def main():
    accounts = [
        BankAccount("user1", "pass1", 1000),
        BankAccount("user2", "pass2", 500)
    ]

    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        user = next((acc for acc in accounts if acc.login(username, password)), None)

        if user:
            print("Login successful!")
            while True:
                print("\n1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Logout")
                choice = input("Enter your choice (1-4): ")

                if choice == '1':
                    amount = float(input("Enter deposit amount: "))
                    if user.deposit(amount):
                        print("Deposit successful")
                    else:
                        print("Invalid deposit amount")
                elif choice == '2':
                    amount = float(input("Enter withdrawal amount: "))
                    if user.withdraw(amount):
                        print("Withdrawal successful")
                    else:
                        print("Insufficient funds or invalid amount")
                elif choice == '3':
                    print(f"Your current balance is: ${user.get_balance():.2f}")
                elif choice == '4':
                    print("Logout successful")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid username or password. Please try again.")

        continue_banking = input("Do you want to continue banking? (y/n): ")
        if continue_banking.lower() != 'y':
            break

    print("Thank you for using our banking system!")

if __name__ == "__main__":
    main()