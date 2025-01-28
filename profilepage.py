from tkinter import messagebox
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
import csv
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else:  
    base_path = os.path.dirname(__file__)

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username  

        try:
            bg_image = Image.open(os.path.join(base_path, 'Desain DAA', 'profilebg.png'))
            self.bg_image = ctk.CTkImage(light_image=bg_image, size=(1366, 768))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "File gambar background tidak ditemukan.")

        self.create_profile_page()
        self.add_buttons()

    def create_profile_page(self):
        user_data = self.get_user_data(self.username)

        if user_data:
            username_label = ctk.CTkLabel(
            self,
            text=f"{user_data['username']}",
            font=("Tahoma", 24, "bold"),
            fg_color="#FFFFFF",
            text_color="#000000"
            )
            username_label.place(x=1060, y=520) 

            # Tampilkan informasi user (username, email, password)
            self.create_table([
                ("Username", user_data['username']),
                ("Email", user_data['email']),
                ("Password", user_data['password']),
                ("Relationship Manager", "Relationship Manager")  # Placeholder value
            ])

            self.create_profile_picture(x=963, y=230)

    def create_table(self, data):
        """Membuat tabel untuk menampilkan data user"""
        row_height = 30
        label_width = 150
        value_width = 360

        # Menentukan koordinat untuk masing-masing data
        coordinates = {
            "Username": (190, 272), 
            "Email": (190, 383),
            "Password": (190, 502),
            "Relationship Manager": (190, 608)
        }

        for label_text, value in data:
            x, y = coordinates.get(label_text, (265, 255))  
            
            value_label = ctk.CTkLabel(
                self,
                text=value,
                font=("Tahoma", 16),
                width=value_width,
                height=row_height,
                bg_color="#EAE9F1",
                fg_color="#EAE9F1",
                text_color="#000000",
                corner_radius=10,
                anchor="w"
            )
            value_label.place(x=x + label_width + 10, y=y)        

    def get_user_data(self, username):
        """Mengambil data pengguna dari file CSV berdasarkan username"""
        try:
            csv_file_path = os.path.join(base_path, "data_users.csv")
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        kolom_username = row[0].strip()
                        kolom_email = row[1].strip()
                        kolom_password = row[2].strip()
                        kolom_photo_path = row[3].strip() if len(row) > 3 else ""

                        if kolom_username == username:
                            return {
                                'username': kolom_username,
                                'email': kolom_email,
                                'password': kolom_password,
                                'photo_path': kolom_photo_path
                            }
            return None
        except FileNotFoundError:
            messagebox.showerror("Error", "File data_users.csv not found!")
            return None
        
    def create_profile_picture(self, x, y):
        """Menampilkan foto profil dengan lingkaran dan tombol Change dan Delete"""
        try:
            user_data = self.get_user_data(self.username)

            # Gunakan gambar default jika tidak ada photo_path
            if user_data and user_data.get('photo_path'):
                photo_path = user_data['photo_path']
            else:
                photo_path = os.path.join(base_path, "Desain DAA", "defaultprofile.png")

            if not os.path.exists(photo_path):  
                photo_path = os.path.join(base_path, "Desain DAA", "defaultprofile.png")

            photo_image = Image.open(photo_path)
            photo_image = photo_image.resize((260, 260))
            photo_image = photo_image.convert("RGBA")

            # Buat lingkaran untuk foto profil
            mask = Image.new("L", photo_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, photo_image.size[0], photo_image.size[1]), fill=255)
            photo_image.putalpha(mask)

            self.photo_image = ImageTk.PhotoImage(photo_image)
            self.profile_picture_label = ctk.CTkLabel(self, image=self.photo_image, text="", bg_color="#fff")
            self.profile_picture_label.place(x=x, y=y)

            # Button Change dan Delete
            self.create_button("Change", x + 10, y + 360, self.change_picture)
            self.create_button("Delete", x + 160, y + 360, self.delete_picture)

        except FileNotFoundError:
            messagebox.showerror("Error", "File gambar profil tidak ditemukan.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def create_button(self, text, x, y, command):
        """Membuat tombol dengan posisi x, y"""
        button = ctk.CTkButton(
            self, 
            text=text, 
            command=command, 
            width=100, 
            height=30, 
            corner_radius=20, 
            bg_color="#fff",
            fg_color="#EAE9F1", 
            text_color="#4B4B4B"  
        )
        button.place(x=x, y=y)

    def change_picture(self):
        """Fungsi untuk mengganti foto profil"""
        # Dialog untuk memilih file gambar
        file_path = filedialog.askopenfilename(
            title="Select a Profile Picture",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        )

        if not file_path:
            messagebox.showinfo("Info", "No file selected.")
            return

        csv_file = os.path.join(base_path, "data_users.csv")

        updated = False
        rows = []
        try:
            with open(csv_file, mode="r", newline='', encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == self.username:  # Cek berdasarkan username
                        if len(row) == 3:
                            row.append(file_path)
                        else:
                            row[3] = file_path
                        updated = True
                    rows.append(row)

            if updated:
                with open(csv_file, mode="w", newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                
                self.update_profile_picture(file_path)
                messagebox.showinfo("Success", "Profile picture updated successfully!")
            else:
                messagebox.showerror("Error", "User not found in the database.")

        except FileNotFoundError:
            messagebox.showerror("Error", f"CSV file not found: {csv_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_profile_picture(self, file_path):
        """Memperbarui tampilan foto profil di GUI"""
        try:
            new_photo_image = Image.open(file_path)
            
            new_photo_image = new_photo_image.resize((260, 260))
            new_photo_image = new_photo_image.convert("RGBA")
            mask = Image.new("L", new_photo_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, new_photo_image.size[0], new_photo_image.size[1]), fill=255)
            new_photo_image.putalpha(mask)

            self.photo_image = ImageTk.PhotoImage(new_photo_image)
            self.profile_picture_label.configure(image=self.photo_image)

        except FileNotFoundError:
            messagebox.showerror("Error", "Selected image file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_picture(self):
        """Fungsi untuk menghapus foto profil"""
        response = messagebox.askyesno("Delete Picture", "Are you sure you want to delete your profile picture?")
        if not response:
            return

        csv_file = os.path.join(base_path, "data_users.csv")

        updated = False
        rows = []
        try:
            with open(csv_file, mode="r", newline='', encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == self.username:  
                        if len(row) > 3:
                            row.pop(3)  
                        updated = True
                    rows.append(row)

            if updated:
                with open(csv_file, mode="w", newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)

                self.update_profile_picture_to_default()
                messagebox.showinfo("Success", "Profile picture deleted successfully!")
            else:
                messagebox.showerror("Error", "User not found in the database.")

        except FileNotFoundError:
            messagebox.showerror("Error", f"CSV file not found: {csv_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_profile_picture_to_default(self):
        """Mengganti foto profil di GUI ke foto default"""
        try:
            default_photo_path = os.path.join(base_path, "Desain DAA", "defaultprofile.png")
            default_photo_image = Image.open(default_photo_path)

            default_photo_image = default_photo_image.resize((260, 260))
            default_photo_image = default_photo_image.convert("RGBA")
            mask = Image.new("L", default_photo_image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, default_photo_image.size[0], default_photo_image.size[1]), fill=255)
            default_photo_image.putalpha(mask)

            self.photo_image = ImageTk.PhotoImage(default_photo_image)
            self.profile_picture_label.configure(image=self.photo_image)

        except FileNotFoundError:
            messagebox.showerror("Error", "Default profile picture file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def add_buttons(self):
        button_names = ['profile', 'dashboard', 'input', 'data', 'logout']
        button_images = {
            'profile': "profileaktif.png",
            'dashboard': "dashboard.png",
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
                img_path = os.path.join(base_path, "Desain DAA", button_images[name])
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
