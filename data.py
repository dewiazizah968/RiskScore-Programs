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

class DataPage(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username

        try:
            bg_image = Image.open(os.path.join(base_path, 'Desain DAA', 'databg.png'))
            self.bg_image = ctk.CTkImage(light_image=bg_image, size=(1366, 768))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("Error", "File gambar background tidak ditemukan.")

        self.add_buttons()
        self.create_table()
        self.reset_selection()

    def create_table(self):
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background="#EAE9F1", 
                        fieldbackground="#EAE9F1",
                        font=("Arial", 10))
        style.configure("Custom.Treeview.Heading", 
                        font=("Arial", 12, "bold"))
        
        # Frame for the table
        table_frame = ctk.CTkFrame(self, width=1266, height=900)
        table_frame.place(x=320, y=250)

        # Treeview widget
        self.tree = ttk.Treeview(
            table_frame, 
            columns=("no", "id", "nama", "usia", "pendapatan", "pinjaman", "keputusan", "detail"), 
            show='headings', 
            height=17,
            style="Custom.Treeview"
        )

        # Define headings
        self.tree.heading("no", text="No")
        self.tree.heading("id", text="ID")
        self.tree.heading("nama", text="Nama")
        self.tree.heading("usia", text="Usia")
        self.tree.heading("pendapatan", text="Pendapatan")
        self.tree.heading("pinjaman", text="Jumlah Pinjaman")
        self.tree.heading("keputusan", text="Keputusan")
        self.tree.heading("detail", text="Action")

        # Define column widths
        self.tree.column("no", width=50, anchor='center')
        self.tree.column("id", width=100, anchor='center')
        self.tree.column("nama", width=200, anchor='w')
        self.tree.column("usia", width=70, anchor='center')
        self.tree.column("pendapatan", width=100, anchor='e')
        self.tree.column("pinjaman", width=100, anchor='e')
        self.tree.column("keputusan", width=180, anchor='center')
        self.tree.column("detail", width=100, anchor='center')

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the treeview
        self.tree.pack(fill="both", expand=True)

        # Load data from CSV
        self.load_data()

    def load_data(self):
        try:
            with open(os.path.join(base_path, 'data.csv'), "r") as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader, start=1):
                    self.tree.insert("", "end", values=(
                        i,
                        row["id"],
                        row["nama"],
                        row["usia"],
                        row["pendapatan tahunan"],
                        row["jumlah pinjaman"],
                        row["keputusan"],
                        "Detail"
                    ))
        except FileNotFoundError:
            messagebox.showerror("Error", "File data.csv tidak ditemukan.")
        except KeyError as e:
            messagebox.showerror("Error", f"Kolom yang dibutuhkan tidak ditemukan: {e}")

        # Bind detail column click
        self.tree.bind("<Button-1>", self.on_detail_click)

    def on_detail_click(self, event):
        row_id = self.tree.identify_row(event.y)  
        column = self.tree.identify_column(event.x)  

        if column == "#8" and row_id:
            values = self.tree.item(row_id, "values")
            if values:
                user_id = values[1]  
                self.parent.show_detail_page(user_id, self.username)  # Panggil halaman detail

    def reset_selection(self):
        """Menghapus seleksi baris di Treeview."""
        self.tree.selection_remove(self.tree.selection())

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