import pandas as pd
from datetime import datetime
from uuid import uuid4
import os
import sys

# Product categories
PRODUCT_CATEGORIES = ['Shoes', 'T-Shirts', 'Caps', 'Bags']

# Excel file names
PRODUCT_CATALOG_FILE = 'product_catalog.xlsx'
LOGIN_CREDENTIALS_FILE = 'login_credentials.xlsx'

# Clear console function (compatible with Windows and Mac OS)
def clear_console():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

# Load product catalog from Excel sheet
try:
    product_catalog = pd.read_excel(PRODUCT_CATALOG_FILE)
    # Filter product catalog to only include the desired categories
    product_catalog = product_catalog[product_catalog['category'].isin(PRODUCT_CATEGORIES)]
except FileNotFoundError:
    print(f"'{PRODUCT_CATALOG_FILE}' not found. Creating a new file.")
    product_catalog = pd.DataFrame(columns=['product_id', 'product_name', 'category', 'price'])
    product_catalog.to_excel(PRODUCT_CATALOG_FILE, index=False)

# Load user and admin login credentials from Excel sheet
try:
    login_credentials = pd.read_excel(LOGIN_CREDENTIALS_FILE)
    login_credentials = login_credentials._append({'email': 'Admin1', 'password': 'Admin123', 'role': 'admin'}, ignore_index=True) 
except FileNotFoundError:
    print(f"'{LOGIN_CREDENTIALS_FILE}' not found. Creating a new file.")
    login_credentials = pd.DataFrame(columns=['email', 'password', 'role'])
    #adding admin access by default
    login_credentials = login_credentials._append({'email': 'Admin1', 'password': 'Admin123', 'role': 'admin'}, ignore_index=True) 
    login_credentials.to_excel(LOGIN_CREDENTIALS_FILE, index=False)

