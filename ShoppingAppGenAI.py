#
#Database Initialization: The script checks if the user and product databases exist. If not, it creates them.

#Classes:

#User: Handles user login, signup, password change, and account deletion.

#Admin: Inherits from User and adds functionalities to manage products and categories.

#ShoppingCart: Manages the cart operations like adding, removing, viewing, and checking out items.

#Main Function: Handles the initial login/signup process and directs users to the appropriate menu based on their role.

#Admin Menu: Admin can add, update, and delete products and categories.

#User Menu: Users can view products, manage their cart, checkout, change their password, and delete their account.

#Cart Management: Users can add or remove items from their cart.

#Checkout: Users can select a payment method and complete their purchase.

#Password Management: Users can change their password.

#Account Deletion: Users can delete their account.

#Error Handling: The script includes basic error handling for invalid inputs.

#Console Clearing: The script clears the console for a fresh start each time.

#This script provides a backend implementation for a shopping application using Python and pandas to manage data in Excel files.






import pandas as pd
import os
import sys

# Constants
USER_DB = 'user_db.xlsx'
PRODUCT_DB = 'product_db.xlsx'
CATEGORIES = ['Footwear', 'T-shirts', 'Jeans', 'Wallets', 'Bags']
ADMIN_CREDENTIALS = {'username': 'Admin1', 'password': 'Admin123', 'role': 'admin'}

# Clear console function
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Initialize databases if not present
def initialize_databases():
    if not os.path.exists(USER_DB):
        user_data = pd.DataFrame(columns=['username', 'password', 'role', 'session_id'])
        user_data = user_data._append(ADMIN_CREDENTIALS, ignore_index=True)
        user_data.to_excel(USER_DB, index=False)
    
    if not os.path.exists(PRODUCT_DB):
        product_data = pd.DataFrame(columns=['product_id', 'name', 'category', 'price'])
        product_data.to_excel(PRODUCT_DB, index=False)

# Load databases
def load_databases():
    user_data = pd.read_excel(USER_DB)
    product_data = pd.read_excel(PRODUCT_DB)
    global CATEGORIES
    CATEGORIES = list(set(product_data['category'].to_list()))
    return user_data, product_data

# Save databases
def save_database_product(product_data):
    #user_data.to_excel(USER_DB, index=False)
    product_data.to_excel(PRODUCT_DB, index=False)

def save_database_user(user_data):
    user_data.to_excel(USER_DB, index=False)
    #product_data.to_excel(PRODUCT_DB, index=False)

class User:
    def __init__(self, username, password, role='user', session_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.session_id = session_id

    def login(self, user_data):
        user = user_data[(user_data['username'] == self.username) & (user_data['password'] == self.password)]
        if not user.empty:
            self.session_id = os.urandom(16).hex()
            user_data.loc[user.index, 'session_id'] = self.session_id
            return True
        return False

    def signup(self, user_data):
        if self.username == ADMIN_CREDENTIALS['username']:
            print("Username 'Admin1' is reserved. Please choose another username.")
            return user_data
        if self.username in user_data['username'].values:
            print("Username already exists. Please choose another username.")
            return user_data
        new_user = {'username': self.username, 'password': self.password, 'role': self.role, 'session_id': ''}
        user_data = user_data._append(new_user, ignore_index=True)
        return user_data

    def change_password(self, user_data, new_password):
        user_data.loc[user_data['session_id'] == self.session_id, 'password'] = new_password
        print("Password changed successfully.")
        return user_data

    def delete_account(self, user_data):
        user_data = user_data[user_data['session_id'] != self.session_id]
        print("Account deleted successfully.")
        return user_data

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, role='admin')

    def add_product(self, product_data, product_id, name, category, price):
        product = product_data[product_data['product_id'] == int(product_id)]
        if product.empty and (category in CATEGORIES):
            new_product = {'product_id': product_id, 'name': name, 'category': category, 'price': price}
            product_data = product_data._append(new_product, ignore_index=True)
            print("Product added successfully.")
        else:
            print('Product ID Already Exist or Category Does not Exist')
        return product_data

    def update_product(self, product_data, product_id, name, category, price):
        product_id = int(product_id)
        product = product_data[product_data['product_id'] == product_id]
        if not product.empty and (category in CATEGORIES):
            product_data.loc[product.index, ['name', 'category', 'price']] = [name, category, price]
            print("Product updated successfully.")
        else:
            print("Product or Category not found.")
        return product_data

    def delete_product(self, product_data, product_id):
        product_id = int(product_id)
        product = product_data[product_data['product_id'] == product_id]
        if not product.empty:
            product_data.drop(product_data.index[(product_data["product_id"] == product_id)],axis=0,inplace=True)
            print("Product deleted successfully.")
        else:
            print("Product not found.")
        return product_data

    def add_category(self, category):
        if category not in CATEGORIES:
            CATEGORIES.append(category)
            print("Category added successfully.")
        else:
            print("Category already exists.")

    def delete_category(self, category):
        if category in CATEGORIES:
            CATEGORIES.remove(category)
            print("Category deleted successfully.")
        else:
            print("Category not found.")

