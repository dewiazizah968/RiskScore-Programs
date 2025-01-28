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

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.username = ""

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

        logo_label = ctk.CTkLabel(self.frame_left, text="Sign In", font=("Tahoma", 45, "bold"), text_color="black")
        logo_label.pack(pady=(80, 2), padx=40, anchor="w")

        header_label = ctk.CTkLabel(self.frame_left, text="Enter your email and password to login.", 
                                    font=("Inter", 17), text_color="#867E7E")
        header_label.pack(pady=(0, 2), padx=40, anchor="w")

        self.create_form_inputs()
        self.create_login_button()

    def create_form_inputs(self):
        # Label dan input username
        username_label = ctk.CTkLabel(
            self.frame_left, text="Username", text_color="#867E7E", font=("Inter", 14, "bold")
        )
        username_label.pack(pady=(20, 2), padx=40, anchor="w")

        self.username_entry = ctk.CTkEntry(self.frame_left, placeholder_text="Username", height=45, width=500, corner_radius=20)
        self.username_entry.pack(pady=(5, 2), padx=38, anchor="w")

        # Label dan input password
        pw_label = ctk.CTkLabel(
            self.frame_left, text="Password", text_color="gray", font=("Inter", 14, "bold")
        )
        pw_label.pack(pady=(20, 2), padx=40, anchor="w")

        self.password_entry = ctk.CTkEntry(
            self.frame_left, placeholder_text="Password", show="*", width=500, height=45, corner_radius=20
        )
        self.password_entry.pack(pady=(5, 8), padx=40, anchor="w")

    def create_login_button(self):
        signup_button = ctk.CTkButton(self.frame_left, text="Login", font=('Inter', 15, 'bold'), fg_color="#464365",
                                      height=45, width=500, corner_radius=20, command=self.login)
        signup_button.pack(pady=50, padx=40, anchor='w')

        signup_label = ctk.CTkLabel(self.frame_left, text="New here? Create an account.", text_color="#4285F4", font=("Inter", 12, "underline", 'bold'), cursor="hand2")
        signup_label.pack(pady=(50, 2), padx=(346, 12), anchor="w")
        signup_label.bind("<Button-1>", lambda e: self.parent.show_signup_page()) 

    def create_right_frame(self):
        frame_right = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        frame_right.pack(side="right", fill="both", expand=True)

        try:
            image = Image.open(os.path.join(base_path, 'Desain DAA', 'iconawal.png'))
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

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username and password:
            try:
                with open(os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "data_users.csv"), mode="r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) < 3:
                            continue
                        kolom_username = row[0].strip()
                        kolom_password = row[2].strip()

                        if kolom_username == username and kolom_password == password:
                            messagebox.showinfo("Login successful!", f"Welcome to RiskScore, {username}! ^___^")
                            self.parent.show_dashboard_page(username)
                            return
                    messagebox.showerror("Login Failed", "Incorrect username or password!")
            except FileNotFoundError:
                messagebox.showerror("Error", "File data_users.csv not found!")
        else:
            messagebox.showerror("Error", "Enter the username and password correctly!")

    def on_close(self):
        self.parent.quit() 

