import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import textwrap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else: 
    base_path = os.path.dirname(__file__)

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_close) 

        try:
            bg_image = Image.open(os.path.join(base_path, 'Desain DAA', 'dashboardbg.png'))
            self.bg_image = ctk.CTkImage(light_image=bg_image, size=(1366, 768))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "File gambar background tidak ditemukan.")
        
        self.data = pd.read_csv(os.path.join(base_path, 'data.csv'))

        self.create_dashboard()
        self.add_buttons()

    def create_dashboard(self):
        greeting_label = ctk.CTkLabel(self, text=f"Hello {self.username}!", font=("Tahoma", 50, 'bold'), text_color="#34324A", bg_color='white')
        greeting_label.pack(pady=50, padx=260, anchor="w")

        # Rata-rata jumlah pinjaman
        avg_loan = self.data['jumlah pinjaman'].mean()
        self.avg_loan_score = ctk.CTkLabel(self, text=f"$ {avg_loan:.2f}", font=("Times", 30), bg_color="white")
        self.avg_loan_score.place(x=570, y=280)
        
        # Rata-rata skor risiko kredit
        avg_risk_score = self.data['skor risiko kredit'].mean()
        self.avg_risk_score_label = ctk.CTkLabel(self, text=f"{avg_risk_score:.2f}", font=("Times", 55), bg_color="white")
        self.avg_risk_score_label.place(x=1010, y=265) 
        
        # Bar chart klasifikasi risiko
        risk_counts = self.data['klasifikasi risiko'].value_counts()
        fig, ax = plt.subplots(figsize=(3, 2))
        risk_counts.plot(kind='bar', ax=ax, color='#7873AF')
        fig.patch.set_facecolor('#FFFFFF')
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center')
        self.plot_graph(fig, 280, 470)

        # Pie chart tujuan pinjaman
        loan_purpose_counts = self.data['tujuan pinjaman'].value_counts()
        colors = ['#7873AF', '#8E8ABB', '#CDC8F0', '#8072E4', '#B2AAEF', '#5C4FB8']
        colors_to_use = colors[:len(loan_purpose_counts)]  
        wrapped_labels = [textwrap.fill(label, width=10) for label in loan_purpose_counts.index]
        fig2, ax2 = plt.subplots(figsize=(3, 2))
        ax2.pie(loan_purpose_counts, labels=wrapped_labels, autopct='%1.1f%%', startangle=90, colors=colors_to_use, textprops={'fontsize': 8})
        fig2.patch.set_facecolor('#FFFFFF')
        self.plot_graph(fig2, 620, 470)

        # Stacked bar usia dan jenis kelamin
        gender_age_group = pd.crosstab(self.data['jenis kelamin'], self.data['usia'])
        fig3, ax3 = plt.subplots(figsize=(3, 2)) 
        gender_age_group.T.plot(kind='bar', stacked=True, ax=ax3, color=['#CDC8F0', '#7873AF'])
        fig3.patch.set_facecolor('#FFFFFF') 
        # ax3.set_title("Data Calon Debitur", fontsize=12)
        ax3.tick_params(rotation=0, axis='both', which='major', labelsize=8)
        self.plot_graph(fig3, 970, 470)

    def add_buttons(self):
        button_names = ['profile', 'dashboard', 'input', 'data', 'logout']
        button_images = {
            'profile': "profile.png",
            'dashboard': "dashboardaktif.png",
            'input': "input.png",
            'data': "data.png",
            'logout': "logout.png"
        }

        button_positions = {
            'profile': {'x': 35, 'y': 95, 'width': 50, 'height': 50},
            'logout': {'x': 35, 'y': 640, 'width': 150, 'height': 60}
        }

        y_position = 285
        for name in button_names:
            try:
                img_path = os.path.join(base_path, 'Desain DAA', button_images[name])
                image = Image.open(img_path)

                if name == 'profile': 
                    image_resized = image.resize((140, 140)) 
                elif name == 'logout':  
                    image_resized = image.resize((145, 40))
                else:  
                    image_resized = image.resize((157, 40))  

                button_image = ctk.CTkImage(light_image=image_resized, size=image_resized.size)

                button = ctk.CTkButton(
                    self,
                    image=button_image,
                    text="",
                    command=lambda name=name: self.handle_button_click(name),
                    fg_color="#EAE9F1",
                    bg_color="#EAE9F1",
                    hover_color="#EAE9F1",
                    border_width=1,
                    border_color="#EAE9F1"
                )
                
                if name in button_positions:
                    pos = button_positions[name]
                    button.place(x=pos['x'], y=pos['y'])
                else:
                    button.place(x=25, y=y_position)
                    y_position += 65  

            except FileNotFoundError:
                messagebox.showerror("Error", f"File gambar tombol {name} tidak ditemukan.")

    def handle_button_click(self, button_name):
        if button_name == 'dashboard':
            self.parent.show_dashboard_page(self.username)
        elif button_name == 'input':
            self.parent.show_input_page(self.username)
        elif button_name == 'data':
            self.parent.show_data_page(self.username)
        elif button_name == 'profile':
            self.parent.show_profile_page(self.username)
        elif button_name == 'logout':
            self.on_close()  
        else:
            messagebox.showinfo("Info", f"Button {button_name} not implemented.")

    def plot_graph(self, fig, x_pos, y_pos):
        canvas = FigureCanvasTkAgg(fig, master=self)  
        canvas.draw()
        canvas.get_tk_widget().place(x=x_pos, y=y_pos)

    def on_close(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
            messagebox.showinfo("Logout", "You have successfully logged out")
            self.parent.quit()