class ShoppingCart:
    def __init__(self):
        self.cart = []

    def add_to_cart(self, product_data, product_id, quantity):
        product = product_data[product_data['product_id'] == product_id]
        if not product.empty:
            self.cart.append({'product_id': product_id, 'quantity': quantity})
            print("Product added to cart.")
        else:
            print("Product not found.")

    def remove_from_cart(self, product_id):
        self.cart = [item for item in self.cart if item['product_id'] != product_id]
        print("Product removed from cart.")

    def view_cart(self):
        print("\nCart Contents:")
        for item in self.cart:
            print(f"Product ID: {item['product_id']}, Quantity: {item['quantity']}")

    def checkout(self):
        if self.cart:
            print("Select payment method:")
            print("1. Net Banking")
            print("2. PayPal")
            print("3. UPI")
            choice = input("Enter your choice: ")
            if choice in ['1', '2', '3']:
                print("Your order is successfully placed.")
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Cart is empty.")

def main():
    clear_console()
    print("Welcome to the Demo Marketplace")
    initialize_databases()
    user_data, product_data = load_databases()
    
    while True:
        print("\n1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
                admin = Admin(username, password)
                admin_menu(admin, product_data)
            else:
                user = User(username, password)
                if user.login(user_data):
                    user_menu(user, user_data, product_data)
                else:
                    print("Invalid credentials. Try again or create a new account.")
        elif choice == '2':
            username = input("Enter new username: ")
            password = input("Enter new password: ")
            user = User(username, password)
            user_data = user.signup(user_data)
        elif choice == '3':
            print("Thank you and goodbye!")
            try:
                save_database_product(product_data)
                save_database_user(user_data)
            except NameError:
                pass
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def admin_menu(admin, product_data):
    while True:
        print("\nAdmin Menu:")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. Add Category")
        print("5. Delete Category")
        print("6. View Catalogue")
        print("7. View Categories")
        print("8. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            price = float(input("Enter product price: "))
            product_data = admin.add_product(product_data, product_id, name, category, price)
        elif choice == '2':
            product_id = input("Enter product ID to update: ")
            name = input("Enter new product name: ")
            category = input("Enter new product category: ")
            price = float(input("Enter new product price: "))
            product_data = admin.update_product(product_data, product_id, name, category, price)
        elif choice == '3':
            product_id = input("Enter product ID to delete: ")
            product_data = admin.delete_product(product_data, product_id)
        elif choice == '4':
            category = input("Enter new category: ")
            admin.add_category(category)
        elif choice == '5':
            category = input("Enter category to delete: ")
            admin.delete_category(category)
        elif choice == '6':
            print("\nProduct Catalog:")
            print(product_data)
        elif choice == '7':
            print("\nThe Category")
            print(CATEGORIES)
        elif choice == '8':
            print("Thank you and goodbye!")
            try:
                save_database_product(product_data)
                save_database_user(user_data)
            except NameError:
                pass
                
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def user_menu(user, user_data, product_data):
    cart = ShoppingCart()
    while True:
        print("\nUser Menu:")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. Remove from Cart")
        print("4. View Cart")
        print("5. Checkout")
        print("6. Change Password")
        print("7. Delete Account")
        print("8. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_products(product_data)
        elif choice == '2':
            product_id = input("Enter product ID to add to cart: ")
            quantity = int(input("Enter quantity: "))
            cart.add_to_cart(product_data, product_id, quantity)
        elif choice == '3':
            product_id = input("Enter product ID to remove from cart: ")
            cart.remove_from_cart(product_id)
        elif choice == '4':
            cart.view_cart()
        elif choice == '5':
            cart.checkout()
        elif choice == '6':
            new_password = input("Enter new password: ")
            user_data = user.change_password(user_data, new_password)
        elif choice == '7':
            user_data = user.delete_account(user_data)
            print("Account deleted. Thank you and goodbye!")
            try:
                save_database_product(product_data)
                save_database_user(user_data)
            except NameError:
                pass
            sys.exit()
        elif choice == '8':
            print("Thank you and goodbye!")
            try:
                save_database_product(product_data)
                save_database_user(user_data)
            except NameError:
                pass
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def view_products(product_data):
    print("\nProduct Catalog:")
    print(product_data)

if __name__ == "__main__":
    main()