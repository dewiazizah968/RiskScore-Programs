import csv
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else:  
    base_path = os.path.dirname(__file__)

class DetailPage(ctk.CTkFrame):
    def __init__(self, parent, username, user_id=None):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.user_id = user_id
        self.data = None

        try:
            bg_image = Image.open(os.path.join(base_path, 'Desain DAA', 'detailbg.png'))
            self.bg_image = ctk.CTkImage(light_image=bg_image, size=(1366, 768))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "File gambar background tidak ditemukan.")

        self.user_id = user_id
        self.data = None

        self.add_buttons()
        self.load_detail_data()
        self.display_details()

    def load_detail_data(self):
        self.data = None
        try:
            with open(os.path.join(base_path, 'data.csv'), "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["id"] == self.user_id:
                        self.data = row
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "File data.csv tidak ditemukan.")

    def display_details(self):
        if not self.data:
            messagebox.showerror("Error", "Data tidak ditemukan untuk ID ini.")
            return

        y_position = 180

        positions_and_widths = [
            (320, y_position, 30),   # ID
            (420, y_position, 200),  # Nama
            (320, y_position + 100, 30),   # Usia
            (420, y_position + 100, 150),  # Jenis Kelamin

            (320, y_position + 200, 200),   # Pendapatan Tahunan
            (640, y_position + 200, 150),   # Lama Bekerja
            (900, y_position + 200, 160),  # Kepemilikan Rumah
            (320, y_position + 300, 160),   # Jumlah Pinjaman

            (550, y_position + 300, 160),   # Tujuan Pinjaman
            (780, y_position + 300, 160),   # Lama Pinjaman
            (1010, y_position + 300, 160),   # Persentase Pendapatan Pinjaman
            (640, y_position + 100, 160),   # Email

            (870, y_position + 100, 100),   # Kontak
            (320, y_position + 400, 200),   # Skor Risiko Kredit
            (645, y_position + 400, 200),   # Klasifikasi Risiko
            (970, y_position + 400, 200),  # Keputusan
        ]

        labels = [
            ("ID", "id"),
            ("Nama", "nama"),
            ("Usia", "usia"),
            ("Jenis Kelamin", "jenis kelamin"),
            ("Pendapatan Tahunan", "pendapatan tahunan"),
            ("Lama Bekerja", "lama bekerja"),
            ("Kepemilikan Rumah", "kepemilikan rumah"),
            ("Jumlah Pinjaman", "jumlah pinjaman"),
            ("Tujuan Pinjaman", "tujuan pinjaman"),
            ("Lama Pinjaman", "lama pinjaman"),
            ("Persentase (LIP)", "persentase pendapatan pinjaman"),
            ("Email", "email"),
            ("Kontak", "kontak"),
            ("Skor Risiko Kredit", "skor risiko kredit"),
            ("Klasifikasi Risiko", "klasifikasi risiko"),
            ("Keputusan", "keputusan"),
        ]

        for i, (label_text, key) in enumerate(labels):
            value = self.data.get(key, "-")

            if key in ["usia", "lama bekerja", "lama pinjaman"] and value.isdigit():
                value += " tahun"

            if key in ["pendapatan tahunan", "jumlah pinjaman"] and value.isdigit():
                value = f"$ {value}"
            
            x_position, y_pos, width = positions_and_widths[i]

            label = ctk.CTkLabel(self, text=f"{label_text}:", anchor="w", width=width, fg_color="#FFFFFF", bg_color="#fff", corner_radius=8, font=("Arial", 18, "bold"))
            label.place(x=x_position, y=y_pos)

            value_label = ctk.CTkLabel(self, text=value, anchor="center", width=width + 50, fg_color="#EAE9F1", bg_color="#fff", corner_radius=8, font=("Arial", 15))
            value_label.place(x=x_position, y=y_pos + 30)

        # Tombol kembali
        back_button = ctk.CTkButton(self, text="Back",font=("Arial", 14, "bold"), command=self.back_to_data_page, width=100, height=30, corner_radius=30, bg_color="#FFFFFF", fg_color="#ACA7D1", text_color="#34324A")
        back_button.place(x=1150, y=180)

    def back_to_data_page(self):
        self.parent.show_data_page(self.username)

    def add_buttons(self):
        button_names = ['profile', 'dashboard', 'input', 'data', 'logout']
        button_images = {
            'profile': "profile.png",
            'dashboard': "dashboard.png",
            'input': "input.png",
            'data': "dataaktif.png",
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
                    image_resized = image.resize((157, 44)) 

                button_image = ctk.CTkImage(light_image=image_resized, size=image_resized.size)

                button = ctk.CTkButton(
                    self,
                    image=button_image,
                    text="",
                    command=lambda name=name: self.handle_button_click(name),
                    fg_color="#EAE9F1",
                    bg_color="#EAE9F1",
                    hover_color="#EAE9F1"
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

    def on_close(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if response:
            messagebox.showinfo("Logout", "You have successfully logged out")
            self.parent.quit()