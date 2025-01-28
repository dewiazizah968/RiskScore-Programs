import customtkinter as ctk
import os
import sys
from signup import SignUpPage
from login import LoginPage
from profilepage import ProfilePage
from dashboard import Dashboard
from input import InputPage
from hasil import HasilPage
from data import DataPage
from detail import DetailPage

# pyinstaller --onefile --windowed --icon=ikon.ico main.py

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else:  
    base_path = os.path.dirname(__file__)

data_path = os.path.join(base_path, 'data.csv')
users_data_path = os.path.join(base_path, 'data_users.csv')
desain_folder = os.path.join(base_path, 'Desain DAA')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_page = None 
        self.title("RiskScore")
        self.geometry("1366x768")
        self.state("zoomed")

        self.signup_page = SignUpPage(self)
        self.signup_page.pack(fill="both", expand=True)
        self.current_page = self.signup_page

        self.login_page = None
        self.profile_page = None
        self.dashboard_page = None
        self.input_page = None
        self.hasil_page = None
        self.data_page = None

    def show_profile_page(self,username):
        """Show the profile page"""
        if self.current_page:
            self.current_page.pack_forget()
        if not self.profile_page:
            self.profile_page = ProfilePage(self,username) 
        self.profile_page.pack(fill="both", expand=True)
        self.current_page = self.profile_page
        
    def show_signup_page(self):
        """Menampilkan halaman SignUp"""
        if self.current_page:
            self.current_page.pack_forget()
        if not self.signup_page:
            self.signup_page = SignUpPage(self)
        self.signup_page.pack(fill="both", expand=True)
        self.current_page = self.signup_page

    def show_login_page(self):
        """Show the login page"""
        if self.current_page:
            self.current_page.pack_forget()
        if not self.login_page:
            self.login_page = LoginPage(self)
        self.login_page.pack(fill="both", expand=True)
        self.current_page = self.login_page

    def show_dashboard_page(self,username):
        """Show the dashboard page"""
        if self.current_page:
            self.current_page.pack_forget()
        if not self.dashboard_page:
            self.dashboard_page = Dashboard(self, username)
        self.dashboard_page.pack(fill="both", expand=True)
        self.current_page = self.dashboard_page

    def show_input_page(self,username):
        """Show the input page"""
        if self.current_page:
            self.current_page.pack_forget()
        if not self.input_page:
            self.input_page = InputPage(self,username)
        self.input_page.pack(fill="both", expand=True)
        self.current_page = self.input_page

    def show_hasil_page(self, user_id, username):
        """Show the result page"""
        if hasattr(self, 'current_page') and self.current_page:
            self.current_page.pack_forget()
        
        if not hasattr(self, 'hasil_page') or not self.hasil_page:
            self.hasil_page = HasilPage(self, username, user_id)
        
        self.hasil_page.pack(fill="both", expand=True)
        self.current_page = self.hasil_page

    def show_data_page(self, username):
        """Show the data page"""
        if hasattr(self, 'current_page') and self.current_page:
            self.current_page.pack_forget()
        
        if not hasattr(self, 'data_page') or not self.data_page:
            self.data_page = DataPage(self, username)
        
        self.data_page.pack(fill="both", expand=True)
        self.current_page = self.data_page  
        self.current_page.reset_selection() 

    def show_detail_page(self, user_id, username):
        """Show the detail page"""
        if hasattr(self, 'current_page') and self.current_page:
            self.current_page.pack_forget()

        self.detail_page = DetailPage(self, username, user_id)

        self.detail_page.pack(fill="both", expand=True)
        self.current_page = self.detail_page

if __name__ == "__main__":
    app = App()
    app.mainloop()
