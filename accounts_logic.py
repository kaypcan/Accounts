from PyQt6 import *
from PyQt6.QtWidgets import *
from accounts_gui import *
from accounts_gui import Ui_AccountsMainWindow
import csv

class Logic(QDialog, Ui_AccountsMainWindow):
    def __init__(self):
        """
        Sets up UI, gives functions to every button on the screen
        """
        super().__init__()
        self.setupUi(self)

        self.loginButton.clicked.connect(lambda: self.login())
        self.withdrawButton.clicked.connect(lambda: self.withdraw())
        self.depositButton.clicked.connect(lambda: self.deposit())
        self.logoutButton.clicked.connect(lambda: self.logout())

    def login(self) -> None:
        """
        Checks if username and password match to log user in; if yes, displays info, if no, gives error message
        :return: None
        """
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        username_match = False
        logged_in = False

        with open('bank_account_info.csv', 'r', newline = '') as account_info:
            csv_reader = csv.reader(account_info, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                if row[1] == username:
                    username_match = True
                    self.__username = row[1]
                    self.__name = row[0]
                    if row[2] == password:
                        logged_in = True
                        self.__password = row[2]
                        self.nameDisplay.setText(f'Welcome back, {row[0]}!')
                        self.display_info()

            if logged_in == False and username_match == False:
                self.messageDisplay.setText('Incorrect username - please try again')
                self.usernameInput.clear()
                self.passwordInput.clear()
            elif logged_in == False:
                self.messageDisplay.setText('Incorrect password - please try again')
                self.passwordInput.clear()

    def display_info(self) -> None:
        """
        Displays user account info; if savings account, shows savings info
        :return: None
        """
        with open('bank_account_info.csv', 'r', newline = '') as account_info:
            csv_reader = csv.reader(account_info, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                if row[1] == self.usernameInput.text():
                    if row[4] == 'True':
                        self.__savings_account = True
                        self.savingsDisplay.setText('SAVINGS ACCOUNT')
                        self.__minimum = float(row[5])
                        self.__rate = float(row[6])
                        self.__deposit_count = 0
                    else:
                        self.__savings_account = False

                self.__balance = float(row[3])
                self.balanceDisplay.setText(f'$\t{self.__balance}')

                self.messageDisplay.setText('')

    def withdraw(self) -> None:
        """
        Allows user to withdraw input amount from account; gives error if amount is outside allowed range
        :return: None
        """
        try:
            try:
                withdrawal_amount = float(self.withdrawInput.text())

                if self.__savings_account == True:
                    if withdrawal_amount > 0 and withdrawal_amount <= self.__minimum:
                        self.__balance -= withdrawal_amount
                    else:
                        self.messageDisplay.setText('Invalid value - decreases balance below savings minimum')
                elif withdrawal_amount > 0 and withdrawal_amount <= self.__balance:
                    self.__balance -= withdrawal_amount
                    Logic.change_balance(self)
                else:
                    self.messageDisplay.setText('Invalid value - cannot be more than account balance')

                self.balanceDisplay.setText(f'$\t{self.__balance}')
                self.withdrawInput.clear()

            except ValueError:
                self.messageDisplay.setText('Invalid value - enter only digits')

        except AttributeError:
            self.messageDisplay.setText('Log in to account before withdrawal')

    def deposit(self) -> None:
        """
        Allows user to deposit input amount in account; gives error if amount is outside allowed range
        :return: None
        """
        try:
            try:
                deposit_amount = float(self.depositInput.text())

                if deposit_amount > 0:
                    self.__balance += deposit_amount
                    self.__deposit_count += 1
                    if self.__deposit_count % 5 == 0:
                        self.__balance *= (1 + self.__rate)
                    Logic.change_balance(self)
                else:
                    self.messageDisplay.setText('Invalid value - cannot be less than zero')

                self.balanceDisplay.setText(f'$\t{self.__balance}')
                self.depositInput.clear()

            except ValueError:
                self.messageDisplay.setText('Invalid value - enter only digits')

        except AttributeError:
            self.messageDisplay.setText('Log in to account before withdrawal')

    def logout(self) -> None:
        """
        Clears out all saved and displayed user data to log out
        :return: None
        """
        del self.__username
        del self.__password
        del self.__balance
        del self.__name

        if self.__savings_account == True:
            del self.__rate
            del self.__minimum
            del self.__savings_account
            del self.__deposit_count

        self.balanceDisplay.setText('')
        self.usernameInput.clear()
        self.passwordInput.clear()
        self.messageDisplay.setText('')
        self.savingsDisplay.setText('')
        self.nameDisplay.setText('')
        self.withdrawInput.clear()
        self.depositInput.clear()
        self.usernameInput.setFocus()

    def change_balance(self) -> None:
        """
        Adjusts balance and saves new user info, with adjusted balance, to csv file
        :return: None
        """
        with open('bank_account_info.csv', 'w') as account_info_write:
            csv_writer = csv.writer(account_info_write, delimiter = ',')
            with open('bank_account_info_copy.csv', 'r') as account_info_read:
                csv_reader = csv.reader(account_info_read, delimiter = ',')
                for row in csv_reader:
                    if row[1] != self.__username:
                        csv_writer.writerow(row)
        with open('bank_account_info.csv', 'a') as account_info_append:
            csv_appender = csv.writer(account_info_append, delimiter = ',')
            csv_appender.writerow([self.__name, self.__username, self.__password, self.__balance, self.__savings_account, self.__minimum, self.__rate])

        with open('bank_account_info.csv', 'r') as account_info_read:
            csv_reader = csv.reader(account_info_read, delimiter = ',')
            with open('bank_account_info_copy.csv', 'w') as account_info_write:
                csv_writer = csv.writer(account_info_write, delimiter = ',')
                for row in csv_reader:
                    csv_writer.writerow(row)
