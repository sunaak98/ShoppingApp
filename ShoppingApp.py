import time
import os
import uuid
import openpyxl as xl
import update_userxl_db as udb

#Display the Welcome Message three times with a blink

for i in range(0,3):
    os.system('clear')
    time.sleep(1)
    print("***************************************")
    print("*** Welcome to the Demo Marketplace ***")
    print("***************************************")
    #provide a delay
    time.sleep(1)


###Creating Databases

#Admin Login Database. In the form of "admin_user_id:admin_password"
admin_db = {"admin1":"admin01","admin2":"admin02"}

#Users login database. In the form of "user_id:user_password"
user_db = {}

#Session ID Storage. Empty list right now.
sessionID = {}

#Relation_ID
r_id = 4

#Creating Classes

#This class adds new user, authenticate them, updates new id or username and delete a user information. It also creates session id for the same user
class user_update():
  #Initialization of the class: constructor
  def __init__(self, username, password,):
    self.username = username
    self.password = password

  #creating new user
  def new_user(self):
    #Authenticating the new username must not exist, else make the new user
    if self.username in user_db:
      print("User Already Exist")
      ans = input("User Already Exist.\n1. Log In\t2. Create Account\t3. Exit")
      if ans == 1:
        user_login(2)
      if ans == 2:
        user_login(1)
      if ans == 3:
        print("Logging Out...")
        time.sleep(3)
        print("THANKYOU FOR VISITING DEMO MARKETPLACE")
        time.sleep(3)
        os.system('clear')      
      time.sleep(3)
      return 1
    else:
      self.session_id = uuid.uuid4()
      user_db[self.username] = [self.password, str(uuid.uuid4())]
      print("Account Created Successfully. ")
      time.sleep(2)
      #print(user_db)
      #print(sessionID)
      return 0

  def auth_user(self):
    if self.username in user_db:
      if self.password in user_db[self.username]:
        print("Authorisation successful")
        time.sleep(3)
      else:
        print("Wrong Password")
        pass_choice = str(input("1. Forgot Password\t2. Re-enter Password:"))

    else:
      ans = str(input("User Does Not Exist. Create Account? [Y/N]: "))
      if ans == "Y" or ans == "y":
        os.system('clear')
        user_login(1)
      if ans == "N" or ans == "n":
        print("Logging Out...")
        time.sleep(3)
        print("THANKYOU FOR VISITING DEMO MARKETPLACE")
        time.sleep(3)
        os.system('clear')

  def remove_user(self):
    if self.username in user_db:
      del user_db[self.username]
      print("User Deleted")
    else:
      print("User Not Found")

  def change_pass(self):
    if self.username in user_db:
      print("User Found")
      self.password = input("Enter New Password: ")
      user_db[self.username]=self.password
      print("Password Updated:")
      print(user_db)
    else:
      print("User Not Found")

  def change_usrnm(self):
    if self.username in user_db:
      print("User Found")
      u_pass = self.password
      del user_db[self.username]
      self.username = input("Enter New Username: ")
      user_db[self.username] = u_pass
      print("Username Updated:")
      print(user_db)
    else:
      print("User Not Found")

# Create Login Page

#User Login Function
def user_login(r_id):
  #Create a new User
  while(r_id is not 0 and r_id is 1):
    time.sleep(1)
    username = input("Enter New Username: ")
    password = input("Enter New Password: ")
    user = user_update(username,password)
    r_id = user.new_user()
    #print(len(user_db))
    #udb.save_new_user("user_db.xlsx", user_db)

  #Login User
  while(r_id is not 0 and r_id is 2):
    time.sleep(1)
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    user = user_update(username,password)
    r_id = user.auth_user()

  while(r_id is not 0 and r_id is 3):
    print("Thanks for visiting us, hope to see you again")
    time.sleep(2)
    r_id = 0
    break



#Customer Page
while(1):
  time.sleep(1)
  print("Please select your relation with us:")
  print("[1] Sign Up\t[2] Sign In\t[3] Exit")
  try:
    r_id = int(input("::"))
    os.system('clear')
  except:
    #r_id = 4
    print("Wrong Choice...")
  if(r_id in [1,2]):
    user_login(r_id)
  if(r_id == 3):
    print("THANKYOU FOR VISITING DEMO MARKETPLACE")
    time.sleep(3)
    os.system('clear')
    break




os.system("clear")