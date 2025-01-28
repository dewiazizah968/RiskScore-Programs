from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import csv
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else:  
    base_path = os.path.dirname(__file__)

class HasilPage(ctk.CTkFrame):
    def __init__(self, parent, username, user_id=None):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.user_id = user_id

        # Background Image
        try:
            bg_image = Image.open(os.path.join(base_path, 'Desain DAA', 'hasilbg.png'))
            self.bg_image = ctk.CTkImage(light_image=bg_image, size=(1366, 768))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "File gambar background tidak ditemukan.")

        # Load Data from CSV
        self.latest_data = self.load_latest_data()

        self.display_latest_data()
        self.add_buttons()

    def load_latest_data(self):
        file_path = os.path.join(base_path, 'data.csv')
        latest_entry = None

        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  
                for row in reader:
                    latest_entry = row 
        except FileNotFoundError:
            messagebox.showerror("Error", "File CSV tidak ditemukan.")
        
        return latest_entry

    def display_latest_data(self):
        if not self.latest_data:
            messagebox.showinfo("Error", "Data tidak ditemukan di file CSV.")
            return

        user_id, nama, _, _, _, _, _, _, _, _, _, _, _, total_risk_score, risk_level, decision = self.latest_data

        # ID dan Nama Calon Debitur
        id_label = ctk.CTkLabel(self, text=f"ID Calon Debitur: {user_id}", font=("Times", 20), text_color="black", bg_color="#EAE9F1")
        id_label.place(x=260, y=170)

        nama_label = ctk.CTkLabel(self, text=f"Nama Calon Debitur: {nama}", font=("Times", 20), text_color="black", bg_color="#EAE9F1")
        nama_label.place(x=260, y=200)

        # Skor Risiko Kredit
        skor_label = ctk.CTkLabel(self, text=f"{total_risk_score}",
                                font=("Times", 100), text_color="black", bg_color="#EFEFEF", wraplength=500)
        skor_label.place(x=370, y=350)

        # Klasifikasi Risiko
        classification_desc = {
            "Rendah": "Risiko kredit rendah aman untuk disetujui.",
            "Sedang": "Risiko kredit sedang perlu evaluasi lebih lanjut.",
            "Tinggi": "Risiko kredit tinggi perlu pertimbangan mendalam."
        }
        risk_title_label = ctk.CTkLabel(self, text=risk_level,
                                font=("Times", 50, "bold"), text_color="black", bg_color="#EFEFEF")
        risk_title_label.place(x=690, y=350)

        # Deskripsi Risiko
        risk_desc_label = ctk.CTkLabel(self, text=classification_desc.get(risk_level, ""),
                                    font=("Times", 20), text_color="black", bg_color="#EFEFEF", wraplength=200)
        risk_desc_label.place(x=690, y=450)

        # Keputusan
        decision_desc = {
            "Approve": "Anda dapat menyetujui calon debitur ini.",
            "Review Manually": "Perlu pemeriksaan lebih lanjut sebelum keputusan akhir.",
            "Reject": "Pinjaman ditolak. Hubungi calon peminjam untuk klarifikasi."
        }

        decision_title_label = ctk.CTkLabel(self, text=decision,
                                            font=("Times", 50, "bold"), text_color="black", bg_color="#EFEFEF", wraplength=250)
        decision_title_label.place(x=1040, y=350)

        if decision == "Review Manually":
            y_position = 500
        else:
            y_position = 450

        # Deskripsi Keputusan
        decision_desc_label = ctk.CTkLabel(self, text=decision_desc.get(decision, ""),
                                        font=("Times", 20), text_color="black", bg_color="#EFEFEF", wraplength=200)
        decision_desc_label.place(x=1040, y=y_position)

    def add_buttons(self):
        button_names = ['profile', 'dashboard', 'input', 'data', 'logout']
        button_images = {
            'profile': "profile.png",
            'dashboard': "dashboard.png",
            'input': "inputaktif.png",
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