# Main loop
while True:
    clear_console()
    print("Welcome to the Demo Marketplace")

    # Sign-up or login
    while True:
        action = input("Do you want to sign up, login, or delete your account? (sign up/login/delete) ").lower()
        if action == 'sign up':
            user_email = input("Enter your email: ")
            user_password = input("Enter your password: ")
            if (login_credentials[(login_credentials['email'] == user_email)]).empty:
                login_credentials = login_credentials._append({'email': user_email, 'password': user_password, 'role': 'user'}, ignore_index=True)
                user_session_id = str(uuid4())
                print(f"Your session ID is: {user_session_id}")
                action = 'login'
                #break
            else:
                print("User already exists. Please login.")
                action = 'login'
        if action == 'login':
            print("Enter your credentials:\n")
            user_email = input("Enter your email: ")
            user_password = input("Enter your password: ")
            if (login_credentials[(login_credentials['email'] == user_email) & (login_credentials['password'] == user_password) & (login_credentials['role'] == 'admin')]).empty:
                if (login_credentials[(login_credentials['email'] == user_email) & (login_credentials['password'] == user_password) & (login_credentials['role'] == 'user')]).empty:
                    print("User not found. Do you want to sign up? (y/n)")
                    create_account = input().lower()
                    if create_account == 'y':
                        continue
                    else:
                        print("Goodbye!")
                        login_credentials.to_excel(LOGIN_CREDENTIALS_FILE, index=False)
                        product_catalog.to_excel(PRODUCT_CATALOG_FILE, index=False)
                        exit()
                else:
                    print("User login successful!")
                    user_session_id = str(uuid4())
                    print(f"Your session ID is: {user_session_id}")
                    break
            else:
                print("Admin login successful!")
                admin_session_id = str(uuid4())
                admin_credentials = {'username': 'Admin1', 'password': 'Admin123', 'session_id': admin_session_id}
                print(f"Your session ID is: {admin_session_id}")
                break
        if action == 'delete':
            while True:
                count = 0
                if count<3:
                    user_email = input("Enter your email: ")
                    user_password = input("Enter your password: ")
                    if (login_credentials[(login_credentials['email'] == user_email) & (login_credentials['password'] == user_password) & (login_credentials['role'] == 'user')]).empty:
                        print("User not found. Please try again.")
                        count += 1
                        continue
                    else:
                        login_credentials = login_credentials[~(login_credentials['email'] == user_email)]
                        print("Your account has been deleted.")
                        login_credentials.to_excel(LOGIN_CREDENTIALS_FILE, index=False)
                        product_catalog.to_excel(PRODUCT_CATALOG_FILE, index=False)
                        exit()
            exit()
        else:
            print("Invalid input. Please try again.")

    # Admin functions
    if 'admin_credentials' in locals():
        while True:
            clear_console()
            admin_choice = input("\nAdmin menu:\n1. Add new product\n2. Update existing product\n3. Remove product\n4. Add new category\n5. Remove category\n6. Exit\nEnter your choice: ")
            if admin_choice == '1':
                new_product_name = input("Enter new product name: ")
                new_product_category = input("Enter product category: ")
                if new_product_category not in PRODUCT_CATEGORIES:
                    print(f"Invalid category. Allowed categories are: {', '.join(PRODUCT_CATEGORIES)}")
                    continue
                new_product_price = float(input("Enter product price: "))
                new_product_id = product_catalog['product_id'].max() + 1
                product_catalog = product_catalog.append({'product_id': new_product_id, 'product_name': new_product_name, 'category': new_product_category, 'price': new_product_price}, ignore_index=True)
                print(f"New product '{new_product_name}' added to the catalog.")
            elif admin_choice == '2':
                product_id = int(input("Enter product ID to update: "))
                product = product_catalog[product_catalog['product_id'] == product_id]
                if product.empty:
                    print("Invalid product ID.")
                    continue
                new_product_name = input(f"Enter new name (current: {product['product_name'].values[0]}): ")
                new_product_category = input(f"Enter new category (current: {product['category'].values[0]}): ")
                if new_product_category not in PRODUCT_CATEGORIES:
                    print(f"Invalid category. Allowed categories are: {', '.join(PRODUCT_CATEGORIES)}")
                    continue
                new_product_price = float(input(f"Enter new price (current: {product['price'].values[0]}): "))
                product_catalog.loc[product_catalog['product_id'] == product_id, ['product_name', 'category', 'price']] = [new_product_name, new_product_category, new_product_price]
                print(f"Product '{product['product_name'].values[0]}' updated.")
            elif admin_choice == '3':
                product_id = int(input("Enter product ID to remove: "))
                product = product_catalog[product_catalog['product_id'] == product_id]
                if product.empty:
                    print("Invalid product ID.")
                    continue
                product_catalog = product_catalog[product_catalog['product_id'] != product_id]
                print(f"Product '{product['product_name'].values[0]}' removed from the catalog.")
            elif admin_choice == '4':
                new_category = input("Enter new category name: ")
                if new_category in PRODUCT_CATEGORIES:
                    print("Category already exists.")
                    continue
                PRODUCT_CATEGORIES.append(new_category)
                product_catalog = product_catalog._append({'product_id': product_catalog['product_id'].max() + 1, 'product_name': 'New Product', 'category': new_category, 'price': 0.0}, ignore_index=True)
                print(f"New category '{new_category}' added to the catalog.")
            elif admin_choice == '5':
                category_to_remove = input("Enter category to remove: ")
                if category_to_remove not in PRODUCT_CATEGORIES:
                    print("Category does not exist.")
                    continue
                PRODUCT_CATEGORIES.remove(category_to_remove)
                product_catalog = product_catalog[product_catalog['category'] != category_to_remove]
                print(f"Category '{category_to_remove}' removed from the catalog.")
            elif admin_choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    # User functions
    else:
        while True:
            clear_console()
            user_choice = input("\nUser menu:\n1. Change password\n2. View product catalog\n3. Add to cart\n4. Checkout\n5. Exit\nEnter your choice: ")
            if user_choice == '1':
                new_password = input("Enter your new password: ")
                login_credentials.loc[login_credentials['email'] == user_email, 'password'] = new_password
                print("Password updated successfully.")
            elif user_choice == '2':
                print("\nProduct Catalog:")
                print(product_catalog[['product_id', 'product_name', 'category', 'price']])
            elif user_choice == '3':
                cart = []
                while True:
                    add_item = input("Enter product ID to add to cart (or 'q' to checkout): ")
                    if add_item.lower() == 'q':
                        break
                    try:
                        product = product_catalog[product_catalog['product_id'] == int(add_item)]
                        if product.empty:
                            print("Invalid product ID. Please try again.")
                            continue
                        quantity = int(input(f"Enter quantity for {product['product_name'].values[0]}: "))
                        cart.append({'product_id': int(add_item), 'product_name': product['product_name'].values[0], 'quantity': quantity, 'price': product['price'].values[0]})
                        print(f"{quantity} x {product['product_name'].values[0]} added to cart.")
                    except ValueError:
                        print("Invalid input. Please enter a valid product ID or 'q' to checkout.")
            elif user_choice == '4':
                total_cart_value = sum([item['quantity'] * item['price'] for item in cart])
                print(f"\nTotal cart value: Rs. {total_cart_value}")
                payment_method = input("Select payment method (Net Banking, PayPal, UPI): ")
                if payment_method.lower() == 'upi':
                    print(f"You will be shortly redirected to the portal for Unified Payment Interface to make a payment of Rs. {total_cart_value}")
                else:
                    print("Your order is successfully placed.")
            elif user_choice == '5':
                login_credentials.to_excel(LOGIN_CREDENTIALS_FILE, index=False)
                product_catalog.to_excel(PRODUCT_CATALOG_FILE, index=False)
                break
            else:
                print("Invalid choice. Please try again.")