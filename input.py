from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
import csv
import re
import random
import os
import numpy as np
import pandas as pd
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else:  
    base_path = os.path.dirname(__file__)

class InputPage(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.parent = parent
        self.username = username

        try:
            bg_image = Image.open(os.path.join(base_path, 'Desain DAA', 'inputbg.png'))
            self.bg_image = ctk.CTkImage(light_image=bg_image, size=(1366, 768))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "File gambar background tidak ditemukan.")

        self.ensure_csv_exists()
        self.add_buttons()
        self.entries = []

        # Nama
        nama_label = ctk.CTkLabel(self, text="Nama:", bg_color="white")
        nama_label.place(x=310, y=220)
        self.nama_entry = ctk.CTkEntry(self, width=300, bg_color="white")
        self.nama_entry.place(x=310, y=250)
        self.entries.append(self.nama_entry)

        # Usia
        usia_label = ctk.CTkLabel(self, text="Usia:", bg_color="white")
        usia_label.place(x=680, y=220)
        self.usia_entry = ctk.CTkEntry(self, width=200, bg_color="white")
        self.usia_entry.place(x=680, y=250)
        self.entries.append(self.usia_entry)

        # Jenis Kelamin
        jenis_kelamin_label = ctk.CTkLabel(self, text="Jenis Kelamin:", bg_color="white")
        jenis_kelamin_label.place(x=1030, y=220)
        self.jenis_kelamin_dropdown = ctk.CTkComboBox(self, values=["Male", "Female"], width=200, bg_color="white")
        self.jenis_kelamin_dropdown.place(x=1030, y=250)

        # Pendapatan Tahunan
        pendapatan_label = ctk.CTkLabel(self, text="Pendapatan Tahunan ($):", bg_color="white")
        pendapatan_label.place(x=310, y=300)
        self.pendapatan_entry = ctk.CTkEntry(self, width=200, bg_color="white")
        self.pendapatan_entry.place(x=310, y=330)
        self.entries.append(self.pendapatan_entry)

        # Lama Bekerja
        lama_bekerja_label = ctk.CTkLabel(self, text="Lama Bekerja (tahun):", bg_color="white")
        lama_bekerja_label.place(x=680, y=300)
        self.lama_bekerja_entry = ctk.CTkEntry(self, width=200, bg_color="white")
        self.lama_bekerja_entry.place(x=680, y=330)
        self.entries.append(self.lama_bekerja_entry)

        # Kepemilikan Rumah
        rumah_label = ctk.CTkLabel(self, text="Kepemilikan Rumah:", bg_color="white")
        rumah_label.place(x=1030, y=300)
        self.rumah_dropdown = ctk.CTkComboBox(self, values=["Mortgage", "Rent", "Own", "Other"], width=200, bg_color="white")
        self.rumah_dropdown.place(x=1030, y=330)

        # Jumlah Pinjaman
        jumlah_pinjaman_label = ctk.CTkLabel(self, text="Jumlah Pinjaman ($):", bg_color="white")
        jumlah_pinjaman_label.place(x=310, y=380)
        self.jumlah_pinjaman_entry = ctk.CTkEntry(self, width=200, bg_color="white")
        self.jumlah_pinjaman_entry.place(x=310, y=410)
        self.entries.append(self.jumlah_pinjaman_entry)

        # Tujuan Pinjaman
        tujuan_label = ctk.CTkLabel(self, text="Tujuan Pinjaman:", bg_color="white")
        tujuan_label.place(x=680, y=380)
        self.tujuan_dropdown = ctk.CTkComboBox(self, values=["Debt Consolidation", "Education", "Medical", 
                                                             "Personal", "Venture", "Home Improvement"], width=200, bg_color="white")
        self.tujuan_dropdown.place(x=680, y=410)

        # Lama Pinjaman
        lama_pinjaman_label = ctk.CTkLabel(self, text="Lama Pinjaman (tahun):", bg_color="white")
        lama_pinjaman_label.place(x=1030, y=380)
        self.lama_pinjaman_entry = ctk.CTkEntry(self, width=200, bg_color="white")
        self.lama_pinjaman_entry.place(x=1030, y=410)
        self.entries.append(self.lama_pinjaman_entry)

        # Persentase Pendapatan Pinjaman
        loan_income_label = ctk.CTkLabel(self, text="Persentase Pendapatan Pinjaman (%):", bg_color="white")
        loan_income_label.place(x=310, y=460)
        self.loan_income_entry = ctk.CTkEntry(self, width=200, bg_color="white")
        self.loan_income_entry.place(x=310, y=490)
        self.entries.append(self.loan_income_entry)

        # Email
        email_label = ctk.CTkLabel(self, text="Email:", bg_color="white")
        email_label.place(x=680, y=460)
        self.email_entry = ctk.CTkEntry(self, width=200, bg_color="white")
        self.email_entry.place(x=680, y=490)
        self.entries.append(self.email_entry)

        # Kontak
        kontak_label = ctk.CTkLabel(self, text="Kontak:", bg_color="white")
        kontak_label.place(x=1030, y=460)
        self.kontak_entry = ctk.CTkEntry(self, width=200, bg_color="white")
        self.kontak_entry.place(x=1030, y=490)
        self.entries.append(self.kontak_entry)

        # Tombol Submit
        submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_data, corner_radius=12, width=870 ,fg_color='#A6A5AF', bg_color="#fff")
        submit_button.place(x=340, y=585)

    def ensure_csv_exists(self):
        file_path = os.path.join(base_path, 'data.csv')
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                header = ["id", "nama", "usia", "jenis kelamin", "pendapatan tahunan", "lama bekerja",
                          "kepemilikan rumah", "jumlah pinjaman", "tujuan pinjaman", "lama pinjaman",
                          "persentase pendapatan pinjaman", "email", "kontak", "skor risiko kredit",
                          "klasifikasi risiko", "keputusan"]
                writer.writerow(header)

    def submit_data(self):
        # Generate User ID
        user_id = str(random.randint(10000, 99999))
        
        # Retrieve input data
        nama = self.nama_entry.get().strip()
        usia = self.usia_entry.get().strip()
        jenis_kelamin = self.jenis_kelamin_dropdown.get()
        pendapatan_tahunan = self.pendapatan_entry.get().strip()
        lama_bekerja = self.lama_bekerja_entry.get().strip()
        kepemilikan_rumah = self.rumah_dropdown.get()
        jumlah_pinjaman = self.jumlah_pinjaman_entry.get().strip()
        tujuan_pinjaman = self.tujuan_dropdown.get()
        lama_pinjaman = self.lama_pinjaman_entry.get().strip()
        persentase_pinjaman = self.loan_income_entry.get().strip()
        email = self.email_entry.get().strip()
        kontak = self.kontak_entry.get().strip()

        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Alamat email tidak valid!")
            return

        # Validate kontak (only digits)
        if not kontak.isdigit():
            messagebox.showerror("Error", "Kontak harus berupa angka!")
            return

        # Convert percentage to decimal
        try:
            persentase_desimal = float(persentase_pinjaman.strip('%')) / 100
        except ValueError:
            messagebox.showerror("Error", "Persentase pendapatan pinjaman harus berupa persentase valid!")
            return

        # Greedy classification
        def classify_risk(loan_percent_income, loan_amnt, person_income, cred_hist_length):
            # Thresholds dari analisis sebelumnya
            loan_percent_income_thresholds = (0.11, 0.20)
            loan_amnt_thresholds = (6000, 10000)
            person_income_thresholds = (45000, 65000)
            cred_hist_length_thresholds = (3.50, 6.00)

            # Klasifikasi loan_percent_income
            if loan_percent_income < loan_percent_income_thresholds[0]:
                loan_percent_income_risk = 'Rendah'
                loan_percent_income_score = 1
            elif loan_percent_income <= loan_percent_income_thresholds[1]:
                loan_percent_income_risk = 'Sedang'
                loan_percent_income_score = 2
            else:
                loan_percent_income_risk = 'Tinggi'
                loan_percent_income_score = 3

            # Klasifikasi loan_amnt
            if loan_amnt < loan_amnt_thresholds[0]:
                loan_amnt_risk = 'Rendah'
                loan_amnt_score = 1
            elif loan_amnt <= loan_amnt_thresholds[1]:
                loan_amnt_risk = 'Sedang'
                loan_amnt_score = 2
            else:
                loan_amnt_risk = 'Tinggi'
                loan_amnt_score = 3

            # Klasifikasi person_income
            if person_income < person_income_thresholds[0]:
                person_income_risk = 'Rendah'
                person_income_score = 1
            elif person_income <= person_income_thresholds[1]:
                person_income_risk = 'Sedang'
                person_income_score = 2
            else:
                person_income_risk = 'Tinggi'
                person_income_score = 3

            # Klasifikasi cred_hist_length
            if cred_hist_length < cred_hist_length_thresholds[0]:
                cred_hist_length_risk = 'Pendek'
                cred_hist_length_score = 1
            elif cred_hist_length <= cred_hist_length_thresholds[1]:
                cred_hist_length_risk = 'Menengah'
                cred_hist_length_score = 2
            else:
                cred_hist_length_risk = 'Panjang'
                cred_hist_length_score = 3

            # Skor risiko total
            total_risk_score = (loan_percent_income_score +
                                loan_amnt_score +
                                person_income_score +
                                cred_hist_length_score)

            # Tingkat risiko keseluruhan
            if total_risk_score >= 10:
                overall_risk_level = "Tinggi"
            elif 5 <= total_risk_score < 10:
                overall_risk_level = "Sedang"
            else:
                overall_risk_level = "Rendah"

            # Rekomendasi pengambilan keputusan
            if overall_risk_level == "Rendah":
                decision = "Approve"
            elif overall_risk_level == "Sedang":
                decision = "Review Manually"
            else:
                decision = "Reject"

            return total_risk_score, overall_risk_level, decision

        try:
            loan_percent_income = persentase_desimal
            loan_amnt = float(jumlah_pinjaman)
            person_income = float(pendapatan_tahunan)
            cred_hist_length = float(lama_bekerja)
        except ValueError:
            messagebox.showerror("Error", "Pastikan data yang diisi valid!")
            return

        # Kalkulasi risiko
        total_risk_score, risk_classification, decision = classify_risk(loan_percent_income, loan_amnt, person_income, cred_hist_length)

        total_risk_score_formatted = f"{total_risk_score:02}"

        # Save data to CSV
        data = [user_id, nama, usia, jenis_kelamin, pendapatan_tahunan, lama_bekerja,
                kepemilikan_rumah, jumlah_pinjaman, tujuan_pinjaman, lama_pinjaman,
                persentase_desimal, email, kontak, total_risk_score_formatted, risk_classification, decision]
        
        file_path = os.path.join(base_path, 'data.csv')
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")

        # Tampilkan hasil di panel
        print(f"\nKlasifikasi Risiko:")
        print(f"  Total Skor: {total_risk_score}")
        print(f"\nKesimpulan Risiko Keseluruhan: {risk_classification}")
        print(f"Rekomendasi Pengambilan Keputusan: {decision}")

        # Clear all inputs
        for entry in self.entries:
            entry.delete(0, ctk.END)
        
        self.parent.show_hasil_page(user_id, self.username)

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