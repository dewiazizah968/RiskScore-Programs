import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from tkinter import messagebox
import csv
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else:  
    base_path = os.path.dirname(__file__)

class SignUpPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.parent.geometry("1278x650")
        self.parent.title("RiskScore SignUp")
        self.parent.configure(bg="#EAE9F1")

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.pack(fill="both", expand=True)

        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        self.frame_left = ctk.CTkFrame(self, corner_radius=0, fg_color="#EAE9F1")
        self.frame_left.pack(side="left", fill="both", expand=True)

        logo_label = ctk.CTkLabel(self.frame_left, text="Sign Up", font=("Tahoma", 45, "bold"), text_color="black")
        logo_label.pack(pady=(80, 2), padx=40, anchor="w")

        header_label = ctk.CTkLabel(self.frame_left, text="Enter your username, email and password to register.", 
                                    font=("Inter", 17), text_color="#867E7E")
        header_label.pack(pady=(0, 2), padx=40, anchor="w")

        self.create_form_inputs()
        self.create_sign_up_button()

    def create_form_inputs(self):
        username_label = ctk.CTkLabel(self.frame_left, text="Username", text_color="#867E7E", font=("Inter", 14, "bold"))
        username_label.pack(pady=(20, 2), padx=40, anchor="w")

        self.uname_entry = ctk.CTkEntry(self.frame_left, placeholder_text="username", height=45, width=500, corner_radius=20)
        self.uname_entry.pack(pady=(5, 2), padx=38, anchor="w")

        email_label = ctk.CTkLabel(self.frame_left, text="Email", text_color="#867E7E", font=("Inter", 14, "bold"))
        email_label.pack(pady=(20, 2), padx=40, anchor="w")

        self.email_entry = ctk.CTkEntry(self.frame_left, placeholder_text="example@gmail.com", height=45, width=500, corner_radius=20)
        self.email_entry.pack(pady=(5, 2), padx=38, anchor="w")

        pw_label = ctk.CTkLabel(self.frame_left, text="Password", text_color="gray", font=("Inter", 14, "bold"))
        pw_label.pack(pady=(20, 2), padx=40, anchor="w")

        self.password_entry = ctk.CTkEntry(self.frame_left, placeholder_text="password", show="*", width=500, height=45, corner_radius=20)
        self.password_entry.pack(pady=(5, 8), padx=40, anchor="w")

    def create_sign_up_button(self):
        signup_button = ctk.CTkButton(self.frame_left, text="Sign Up", font=('Inter', 15, 'bold'), fg_color="#464365",
                                      height=45, width=500, corner_radius=20, command=self.signup)
        signup_button.pack(pady=20, padx=40, anchor='w')

        # desc_label = ctk.CTkLabel(self.frame_left, text="Already have an account?", text_color="black", font=("Inter", 12, 'bold'))
        # desc_label.pack(pady=(10, 2), padx=(346, 12), anchor="w")

        signin_label = ctk.CTkLabel(self.frame_left, text="Already have an account? Sign In.", text_color="#4285F4", font=("Inter", 12, "underline", 'bold'), cursor="hand2")
        signin_label.pack(pady=(10, 2), padx=(346, 12), anchor="w")
        signin_label.bind("<Button-1>", lambda e: self.parent.show_login_page())

    def create_right_frame(self):
        frame_right = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        frame_right.pack(side="right", fill="both", expand=True)

        try:
            image = Image.open(os.path.join(base_path, "Desain DAA", "iconawal.png"))
            ctk_image = CTkImage(dark_image=image, size=(500, 550))
            image_label = ctk.CTkLabel(frame_right, image=ctk_image, text="")
            image_label.pack(padx=100)
        except Exception as e:
            error_label = ctk.CTkLabel(frame_right, text="Image not found", text_color="red")
            error_label.pack(pady=(50, 20))

        text_label1 = ctk.CTkLabel(frame_right, text="RiskScore", font=("Tahoma", 30, 'bold'), text_color="black", justify="left")
        text_label1.pack(pady=(0, 0), padx=20, anchor="w")

        text_label2 = ctk.CTkLabel(frame_right, text="Managing Risks, Securing Decisions.", font=("Inter", 25, 'bold'), text_color="black", justify="left")
        text_label2.pack(pady=(10, 2), padx=20, anchor="w")

        text_label3 = ctk.CTkLabel(frame_right, text="Robust system designed to assess and manage risk, empowering \nbusinesses and individuals to make safer, more informed decisions.", 
                                   font=("Inter", 19), text_color="black", justify="left")
        text_label3.pack(pady=10, padx=20, anchor="w")

    def signup(self):
        username = self.uname_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and email and password:
            if not self.validasi_email(email):
                messagebox.showerror("Error", "Invalid email format!")
                return

            if self.is_email_registered(email):
                messagebox.showerror("Error", "Email is registered!")
                return

            self.save_user_data(username, email, password)
            messagebox.showinfo("Sign Up", "Account has been successfully created! Please log in! ^___^")
            self.parent.show_login_page()
        else:
            messagebox.showerror("Error", "Enter the username, email and password correctly!")

    def is_email_registered(self, email):
        try:
            with open(os.path.join(base_path, "data_users.csv"), mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2 and row[1].strip() == email:
                        return True
        except FileNotFoundError:
            pass
        return False

    def save_user_data(self, username, email, password):
        with open(os.path.join(base_path, "data_users.csv"), mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password])

    def validasi_email(self, email):
        return "@" in email and "." in email
    
    def on_close(self):
        self.parent.quit() 
 