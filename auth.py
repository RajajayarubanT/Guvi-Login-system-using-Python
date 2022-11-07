
import pandas as pd
import re
from csv import writer


class Auth:
        
    def __init__(self) -> None:
        
        self.email_reg = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.password_reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        self.db_path = "./data.csv"

    def getemail(self):

        email = str(input("Enter E-mail address (ex123@ex.com) : "))

        if self.check_reg(self.email_reg, email):
            return email
        else:
            print('Invalid Email Format')
            return self.getemail()

    def getpass(self):

        email = str(input("Enter Password (Ex#1234): "))

        if self.check_reg(self.password_reg, email):
            return email
        else:
            print('Invalid Password Format')
            return self.getpass()

    def check_reg(self, valid, email):
    
        if(re.fullmatch(valid, email)):
            return True 
        else:
            return False

    def register(self):

        name = str(input("Enter a Name : "))
        email = self.getemail()
        password = self.getpass()
        exist_user = self.check_user_email(email)

        if exist_user:
            print('User Already Exist, Please Login!')
            self.login()

        else:
            self.create_new_user(name, email, password)
            print('User Registered Successfully')

    def login(self):

        email = self.getemail()
        password = self.getpass()

        exist_user = self.check_user_logined(email)

        if exist_user=="no":

            verify_pass = self.check_user_password(password)

            if verify_pass:

                res = self.update_user_logined(email)

                if res:
                    print('User Logged In Successfully')
                else:
                    print('Something went wrong, Please try again')
                    self.login()

            else:
                print('Password Not Match, Please Login with valid details!')
                self.login()

        elif exist_user == "yes":
            print('User Already Logged In')

        elif exist_user == False:

            print('User not exist, Please Register!')
            self.register()

    def check_user_logined(self, email):

        db = pd.read_csv(self.db_path, sep=",")

        dataPF = db.query('email =="'+ email+'"')

        user = dataPF['email']

        if user.count():
            _index = dataPF['islogined'].index[0]
            return dataPF['islogined'][_index]
        else:
            return False

    def update_user_logined(self, email):

        db = pd.read_csv(self.db_path, sep=",")

        dataPF = db.query('email =="'+ email+'"')

        user = dataPF['email']

        if user.count():
        
            _index = user.index[0]
            db.loc[_index, 'islogined'] = "yes"
            db.to_csv(self.db_path, index=False)
            return True

        else:
            return False

    def create_new_user(self, name, email, password):

        with open(self.db_path, 'a+', newline='') as db:

            new_user = [name, email, password, 'no']

            db_writer = writer(db)
            res =db_writer.writerow(new_user)
            db.close()

    def check_user_email(self, email):

        db = pd.read_csv(self.db_path, sep=",")

        dataPF = db.query('email =="'+ email+'"')

        return dataPF['email'].count()

    def check_user_password(self, _pass):

        db = pd.read_csv(self.db_path, sep=",")

        dataPF = db.query('password =="'+ _pass+'"')

        return dataPF['password'].count()

    def init(self):

        isUser = str(input("Aleady have a account?")).lower()

        if isUser[0] == 'y':
            self.login()
        elif isUser[0] == 'n':
            self.register()
        else:
            print('Invalid user Input')


if __name__ == '__main__':
    
    auth = Auth()
    
    auth.init()
    

