import customtkinter
from tkinter import ttk
import re
from tkinter import *
import tkinter as tk
import bcrypt
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
import datetime
from datetime import date
from datetime import datetime
import random
from PIL import Image
from winotify import Notification, audio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedStyle
from distinctipy import distinctipy

app = customtkinter.CTk()
app.geometry("1280x720")
app.resizable(False, False)
app.title("IMS")
customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("Light")


def login_page():
    def login():
        name = log_user.get()
        code = log_password.get()
        userbytes = code.encode("utf-8")
        if name == "" or code == "":
            messagebox.showerror("Empty", "Please fill in the empty field")
        else:
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.execute("SELECT USERNAME FROM USER WHERE USERNAME=?", (name,))
            if cursor.fetchone():
                cursor = conn.execute(
                    "SELECT PASSWORD FROM USER WHERE USERNAME=?", (name,)
                )
                stored_password_tuple = cursor.fetchone()
                if stored_password_tuple:
                    cursor2 = conn.execute(
                        "SELECT ACCESSLEVEL FROM USER WHERE USERNAME=?", (name,)
                    )
                    level = cursor2.fetchone()
                    db_password = stored_password_tuple[0]
                    b_stored_password = db_password.encode("utf-8")
                    if bcrypt.checkpw(userbytes, b_stored_password):
                        messagebox.showinfo("Success", "Login Success")
                        if level[0] == 0:
                            login_page_frame.destroy()
                            admin_dashboard(name)
                        if level[0] == 1:
                            login_page_frame.destroy()
                            supervisor_dashboard(name)
                        if level[0] == 2:
                            login_page_frame.destroy()
                            worker_dashboard(name)
                    else:
                        messagebox.showerror("Invalid", "Invalid Username or Password")
                else:
                    messagebox.showerror("Invalid", "Invalid Username or Password")

    login_page_frame = customtkinter.CTkFrame(
        master=app, width=1280, height=720, border_width=0
    )
    login_page_frame.place(x=0, y=0)

    image_frame = customtkinter.CTkFrame(master=login_page_frame, width=640, height=720)
    image_frame.place(x=0, y=0)
    logo = customtkinter.CTkImage(Image.open("assets/7078214.png"), size=(150, 150))
    logo_label = customtkinter.CTkLabel(master=image_frame, image=logo, text="")
    logo_label.place(x=70, y=50)

    expense_tracker_label = customtkinter.CTkLabel(
        master=image_frame,
        text="Invy",
        font=customtkinter.CTkFont("SF Pro Display", 80, weight="bold"),
    )
    expense_tracker_label.place(x=70, y=220)
    introduction_label = customtkinter.CTkLabel(
        master=image_frame,
        text="Your streamlined solution for efficient inventory management. Designed to simplify tracking, organizing, and managing your inventory",
        font=customtkinter.CTkFont("SF Pro Display", 16),
        wraplength=450,
        justify="left",
    )
    introduction_label.place(x=80, y=350)

    login_frame = customtkinter.CTkFrame(master=login_page_frame, width=640, height=720)
    login_frame.pack()
    login_frame.place(x=640, y=0)

    log_label = customtkinter.CTkLabel(
        master=login_frame,
        text="Sign in",
        width=212,
        height=80,
        font=customtkinter.CTkFont("SF Pro Display", 64, weight="bold"),
    )
    log_label.place(x=214, y=118.5)

    log_user = customtkinter.CTkEntry(
        master=login_frame,
        placeholder_text="Username",
        width=300,
        height=45,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    log_user.place(x=170, y=280.5)
    app.update()
    log_user.focus_set()

    log_password = customtkinter.CTkEntry(
        master=login_frame,
        placeholder_text="Password",
        width=300,
        height=45,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    log_password.place(x=170, y=356.5)
    log_password.configure(show="*")

    log_btn_image = customtkinter.CTkImage(
        Image.open("assets/enter.png"), size=(20, 20)
    )
    log_btn = customtkinter.CTkButton(
        master=login_frame,
        text="Login",
        width=300,
        height=45,
        font=customtkinter.CTkFont("SF Pro Display", 15),
        command=login,
        image=log_btn_image,
        compound="right",
        text_color=("black", "white"),
        fg_color="transparent",
        hover=False,
    )
    log_btn.place(x=170, y=436)

    def show_hide_password():
        if log_show_hide.get() == "on":
            log_password.configure(show="")
        else:
            log_password.configure(show="*")

    log_show_hide = customtkinter.StringVar(value="off")
    log_show_hide_password_switch = customtkinter.CTkSwitch(
        master=login_frame,
        text="Show Password",
        command=show_hide_password,
        variable=log_show_hide,
        onvalue="on",
        offvalue="off",
        font=customtkinter.CTkFont("SF Pro Display"),
    )
    log_show_hide_password_switch.place(x=480, y=368.5)

    def switch_theme():
        if log_switch_theme_var.get() == "on":
            customtkinter.set_appearance_mode("Light")
        else:
            customtkinter.set_appearance_mode("Dark")

    log_switch_theme_var = customtkinter.StringVar(value="off")
    log_switch_theme_switch = customtkinter.CTkSwitch(
        master=login_frame,
        text="Switch Theme",
        command=switch_theme,
        variable=log_switch_theme_var,
        onvalue="on",
        offvalue="off",
        font=customtkinter.CTkFont("SF Pro Display"),
    )
    log_switch_theme_switch.place(x=500, y=680)


def admin_dashboard(username):

    def fetch_to_be_packed_data():
        total_to_be_packed = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Packed",))
        to_be_packed_data = cursor.fetchone()[0]
        total_to_be_packed += to_be_packed_data
        conn.commit()
        conn.close()
        return total_to_be_packed

    def update_to_be_packed_label():
        new_count = fetch_to_be_packed_data()
        total_to_be_packed_label_1.configure(text=str(new_count))

    def fetch_to_be_shipped_data():
        total_to_be_shipped = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Shipped",))
        to_be_shipped_data = cursor.fetchone()[0]
        total_to_be_shipped += to_be_shipped_data
        conn.commit()
        conn.close()
        return total_to_be_shipped

    def update_to_be_shipped_label():
        new_count = fetch_to_be_shipped_data()
        total_to_be_shipped_label_1.configure(text=str(new_count))

    def fetch_to_be_delivered_data():
        total_to_be_delivered = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Delivered",))
        to_be_delivered_data = cursor.fetchone()[0]
        total_to_be_delivered += to_be_delivered_data
        conn.commit()
        conn.close()
        return total_to_be_delivered

    def update_to_be_delivered_label():
        new_count = fetch_to_be_delivered_data()
        total_to_be_delivered_label_1.configure(text=str(new_count))

    def fetch_total_quantity_in_hand_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(PRODUCT_QUANTITY) FROM PRODUCT")
        total_quantity_in_hand = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_quantity_in_hand

    def update_total_quantity_in_hand_label():
        new_count = fetch_total_quantity_in_hand_data()
        total_quantity_in_hand_1.configure(text=str(new_count))

    def fetch_total_quantity_to_be_received_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(PURCHASE_ORDER_PRODUCT_QUANTITY) FROM PURCHASE_ORDER WHERE PURCHASE_ORDER_STATUS = ?", ("To be Received",))
        total_quantity_to_be_received = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_quantity_to_be_received

    def update_total_quantity_to_be_received_label():
        new_count = fetch_total_quantity_to_be_received_data()
        total_quantity_to_be_received_1.configure(text=str(new_count))

    def fetch_low_stock_item_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT WHERE PRODUCT_QUANTITY < PRODUCT_MIN_STOCK")
        low_stock_items = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return low_stock_items

    def update_low_stock_item_label():
        new_count = fetch_low_stock_item_data()
        low_stock_items_1.configure(text=str(new_count))

    def fetch_total_items_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT")
        total_items = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_items

    def update_total_items_label():
        new_count = fetch_total_items_data()
        all_items_1.configure(text=str(new_count))
    def register():
        name = reg_user.get()
        code = reg_password.get()
        level = reg_accesslevel.get()
        if level == "Admin":
            level = 0
        elif level == "Supervisor":
            level = 1
        elif level == "Warehouse Worker":
            level = 2
        bytes = code.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes, salt)
        stored_password = hashed_password.decode("utf-8")
        confirm_code = reg_confirm_password.get()
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT USERNAME FROM USER WHERE USERNAME=?", (name,))
        existing_user = cursor.fetchone()
        if name == "" or code == "" or confirm_code == "":
            messagebox.showerror("Empty", "Please fill in the empty field")
        elif existing_user:
            messagebox.showerror("Invalid", "User already existed")
        elif code != confirm_code:
            messagebox.showerror("Invalid", "Please enter the correct password")
        elif len(code) < 8:
            messagebox.showerror(
                "Invalid", "Make sure your password is at least 8 letters"
            )
        elif re.search("[0-9]", code) is None:
            messagebox.showerror(
                "Invalid", "Make sure your password has a number in it"
            )
        elif re.search("[A-Z]", code) is None:
            messagebox.showerror(
                "Invalid", "Make sure your password has a uppercase letter in it"
            )
        else:
            conn.execute(
                "INSERT INTO USER (USERNAME,PASSWORD,ACCESSLEVEL) \
            VALUES (?,?,?)",
                (name, stored_password, level),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Valid", "Account created")
            add_to_user_table()

    def fetch_user_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT USERNAME, ACCESSLEVEL FROM USER")
        user = cursor.fetchall()
        conn.commit()
        conn.close()
        return user

    def add_to_user_table():
        users = fetch_user_data()
        user_tree.delete(*user_tree.get_children())
        for user in users:
            user_tree.insert("", END, values=user)

    def on_user_double_click(event):
        selected_item = user_tree.selection()[0]
        values = user_tree.item(selected_item, "values")

        change_pw_window = customtkinter.CTk()
        change_pw_window.title("Change Password")

        def fetch_selected_user_details():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USER WHERE USERNAME = ?", (values[0],))
            user_details = cursor.fetchall()
            conn.commit()
            conn.close()
            return user_details

        def change_password():
            new_password = new_password_entry.get()
            bytes = new_password.encode("utf-8")
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(bytes, salt)
            stored_password = hashed_password.decode("utf-8")
            if not new_password:
                messagebox.showerror("Empty", "Please fill in the empty field")
            elif len(new_password) < 8:
                messagebox.showerror(
                    "Invalid", "Make sure your password is at least 8 letters"
                )
            elif re.search("[0-9]", new_password) is None:
                messagebox.showerror(
                    "Invalid", "Make sure your password has a number in it"
                )
            elif re.search("[A-Z]", new_password) is None:
                messagebox.showerror(
                    "Invalid", "Make sure your password has a uppercase letter in it"
                )
            else:
                conn = sqlite3.connect("Inventory Management System.db")
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE USER SET PASSWORD = ? WHERE USERNAME = ?",
                    (stored_password, values[0]),
                )
                conn.commit()
                conn.close()
                change_pw_window.destroy()

        change_pw_title = customtkinter.CTkLabel(
            change_pw_window,
            text="Change Password",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )

        targeted_user_label = customtkinter.CTkLabel(
            change_pw_window,
            text="Targeted User:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        targeted_user_label_details = customtkinter.CTkLabel(
            change_pw_window,
            text=f"{values[0]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )

        new_password_label = customtkinter.CTkLabel(
            change_pw_window,
            text="New Password:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        new_password_entry = customtkinter.CTkEntry(
            master=change_pw_window,
            placeholder_text="Password",
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display", size=13),
            border_width=0,
        )
        change_pw_btn = customtkinter.CTkButton(
            master=change_pw_window,
            text="Change Password",
            command=change_password,
            font=customtkinter.CTkFont("SF Pro Display", size=13),
            corner_radius=200,
            fg_color="#007FFF",
            text_color="black",
        )

        change_pw_title.grid(row=0, column=0, columnspan=2, sticky=W, padx=(10, 0), pady=5)
        targeted_user_label.grid(row=1, column=0, sticky=W, padx=(10, 0), pady=3)
        targeted_user_label_details.grid(row=1, column=1, sticky=W, padx=5, pady=3)
        new_password_label.grid(row=2, column=0, sticky=W, padx=(10, 0), pady=3)
        new_password_entry.grid(row=2, column=1, sticky=W, padx=5, pady=3)
        change_pw_btn.grid(row=3, column=0, columnspan=2, padx=(10, 0), pady=5)

        change_pw_window.mainloop()

    def delete_user_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = user_tree.focus()
        row = user_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM USER WHERE USERNAME= ?", (row[0],))
        conn.commit()
        conn.close()
        add_to_user_table()

    def delete_user_record():
        selected_item = user_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_user_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    # def fetch_customer_data():
    #     conn = sqlite3.connect("Inventory Management System.db")
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM CUSTOMER")
    #     customer = cursor.fetchall()
    #     conn.commit()
    #     conn.close()
    #     return customer
    #
    # def clear_customer_entry_field():
    #     customer_name_entry.delete(0, END)
    #     customer_email_entry.delete(0, END)
    #     customer_contact_entry.delete(0, END)
    #
    # def display_customer_record(event):
    #     selected_item = customer_tree.focus()
    #     if selected_item:
    #         clear_customer_entry_field()
    #         row = customer_tree.item(selected_item)["values"]
    #         customer_name_entry.insert(0, row[1])
    #         customer_email_entry.insert(0, row[2])
    #         customer_contact_entry.insert(0, row[3])
    #
    # def add_to_customer_table():
    #     customers = fetch_customer_data()
    #     customer_tree.delete(*customer_tree.get_children())
    #     for customer in customers:
    #         customer_tree.insert("", END, values=customer)
    #
    # def check_existing_customer(customer_check):
    #     conn = sqlite3.connect("Inventory Management System.db")
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         "SELECT CUSTOMER_NAME FROM CUSTOMER WHERE CUSTOMER_NAME = ?",
    #         (customer_check,),
    #     )
    #     existing_customer = cursor.fetchone()
    #     conn.commit()
    #     conn.close()
    #     return existing_customer
    #
    # def add_new_customer_details():
    #     customer_name = customer_name_entry.get()
    #     customer_email = customer_email_entry.get()
    #     customer_contactno = customer_contact_entry.get()
    #
    #     if not (customer_name and customer_email and customer_contactno):
    #         messagebox.showerror("Error", "Please enter all fields")
    #         return
    #     elif not check_existing_customer(customer_name):
    #         conn = sqlite3.connect("Inventory Management System.db")
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             "INSERT INTO CUSTOMER (CUSTOMER_NAME,CUSTOMER_EMAIL,CUSTOMER_TEL) \
    #         VALUES (?,?,?)",
    #             (customer_name, customer_email, customer_contactno),
    #         )
    #         conn.commit()
    #         conn.close()
    #         messagebox.showinfo("Success", "Data has been inserted")
    #     else:
    #         messagebox.showerror(
    #             "Warning", "Duplicate customer! Please enter new customer."
    #         )
    #     add_to_customer_table()
    #     clear_customer_entry_field()
    #     return
    #
    # def edit_customer_details():
    #     selected_customer_details = customer_tree.focus()
    #     if not selected_customer_details:
    #         messagebox.showerror("Error", "Please select a record to edit")
    #         return
    #     row = customer_tree.item(selected_customer_details)["values"]
    #     new_customer_name = customer_name_entry.get()
    #     new_customer_email = customer_email_entry.get()
    #     new_customer_contactno = customer_contact_entry.get()
    #     if not new_customer_name:
    #         messagebox.showerror("Error", "Please enter all fields")
    #         return
    #     else:
    #         conn = sqlite3.connect("Inventory Management System.db")
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             "UPDATE CUSTOMER SET CUSTOMER_NAME = ?, CUSTOMER_EMAIL = ?, CUSTOMER_TEL = ? WHERE CUSTOMER_NAME = ?",
    #             (new_customer_name, new_customer_email, new_customer_contactno, row[1]),
    #         )
    #         conn.commit()
    #         conn.close()
    #         messagebox.showinfo("Success", "Record successfully edited")
    #     add_to_customer_table()
    #     clear_customer_entry_field()
    #
    # def delete_customer_database():
    #     conn = sqlite3.connect("Inventory Management System.db")
    #     cursor = conn.cursor()
    #     selected_item = customer_tree.focus()
    #     row = customer_tree.item(selected_item)["values"]
    #     cursor.execute("DELETE FROM CUSTOMER WHERE CUSTOMER_NAME= ?", (row[1],))
    #     conn.commit()
    #     conn.close()
    #     add_to_customer_table()
    #     clear_customer_entry_field()
    #
    # def delete_customer_record():
    #     selected_item = customer_tree.focus()
    #     if not selected_item:
    #         messagebox.showerror("Error", "Please select a record to delete")
    #         return
    #     confirmation = messagebox.askyesno(
    #         "Are you sure?", "Are you sure that you want to delete the selected record?"
    #     )
    #     if confirmation:
    #         delete_customer_database()
    #         messagebox.showinfo("Success", "Record successfully deleted")
    #         return
    #
    # def fetch_supplier_data():
    #     conn = sqlite3.connect("Inventory Management System.db")
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM SUPPLIER")
    #     supplier = cursor.fetchall()
    #     conn.commit()
    #     conn.close()
    #     return supplier
    #
    # def add_to_supplier_table():
    #     suppliers = fetch_supplier_data()
    #     supplier_tree.delete(*supplier_tree.get_children())
    #     for supplier in suppliers:
    #         supplier_tree.insert("", END, values=supplier)
    #
    # def clear_supplier_entry_field():
    #     supplier_name_entry.delete(0, END)
    #     supplier_email_entry.delete(0, END)
    #     supplier_contact_entry.delete(0, END)
    #
    # def display_supplier_record(event):
    #     selected_item = supplier_tree.focus()
    #     if selected_item:
    #         clear_supplier_entry_field()
    #         row = supplier_tree.item(selected_item)["values"]
    #         supplier_name_entry.insert(0, row[1])
    #         supplier_email_entry.insert(0, row[2])
    #         supplier_contact_entry.insert(0, row[3])
    #
    # def check_existing_supplier(supplier_check):
    #     conn = sqlite3.connect("Inventory Management System.db")
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         "SELECT SUPPLIER_NAME FROM SUPPLIER WHERE SUPPLIER_NAME = ?",
    #         (supplier_check,),
    #     )
    #     existing_supplier = cursor.fetchone()
    #     conn.commit()
    #     conn.close()
    #     return existing_supplier
    #
    # def add_new_supplier_details():
    #     supplier_name = supplier_name_entry.get()
    #     supplier_email = supplier_email_entry.get()
    #     supplier_contactno = supplier_contact_entry.get()
    #
    #     if not (supplier_name and supplier_email and supplier_contactno):
    #         messagebox.showerror("Error", "Please enter all fields")
    #         return
    #     elif not check_existing_supplier(supplier_name):
    #         conn = sqlite3.connect("Inventory Management System.db")
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             "INSERT INTO SUPPLIER (SUPPLIER_NAME,SUPPLIER_EMAIL,SUPPLIER_TEL) \
    #         VALUES (?,?,?)",
    #             (supplier_name, supplier_name, supplier_contactno),
    #         )
    #         conn.commit()
    #         conn.close()
    #         messagebox.showinfo("Success", "Data has been inserted")
    #     else:
    #         messagebox.showerror(
    #             "Warning", "Duplicate customer! Please enter new customer."
    #         )
    #     add_to_supplier_table()
    #     clear_supplier_entry_field()
    #     return
    #
    # def edit_supplier_details():
    #     selected_supplier_details = supplier_tree.focus()
    #     if not selected_supplier_details:
    #         messagebox.showerror("Error", "Please select a record to edit")
    #         return
    #     row = supplier_tree.item(selected_supplier_details)["values"]
    #     new_supplier_name = supplier_name_entry.get()
    #     new_supplier_email = supplier_email_entry.get()
    #     new_supplier_contactno = supplier_contact_entry.get()
    #     if not new_supplier_name:
    #         messagebox.showerror("Error", "Please enter all fields")
    #         return
    #     else:
    #         conn = sqlite3.connect("Inventory Management System.db")
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             "UPDATE SUPPLIER SET SUPPLIER_NAME = ?, SUPPLIER_EMAIL = ?, SUPPLIER_TEL = ? WHERE SUPPLIER_NAME = ?",
    #             (new_supplier_name, new_supplier_email, new_supplier_contactno, row[1]),
    #         )
    #         conn.commit()
    #         conn.close()
    #         messagebox.showinfo("Success", "Record successfully edited")
    #     add_to_supplier_table()
    #     clear_supplier_entry_field()
    #
    # def delete_supplier_database():
    #     conn = sqlite3.connect("Inventory Management System.db")
    #     cursor = conn.cursor()
    #     selected_item = supplier_tree.focus()
    #     row = supplier_tree.item(selected_item)["values"]
    #     cursor.execute("DELETE FROM SUPPLIER WHERE SUPPLIER_NAME= ?", (row[1],))
    #     conn.commit()
    #     conn.close()
    #     add_to_supplier_table()
    #     clear_supplier_entry_field()
    #
    # def delete_supplier_record():
    #     selected_item = supplier_tree.focus()
    #     if not selected_item:
    #         messagebox.showerror("Error", "Please select a record to delete")
    #         return
    #     confirmation = messagebox.askyesno(
    #         "Are you sure?", "Are you sure that you want to delete the selected record?"
    #     )
    #     if confirmation:
    #         delete_supplier_database()
    #         messagebox.showinfo("Success", "Record successfully deleted")
    #         return

    def fetch_product_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PRODUCT")
        product = cursor.fetchall()
        conn.commit()
        conn.close()
        return product

    def add_to_product_table():
        products = fetch_product_data()
        product_tree.delete(*product_tree.get_children())
        for product in products:
            product_tree.insert("", END, values=product)

    def clear_product_entry_field():
        product_id_entry.delete(0, END)
        product_name_entry.delete(0, END)
        product_quantity_entry.delete(0, END)
        product_description_entry.delete(0, END)
        product_min_stock_entry.delete(0, END)

    def display_product_record(event):
        selected_item = product_tree.focus()
        if selected_item:
            clear_product_entry_field()
            row = product_tree.item(selected_item)["values"]
            product_id_entry.insert(0, [row[0]])
            product_name_entry.insert(0, row[1])
            product_quantity_entry.insert(0, row[2])
            product_description_entry.insert(0, row[3])
            product_min_stock_entry.insert(0, [row[4]])

    def check_existing_product(product_check):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUPPLIER_NAME FROM SUPPLIER WHERE SUPPLIER_NAME = ?",
            (product_check,),
        )
        existing_supplier = cursor.fetchone()
        conn.commit()
        conn.close()
        return existing_supplier

    def add_new_product_details():
        product_id = product_id_entry.get()
        product_name = product_name_entry.get()
        product_quantity = product_quantity_entry.get()
        product_description = product_description_entry.get()
        product_min_stock = product_min_stock_entry.get()

        if not (product_name and product_quantity and product_description):
            messagebox.showerror("Error", "Please enter all fields")
            return
        elif not check_existing_product(product_name):
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PRODUCT (PRODUCT_ID,PRODUCT_NAME,PRODUCT_QUANTITY,PRODUCT_STATUS,PRODUCT_MIN_STOCK) \
            VALUES (?,?,?,?,?)",
                (
                    product_id,
                    product_name,
                    product_quantity,
                    product_description,
                    product_min_stock,
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
        else:
            messagebox.showerror(
                "Warning", "Duplicate customer! Please enter new customer."
            )
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()
        return

    def edit_product_details():
        selected_product_details = product_tree.focus()
        if not selected_product_details:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = product_tree.item(selected_product_details)["values"]
        new_product_id = product_id_entry.get()
        new_product_name = product_name_entry.get()
        new_product_quantity = product_quantity_entry.get()
        new_product_description = product_description_entry.get()
        new_product_min_stock = product_min_stock_entry.get()
        if not new_product_name:
            messagebox.showerror("Error", "Please enter all fields")
            return
        else:
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE PRODUCT SET PRODUCT_ID = ?, PRODUCT_NAME = ?, PRODUCT_QUANTITY = ?, PRODUCT_STATUS = ?, PRODUCT_MIN_STOCK = ? WHERE PRODUCT_NAME = ?",
                (
                    new_product_id,
                    new_product_name,
                    new_product_quantity,
                    new_product_description,
                    new_product_min_stock,
                    row[1],
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record successfully edited")
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def delete_product_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = product_tree.focus()
        row = product_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM PRODUCT WHERE PRODUCT_NAME= ?", (row[1],))
        conn.commit()
        conn.close()
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def delete_product_record():
        selected_item = product_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_product_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    def search_product(event):
        search_term = search_entry.get().lower()
        products = fetch_product_data()
        product_tree.delete(*product_tree.get_children())
        for product in products:
            if search_term in str(product).lower():
                product_tree.insert("", tk.END, values=product)

    def on_product_double_click(event):

        selected_item = product_tree.selection()[0]
        values = product_tree.item(selected_item, "values")

        def fetch_selected_product_details():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCT WHERE PRODUCT_NAME = ?", (values[1],))
            product_details = cursor.fetchall()
            conn.commit()
            conn.close()
            return product_details

        new_window = customtkinter.CTk()
        new_window.title("Product Details")
        # new_window.geometry("500x400")

        def add_incoming_stock():
            incoming_stock_id = generate_purchase_order_id("PO")
            incoming_stock_product = values[1]
            incoming_stock_quantity = restock_quantity_entry.get()
            incoming_stock_status = "To be Received"

            if not incoming_stock_quantity:
                messagebox.showerror("Error", "Please enter all fields")
                return

            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PURCHASE_ORDER (PURCHASE_ORDER_ID,PURCHASE_ORDER_PRODUCT,PURCHASE_ORDER_PRODUCT_QUANTITY,PURCHASE_ORDER_STATUS) \
            VALUES (?,?,?,?)",
                (
                    incoming_stock_id,
                    incoming_stock_product,
                    incoming_stock_quantity,
                    incoming_stock_status,
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
            add_to_incoming_stock_table()
            fetch_tbr_quantity()
            update_total_quantity_in_hand_label()
            update_total_quantity_to_be_received_label()
            new_window.destroy()

        def fetch_tbr_quantity():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT PURCHASE_ORDER_PRODUCT_QUANTITY FROM PURCHASE_ORDER WHERE PURCHASE_ORDER_PRODUCT = ? AND PURCHASE_ORDER_STATUS=?",
                (values[1], "To be Received"),
            )
            incoming_stock_quantity = cursor.fetchall()
            tbr = 0
            for x in incoming_stock_quantity:
                tbr += x[0]
            conn.commit()
            conn.close()
            return tbr

        def fetch_tbs_quantity():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT SALE_ORDER_PRODUCT_QUANTITY FROM SALE_ORDER_PRODUCT WHERE SALE_ORDER_PRODUCT = ?",
                (values[1],),
            )
            outgoing_stock_quantity = cursor.fetchall()
            tbs = 0
            for x in outgoing_stock_quantity:
                tbs += x[0]
            conn.commit()
            conn.close()
            return tbs

        product_details_frame = customtkinter.CTkFrame(new_window, border_width=2)
        product_details_title = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Details",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        product_id_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product ID:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_id_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[0]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_name_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Name:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_name_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[1]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_quantity_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Quantity:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_quantity_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[2]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_description_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Description:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_description_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[3]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )

        restock_frame = customtkinter.CTkFrame(new_window, border_width=2)
        restock_title = customtkinter.CTkLabel(
            restock_frame,
            text="Restock",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        restock_quantity_label = customtkinter.CTkLabel(
            restock_frame,
            text="Restock Quantity:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        restock_quantity_entry = customtkinter.CTkEntry(
            master=restock_frame,
            placeholder_text="Quantity",
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display", size=13),
            border_width=0,
        )

        restock_btn = customtkinter.CTkButton(
            master=restock_frame,
            text="Restock",
            command=add_incoming_stock,
            font=customtkinter.CTkFont("SF Pro Display", size=13),
            corner_radius=200,
            fg_color="#007FFF",
            text_color="black",
        )

        status_frame = customtkinter.CTkFrame(new_window, border_width=2)
        status_details_title = customtkinter.CTkLabel(
            status_frame,
            text="Status",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        total_tbs = customtkinter.CTkFrame(
            master=status_frame, width=100, height=100, fg_color="transparent"
        )
        total_tbs_details_1 = customtkinter.CTkLabel(
            total_tbs,
            text=(str(fetch_tbs_quantity()) + " Qty"),
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        total_tbs_details_2 = customtkinter.CTkLabel(
            total_tbs,
            text="To be Shipped",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        vertical_separator = customtkinter.CTkFrame(
            status_frame, width=2, height=80, fg_color="#CCCCCC"
        )
        total_tbr = customtkinter.CTkFrame(
            master=status_frame, width=100, height=100, fg_color="transparent"
        )
        total_tbr_details_1 = customtkinter.CTkLabel(
            total_tbr,
            text=(str(fetch_tbr_quantity()) + " Qty"),
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        total_tbr_details_2 = customtkinter.CTkLabel(
            total_tbr,
            text="To be Received",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )

        product_details_frame.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        product_details_title.grid(
            row=0, column=0, columnspan=2, sticky=W, padx=10, pady=10
        )
        product_id_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        product_id_label_details.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        product_name_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        product_name_label_details.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        product_quantity_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
        product_quantity_label_details.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        product_description_label.grid(row=4, column=0, sticky=W, padx=5, pady=5)
        product_description_label_details.grid(
            row=4, column=1, sticky=W, padx=5, pady=5
        )

        restock_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        restock_title.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        restock_quantity_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        restock_quantity_entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        restock_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        status_frame.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        status_details_title.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        total_tbs.grid(row=1, column=0, rowspan=5, padx=15, pady=15)
        total_tbs_details_1.pack(side=TOP)
        total_tbs_details_2.pack(side=BOTTOM)
        vertical_separator.grid(row=1, column=1, rowspan=5, pady=36)
        total_tbr.grid(row=1, column=3, rowspan=5, padx=15, pady=15)
        total_tbr_details_1.pack(side=TOP)
        total_tbr_details_2.pack(side=BOTTOM)

        new_window.mainloop()

    def sort_treeview_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: sort_treeview_column(tv, col, not reverse))

    def low_stock_vs_total_item_pie_chart(canvas):
        data=[]

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT WHERE PRODUCT_QUANTITY < PRODUCT_MIN_STOCK")
        low_stock_items = cursor.fetchone()[0]
        data.append(low_stock_items)
        conn.commit()
        conn.close()

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT")
        total_items = cursor.fetchone()[0]
        data.append(total_items - low_stock_items)
        conn.commit()
        conn.close()

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#e5e5e5')  # Set the figure background color
        ax.set_facecolor('#e5e5e5')  # Set the axes background color
        ax.axis("equal")

        ax.pie(data, labels=["Low Stock", "In Stock"], autopct="%.2f%%", pctdistance=0.85)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)

        canvas.figure = fig
        canvas.draw()

    def bar_chart(canvas):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT PRODUCT_ID, PRODUCT_QUANTITY FROM PRODUCT")
        data = cursor.fetchall()
        conn.commit()
        conn.close()

        product_ids = [row[0] for row in data]
        product_quantities = [row[1] for row in data]

        fig1 = plt.Figure()
        ax = fig1.add_subplot(111)
        fig1.patch.set_facecolor('#e5e5e5')
        ax.set_facecolor('#e5e5e5')
        ax.bar(product_ids, product_quantities)
        ax.tick_params(axis='x', labelsize=5)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel('Product Name', fontsize=12)
        ax.set_ylabel('Product Quantity', fontsize=12)
        ax.set_title('Inventory', fontsize=14)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

        canvas.figure = fig1
        canvas.draw()

    admin_dashboard_frame = customtkinter.CTkFrame(
        master=app, width=1280, height=720, border_width=0
    )
    admin_dashboard_frame.place(x=0, y=0)

    info_frame = customtkinter.CTkFrame(
        master=admin_dashboard_frame, width=1280, height=720
    )
    info_frame.place(x=0, y=0)
    info_tab = customtkinter.CTkTabview(master=info_frame, width=1280, height=720)
    info_tab.place(x=0, y=0)
    tab_0 = info_tab.add("Homepage")
    tab_1 = info_tab.add("Register User")
    tab_4 = info_tab.add("Product")
    tab_5 = info_tab.add("User Activities")

    welcome_label = customtkinter.CTkLabel(
        master=tab_0,
        text=f"Hello, {username} ",
        font=customtkinter.CTkFont("SF Pro Display", 24, weight="bold"),
    )

    sales_activity_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    sales_activity_title = customtkinter.CTkLabel(
        sales_activity_frame,
        text="Sales Activity",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    total_to_be_packed_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_packed_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_packed_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Packed",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_1 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_to_be_shipped_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_shipped_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_shipped_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Shipped",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_2 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_to_be_delivered_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_delivered_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_delivered_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Delivered",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_3 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    inventory_summary_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    inventory_summary_title = customtkinter.CTkLabel(
        inventory_summary_frame,
        text="Inventory Summary",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    total_quantity_in_hand_1 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text=str(fetch_total_quantity_in_hand_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_quantity_in_hand_2 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text="Quantity In Hand",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_4 = customtkinter.CTkFrame(
        inventory_summary_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_quantity_to_be_received_1 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text=str(fetch_total_quantity_to_be_received_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_quantity_to_be_received_2 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text="Quantity To be Received",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_5 = customtkinter.CTkFrame(
        inventory_summary_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    product_details_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    product_details_title = customtkinter.CTkLabel(
        product_details_frame,
        text="Product Details",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    low_stock_items_1 = customtkinter.CTkLabel(
        master=product_details_frame,
        text=str(fetch_low_stock_item_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    low_stock_items_2 = customtkinter.CTkLabel(
        master=product_details_frame,
        text="Low Stock Items",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_6 = customtkinter.CTkFrame(
        product_details_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    all_items_1 = customtkinter.CTkLabel(
        master=product_details_frame,
        text=str(fetch_total_items_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    all_items_2 = customtkinter.CTkLabel(
        master=product_details_frame,
        text="Total Items",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_7 = customtkinter.CTkFrame(
        product_details_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    welcome_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    sales_activity_frame.grid(row=1, column=0, padx=10, pady=10)
    inventory_summary_frame.grid(row=1, column=1, padx=10, pady=10)
    product_details_frame.grid(row=1, column=2, padx=10, pady=10)
    fig = plt.Figure()
    fig.set_facecolor('#e5e5e5')
    canvas = FigureCanvasTkAgg(fig, master=tab_0)
    canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10, columnspan=3, sticky="W")
    low_stock_vs_total_item_pie_chart(canvas)
    fig1 = plt.Figure()
    fig1.set_facecolor('#e5e5e5')
    canvas1 = FigureCanvasTkAgg(fig1, master=tab_0)
    canvas1.get_tk_widget().grid(row=2, column=1, padx=10, pady=10, columnspan=2)
    bar_chart(canvas1)


    sales_activity_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    total_to_be_packed_label_1.grid(row=1, column=0, padx=20, pady=5)
    total_to_be_packed_label_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_1.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    total_to_be_shipped_label_1.grid(row=1, column=2, padx=20, pady=5)
    total_to_be_shipped_label_2.grid(row=2, column=2, padx=20, pady=5)
    sales_activity_vertical_separator_2.grid(row=1, column=3, rowspan=2, padx=5, pady=5)
    total_to_be_delivered_label_1.grid(row=1, column=4, padx=20, pady=5)
    total_to_be_delivered_label_2.grid(row=2, column=4, padx=20, pady=5)
    # sales_activity_vertical_separator_3.grid(row=1, column=5, rowspan=2, padx=5, pady=5)

    inventory_summary_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    total_quantity_in_hand_1.grid(row=1, column=0, padx=20, pady=5)
    total_quantity_in_hand_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_4.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    total_quantity_to_be_received_1.grid(row=1, column=2, padx=20, pady=5)
    total_quantity_to_be_received_2.grid(row=2, column=2, padx=20, pady=5)
    # sales_activity_vertical_separator_5.grid(row=1, column=3, rowspan=2, padx=5, pady=5)

    product_details_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    low_stock_items_1.grid(row=1, column=0, padx=20, pady=5)
    low_stock_items_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_6.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    all_items_1.grid(row=1, column=2, padx=20, pady=5)
    all_items_2.grid(row=2, column=2, padx=20, pady=5)
    # sales_activity_vertical_separator_7.grid(row=1, column=3, rowspan=2, padx=5, pady=5)

    tab_0.columnconfigure(1, weight=1)

    user_table_frame = customtkinter.CTkFrame(master=tab_1, width=780, height=645)
    user_table_frame.place(x=430, y=20)

    user_tree = ttk.Treeview(master=user_table_frame, height=23)

    user_verscrlbar = customtkinter.CTkScrollbar(
        master=user_table_frame, orientation="vertical", command=user_tree.yview
    )
    user_verscrlbar.pack(side="right", fill="y")

    user_tree.configure(yscrollcommand=user_verscrlbar.set)
    user_tree["columns"] = (
        "USERNAME",
        "ACCESSLEVEL",
    )

    user_tree.column("#0", width=0, stretch=tk.NO)
    user_tree.column("USERNAME", anchor=tk.CENTER, width=385)
    user_tree.column("ACCESSLEVEL", anchor=tk.CENTER, width=385)

    user_tree.heading("USERNAME", text="Username")
    user_tree.heading("ACCESSLEVEL", text="Access Level")

    user_tree.pack(side="right", fill="both")

    user_tree.bind("<Double-1>", on_user_double_click)

    register_new_user_label = customtkinter.CTkLabel(
        master=tab_1,
        text="Register New User",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    reg_user = customtkinter.CTkEntry(
        master=tab_1,
        placeholder_text="Username",
        width=300,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    app.update()
    reg_user.focus_set()

    reg_password = customtkinter.CTkEntry(
        master=tab_1,
        placeholder_text="Password",
        width=300,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    reg_password.configure(show="*")

    reg_confirm_password = customtkinter.CTkEntry(
        master=tab_1,
        placeholder_text="Confirm Password",
        width=300,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    reg_confirm_password.configure(show="*")

    reg_accesslevel = customtkinter.CTkComboBox(
        master=tab_1,
        values=["Admin", "Supervisor", "Warehouse Worker"],
        width=300,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    reg_btn = customtkinter.CTkButton(
        master=tab_1,
        text="Register",
        width=250,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display", 15),
        command=register,
        hover_color="light blue",
        compound="top",
        text_color=("black", "white"),
        hover=False,
    )

    dlt_user_btn = customtkinter.CTkButton(
        master=tab_1,
        text="Delete",
        width=250,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display", 15),
        command=delete_user_record,
        hover_color="light blue",
        compound="top",
        text_color=("black", "white"),
        hover=False,
    )

    register_new_user_label.grid(row=0, column=0, padx=30, pady=10, sticky="w")
    reg_user.grid(row=1, column=0, padx=30, pady=10, sticky="w")
    reg_password.grid(row=2, column=0, padx=30, pady=10, sticky="w")
    reg_confirm_password.grid(row=3, column=0, padx=30, pady=10, sticky="w")
    reg_accesslevel.grid(row=4, column=0, padx=30, pady=10, sticky="w")
    reg_btn.grid(row=5, column=0, padx=30, pady=10, sticky="ns")
    dlt_user_btn.grid(row=6, column=0, padx=30, pady=10, sticky="ns")

    style = ThemedStyle()
    style.set_theme("equilux")
    style.configure(
        "Treeview",
        font=("SF Pro Display", 10),
        rowheight=24,
        foreground="white",
        background="#2a2d2e",
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", "#22559b")])
    style.configure(
        "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
    )
    style.map("Treeview.Heading", background=[("active", "#3484F0")])
    style.configure(
        "DateEntry",
        font=customtkinter.CTkFont(("SF Pro Display"), 12),
        foreground="white",
        background="#2a2d2e",
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
    )

    product_table_frame = customtkinter.CTkFrame(master=tab_4, width=1280, height=515)
    product_table_frame.place(x=0, y=205)

    product_tree = ttk.Treeview(master=product_table_frame, height=20)

    product_verscrlbar = customtkinter.CTkScrollbar(
        master=product_table_frame, orientation="vertical", command=product_tree.yview
    )
    product_verscrlbar.pack(side="right", fill="y")

    product_tree.configure(yscrollcommand=product_verscrlbar.set)
    product_tree["columns"] = (
        "PRODUCTID",
        "PRODUCTNAME",
        "PRODUCTQUANTITY",
        "PRODUCTDESCRIPTION",
        "PRODUCTMINSTOCK",
    )

    product_tree.column("#0", width=0, stretch=tk.NO)
    product_tree.column("PRODUCTID", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTNAME", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTQUANTITY", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTDESCRIPTION", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTMINSTOCK", anchor=tk.CENTER, width=250)

    product_tree.heading("PRODUCTID", text="ID", command=lambda: sort_treeview_column(product_tree, "PRODUCTID", False))
    product_tree.heading("PRODUCTNAME", text="Name")
    product_tree.heading("PRODUCTQUANTITY", text="Quantity")
    product_tree.heading("PRODUCTDESCRIPTION", text="Description")
    product_tree.heading("PRODUCTMINSTOCK", text="Min. Stock")

    product_tree.pack(side="bottom", fill="both")
    product_tree.bind("<Double-1>", on_product_double_click)
    product_tree.bind("<ButtonRelease>", display_product_record)

    search_entry = customtkinter.CTkEntry(tab_4,placeholder_text="Search", width=1050,)
    search_entry.grid(row=1,column=0, padx=10, pady=10)
    search_entry.bind("<KeyRelease>", search_product)

    product_menu_frame = customtkinter.CTkFrame(
        master=tab_4,
        border_width=2
    )

    insert_product_data_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Insert New Product",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    product_id_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product ID:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_id_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="ID",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_name_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Name:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_name_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Item",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_quantity_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Quantity:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_quantity_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Quantity",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_description_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Description:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_description_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Description",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_min_stock_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Min. Stock:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_min_stock_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Min. Stock",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    addproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Add Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=add_new_product_details,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    editproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Edit Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=edit_product_details,
        compound="top",
        corner_radius=200,
        fg_color="#ADD8E6",
        text_color="black",
    )

    deleteproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Delete Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=delete_product_record,
        compound="top",
        corner_radius=200,
        fg_color="#ff666d",
        text_color="black",
    )

    product_menu_frame.grid(row=0, column=0)

    insert_product_data_label.grid(
        row=0, column=0, sticky="w", padx=5, pady=5, columnspan=2
    )

    product_id_entry_label.grid(row=1, column=0, padx=5)
    product_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    product_name_entry_label.grid(row=1, column=2, padx=5)
    product_name_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    product_quantity_entry_label.grid(row=1, column=4, padx=5)
    product_quantity_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")
    product_description_entry_label.grid(row=2, column=0, padx=5)
    product_description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    product_min_stock_entry_label.grid(row=2, column=2, padx=5)
    product_min_stock_entry.grid(row=2, column=3, padx=5, pady=5)

    addproduct_btn.grid(row=3, column=0, padx=20, pady=5, columnspan=2)
    editproduct_btn.grid(row=3, column=2, padx=20, pady=5, columnspan=2)
    deleteproduct_btn.grid(row=3, column=4, padx=20, pady=5, columnspan=2)

    tab_4.columnconfigure(0,weight=1)

    add_to_user_table()
    add_to_product_table()


def supervisor_dashboard(username):
    def fetch_to_be_packed_data():
        total_to_be_packed = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Packed",))
        to_be_packed_data = cursor.fetchone()[0]
        total_to_be_packed += to_be_packed_data
        conn.commit()
        conn.close()
        return total_to_be_packed

    def update_to_be_packed_label():
        new_count = fetch_to_be_packed_data()
        total_to_be_packed_label_1.configure(text=str(new_count))

    def fetch_to_be_shipped_data():
        total_to_be_shipped = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Shipped",))
        to_be_shipped_data = cursor.fetchone()[0]
        total_to_be_shipped += to_be_shipped_data
        conn.commit()
        conn.close()
        return total_to_be_shipped

    def update_to_be_shipped_label():
        new_count = fetch_to_be_shipped_data()
        total_to_be_shipped_label_1.configure(text=str(new_count))

    def fetch_to_be_delivered_data():
        total_to_be_delivered = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Delivered",))
        to_be_delivered_data = cursor.fetchone()[0]
        total_to_be_delivered += to_be_delivered_data
        conn.commit()
        conn.close()
        return total_to_be_delivered

    def update_to_be_delivered_label():
        new_count = fetch_to_be_delivered_data()
        total_to_be_delivered_label_1.configure(text=str(new_count))

    def fetch_total_quantity_in_hand_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(PRODUCT_QUANTITY) FROM PRODUCT")
        total_quantity_in_hand = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_quantity_in_hand

    def update_total_quantity_in_hand_label():
        new_count = fetch_total_quantity_in_hand_data()
        total_quantity_in_hand_1.configure(text=str(new_count))

    def fetch_total_quantity_to_be_received_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(PURCHASE_ORDER_PRODUCT_QUANTITY) FROM PURCHASE_ORDER WHERE PURCHASE_ORDER_STATUS = ?", ("To be Received",))
        total_quantity_to_be_received = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_quantity_to_be_received

    def update_total_quantity_to_be_received_label():
        new_count = fetch_total_quantity_to_be_received_data()
        total_quantity_to_be_received_1.configure(text=str(new_count))

    def fetch_low_stock_item_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT WHERE PRODUCT_QUANTITY < PRODUCT_MIN_STOCK")
        low_stock_items = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return low_stock_items

    def update_low_stock_item_label():
        new_count = fetch_low_stock_item_data()
        low_stock_items_1.configure(text=str(new_count))

    def fetch_total_items_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT")
        total_items = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_items

    def update_total_items_label():
        new_count = fetch_total_items_data()
        all_items_1.configure(text=str(new_count))

    def fetch_customer_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CUSTOMER")
        customer = cursor.fetchall()
        conn.commit()
        conn.close()
        return customer

    def clear_customer_entry_field():
        customer_name_entry.delete(0, END)
        customer_email_entry.delete(0, END)
        customer_contact_entry.delete(0, END)

    def display_customer_record(event):
        selected_item = customer_tree.focus()
        if selected_item:
            clear_customer_entry_field()
            row = customer_tree.item(selected_item)["values"]
            customer_name_entry.insert(0, row[1])
            customer_email_entry.insert(0, row[2])
            customer_contact_entry.insert(0, row[3])

    def fetch_customer_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CUSTOMER_ID) FROM CUSTOMER")
        last_customer_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_customer_id

    def generate_customer_id(prefix="CUST"):
        last_customer_id = fetch_customer_last_id()
        if last_customer_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_customer_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def add_to_customer_table():
        customers = fetch_customer_data()
        customer_tree.delete(*customer_tree.get_children())
        for customer in customers:
            customer_tree.insert("", END, values=customer)

    def check_existing_customer(customer_check):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT CUSTOMER_NAME FROM CUSTOMER WHERE CUSTOMER_NAME = ?",
            (customer_check,),
        )
        existing_customer = cursor.fetchone()
        conn.commit()
        conn.close()
        return existing_customer

    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    def is_valid_contact_number(contact_number):
        return contact_number.isdigit()

    def add_new_customer_details():
        customer_id = generate_customer_id("CUST")
        customer_name = customer_name_entry.get()
        customer_email = customer_email_entry.get()
        customer_contactno = customer_contact_entry.get()

        if not (customer_name and customer_email and customer_contactno):
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not is_valid_email(customer_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not is_valid_contact_number(customer_contactno):
            messagebox.showerror("Error", "Contact number must be only digits")
            return

        if not check_existing_customer(customer_name):
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO CUSTOMER (CUSTOMER_ID,CUSTOMER_NAME,CUSTOMER_EMAIL,CUSTOMER_TEL) \
                VALUES (?,?,?,?)",
                (customer_id, customer_name, customer_email, customer_contactno),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
        else:
            messagebox.showerror(
                "Warning", "Duplicate customer! Please enter new customer."
            )
        add_to_customer_table()
        clear_customer_entry_field()
        return

    def edit_customer_details():
        selected_customer_details = customer_tree.focus()
        if not selected_customer_details:
            messagebox.showerror("Error", "Please select a record to edit")
            return

        row = customer_tree.item(selected_customer_details)["values"]
        new_customer_name = customer_name_entry.get()
        new_customer_email = customer_email_entry.get()
        new_customer_contactno = customer_contact_entry.get()

        if not (new_customer_name and new_customer_email and new_customer_contactno):
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not is_valid_email(new_customer_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not is_valid_contact_number(new_customer_contactno):
            messagebox.showerror("Error", "Contact number must be only digits")
            return

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE CUSTOMER SET CUSTOMER_NAME = ?, CUSTOMER_EMAIL = ?, CUSTOMER_TEL = ? WHERE CUSTOMER_NAME = ?",
            (new_customer_name, new_customer_email, new_customer_contactno, row[1]),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")
        add_to_customer_table()
        clear_customer_entry_field()

    def delete_customer_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = customer_tree.focus()
        row = customer_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM CUSTOMER WHERE CUSTOMER_NAME= ?", (row[1],))
        conn.commit()
        conn.close()
        add_to_customer_table()
        clear_customer_entry_field()

    def delete_customer_record():
        selected_item = customer_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_customer_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    def fetch_product_to_list():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT PRODUCT_NAME FROM PRODUCT")
        products = cursor.fetchall()
        product = []
        for x in products:
            product.append(x[0])
        conn.commit()
        conn.close()
        return product

    def on_customer_double_click(event):

        selected_item = customer_tree.selection()[0]
        values = customer_tree.item(selected_item, "values")

        def fetch_selected_customer_details():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM CUSTOMER WHERE CUSTOMER_NAME = ?", (values[1],)
            )
            customer_details = cursor.fetchall()
            conn.commit()
            conn.close()
            return customer_details

        def add_new_sale_order():
            sale_order_id = generate_sale_order_id("SO")
            sale_order_date = date.today().strftime("%m/%d/%Y")
            customer_name = values[1]

            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO SALE_ORDER (SALE_ORDER_ID,SALE_ORDER_DATE,SALE_ORDER_CUSTOMER,SALE_ORDER_STATUS) \
            VALUES (?,?,?,?)",
                (sale_order_id, sale_order_date, customer_name, "To be packed"),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
            add_to_sale_order_table()
            return

        sales_window = customtkinter.CTk()
        sales_window.title("Product Details")

        customer_id_label = customtkinter.CTkLabel(
            sales_window,
            text="Customer ID:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_id_label_details = customtkinter.CTkLabel(
            sales_window,
            text=f"{values[0]}",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_name_label = customtkinter.CTkLabel(
            sales_window,
            text="Customer Name:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_name_label_details = customtkinter.CTkLabel(
            sales_window,
            text=f"{values[1]}",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_email_label = customtkinter.CTkLabel(
            sales_window,
            text="Customer Email:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_email_label_details = customtkinter.CTkLabel(
            sales_window,
            text=f"{values[2]}",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_contact_label = customtkinter.CTkLabel(
            sales_window,
            text="Customer Contact No.:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_contact_label_details = customtkinter.CTkLabel(
            sales_window,
            text=f"{values[3]}",
            font=customtkinter.CTkFont("SF Pro Display"),
        )

        sales_quantity_label = customtkinter.CTkLabel(
            sales_window,
            text="Purchase Quantity:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        sales_quantity_entry = customtkinter.CTkEntry(
            master=sales_window,
            placeholder_text="Name",
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display"),
            border_width=0,
        )

        product_selection_label = customtkinter.CTkLabel(
            sales_window,
            text="Product to be purchase:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        product_selection_entry = customtkinter.CTkComboBox(
            master=sales_window,
            values=fetch_product_to_list(),
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display"),
            border_width=0,
        )

        sales_btn = customtkinter.CTkButton(
            master=sales_window,
            text="Create Sales Order",
            width=150,
            height=50,
            command=add_new_sale_order,
            font=customtkinter.CTkFont("SF Pro Display"),
            corner_radius=200,
            fg_color="#007FFF",
            text_color="black",
        )

        customer_id_label.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=5)
        customer_id_label_details.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        customer_name_label.grid(row=1, column=0, sticky=W, padx=(10, 5), pady=5)
        customer_name_label_details.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        customer_email_label.grid(row=2, column=0, sticky=W, padx=(10, 5), pady=5)
        customer_email_label_details.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        customer_contact_label.grid(row=3, column=0, sticky=W, padx=(10, 5), pady=5)
        customer_contact_label_details.grid(row=3, column=1, sticky=W, padx=5, pady=5)

        # sales_quantity_label.grid(row=4, column=0, sticky=W, padx=(10, 5), pady=5)
        # sales_quantity_entry.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        # product_selection_label.grid(row=5, column=0, sticky=W, padx=(10, 5), pady=5)
        # product_selection_entry.grid(row=5, column=1, sticky=W, padx=5, pady=5)
        sales_btn.grid(row=6, column=0, columnspan=2, pady=20)

        sales_window.columnconfigure(0, weight=1)
        sales_window.columnconfigure(1, weight=1)
        sales_window.columnconfigure(2, weight=1)
        sales_window.columnconfigure(3, weight=1)
        sales_window.columnconfigure(4, weight=1)
        sales_window.columnconfigure(5, weight=1)
        sales_window.columnconfigure(6, weight=1)

        sales_window.mainloop()

    def fetch_supplier_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SUPPLIER")
        supplier = cursor.fetchall()
        conn.commit()
        conn.close()
        return supplier

    def add_to_supplier_table():
        suppliers = fetch_supplier_data()
        supplier_tree.delete(*supplier_tree.get_children())
        for supplier in suppliers:
            supplier_tree.insert("", END, values=supplier)

    def clear_supplier_entry_field():
        supplier_name_entry.delete(0, END)
        supplier_email_entry.delete(0, END)
        supplier_contact_entry.delete(0, END)

    def display_supplier_record(event):
        selected_item = supplier_tree.focus()
        if selected_item:
            clear_supplier_entry_field()
            row = supplier_tree.item(selected_item)["values"]
            supplier_name_entry.insert(0, row[1])
            supplier_email_entry.insert(0, row[2])
            supplier_contact_entry.insert(0, row[3])

    def check_existing_supplier(supplier_check):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUPPLIER_NAME FROM SUPPLIER WHERE SUPPLIER_NAME = ?",
            (supplier_check,),
        )
        existing_supplier = cursor.fetchone()
        conn.commit()
        conn.close()
        return existing_supplier

    def fetch_supplier_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(SUPPLIER_ID ) FROM SUPPLIER")
        last_supplier_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_supplier_id

    def generate_supplier_id(prefix="SUPP"):
        last_supplier_id = fetch_supplier_last_id()
        if last_supplier_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_supplier_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def add_new_supplier_details():
        supplier_id = generate_supplier_id("SUPP")
        supplier_name = supplier_name_entry.get()
        supplier_email = supplier_email_entry.get()
        supplier_contactno = supplier_contact_entry.get()

        if not (supplier_name and supplier_email and supplier_contactno):
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not is_valid_email(supplier_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not is_valid_contact_number(supplier_contactno):
            messagebox.showerror("Error", "Contact number must be only digits")
            return

        if not check_existing_supplier(supplier_name):
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO SUPPLIER (SUPPLIER_ID,SUPPLIER_NAME,SUPPLIER_EMAIL,SUPPLIER_TEL) \
                VALUES (?,?,?,?)",
                (supplier_id, supplier_name, supplier_email, supplier_contactno),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
        else:
            messagebox.showerror(
                "Warning", "Duplicate supplier! Please enter new supplier."
            )

        add_to_supplier_table()
        clear_supplier_entry_field()
        return

    def edit_supplier_details():
        selected_supplier_details = supplier_tree.focus()
        if not selected_supplier_details:
            messagebox.showerror("Error", "Please select a record to edit")
            return

        row = supplier_tree.item(selected_supplier_details)["values"]
        new_supplier_name = supplier_name_entry.get()
        new_supplier_email = supplier_email_entry.get()
        new_supplier_contactno = supplier_contact_entry.get()

        if not (new_supplier_name and new_supplier_email and new_supplier_contactno):
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not is_valid_email(new_supplier_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not is_valid_contact_number(new_supplier_contactno):
            messagebox.showerror("Error", "Contact number must be only digits")
            return

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE SUPPLIER SET SUPPLIER_NAME = ?, SUPPLIER_EMAIL = ?, SUPPLIER_TEL = ? WHERE SUPPLIER_NAME = ?",
            (new_supplier_name, new_supplier_email, new_supplier_contactno, row[1]),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")

        add_to_supplier_table()
        clear_supplier_entry_field()

    def delete_supplier_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = supplier_tree.focus()
        row = supplier_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM SUPPLIER WHERE SUPPLIER_NAME= ?", (row[1],))
        conn.commit()
        conn.close()
        add_to_supplier_table()
        clear_supplier_entry_field()

    def delete_supplier_record():
        selected_item = supplier_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_supplier_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    def fetch_product_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PRODUCT")
        product = cursor.fetchall()
        conn.commit()
        conn.close()
        return product

    def add_to_product_table():
        products = fetch_product_data()
        product_tree.delete(*product_tree.get_children())
        for product in products:
            product_tree.insert("", END, values=product)

    def clear_product_entry_field():
        product_id_entry.delete(0, END)
        product_name_entry.delete(0, END)
        product_quantity_entry.delete(0, END)
        product_description_entry.delete(0, END)
        product_min_stock_entry.delete(0, END)

    def display_product_record(event):
        selected_item = product_tree.focus()
        if selected_item:
            clear_product_entry_field()
            row = product_tree.item(selected_item)["values"]
            product_id_entry.insert(0, [row[0]])
            product_name_entry.insert(0, row[1])
            product_quantity_entry.insert(0, row[2])
            product_description_entry.insert(0, row[3])
            product_min_stock_entry.insert(0, [row[4]])

    def check_existing_product(product_check):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUPPLIER_NAME FROM SUPPLIER WHERE SUPPLIER_NAME = ?",
            (product_check,),
        )
        existing_supplier = cursor.fetchone()
        conn.commit()
        conn.close()
        return existing_supplier

    def add_new_product_details():
        product_id = product_id_entry.get()
        product_name = product_name_entry.get()
        product_quantity = product_quantity_entry.get()
        product_description = product_description_entry.get()
        product_min_stock = product_min_stock_entry.get()

        if not (product_name and product_quantity and product_description):
            messagebox.showerror("Error", "Please enter all fields")
            return
        elif not check_existing_product(product_name):
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PRODUCT (PRODUCT_ID,PRODUCT_NAME,PRODUCT_QUANTITY,PRODUCT_STATUS,PRODUCT_MIN_STOCK) \
            VALUES (?,?,?,?,?)",
                (
                    product_id,
                    product_name,
                    product_quantity,
                    product_description,
                    product_min_stock,
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
        else:
            messagebox.showerror(
                "Warning", "Duplicate customer! Please enter new customer."
            )
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()
        return

    def edit_product_details():
        selected_product_details = product_tree.focus()
        if not selected_product_details:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = product_tree.item(selected_product_details)["values"]
        new_product_id = product_id_entry.get()
        new_product_name = product_name_entry.get()
        new_product_quantity = product_quantity_entry.get()
        new_product_description = product_description_entry.get()
        new_product_min_stock = product_min_stock_entry.get()
        if not new_product_name:
            messagebox.showerror("Error", "Please enter all fields")
            return
        else:
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE PRODUCT SET PRODUCT_ID = ?, PRODUCT_NAME = ?, PRODUCT_QUANTITY = ?, PRODUCT_STATUS = ?, PRODUCT_MIN_STOCK = ? WHERE PRODUCT_NAME = ?",
                (
                    new_product_id,
                    new_product_name,
                    new_product_quantity,
                    new_product_description,
                    new_product_min_stock,
                    row[1],
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record successfully edited")
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def delete_product_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = product_tree.focus()
        row = product_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM PRODUCT WHERE PRODUCT_NAME= ?", (row[1],))
        conn.commit()
        conn.close()
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def delete_product_record():
        selected_item = product_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_product_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    def search_product(event):
        search_term = search_entry.get().lower()
        products = fetch_product_data()
        product_tree.delete(*product_tree.get_children())
        for product in products:
            if search_term in str(product).lower():
                product_tree.insert("", tk.END, values=product)

    def on_product_double_click(event):

        selected_item = product_tree.selection()[0]
        values = product_tree.item(selected_item, "values")

        def fetch_selected_product_details():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCT WHERE PRODUCT_NAME = ?", (values[1],))
            product_details = cursor.fetchall()
            conn.commit()
            conn.close()
            return product_details

        new_window = customtkinter.CTk()
        new_window.title("Product Details")
        # new_window.geometry("500x400")

        def add_incoming_stock():
            incoming_stock_id = generate_purchase_order_id("PO")
            incoming_stock_product = values[1]
            incoming_stock_quantity = restock_quantity_entry.get()
            incoming_stock_status = "To be Received"

            if not incoming_stock_quantity:
                messagebox.showerror("Error", "Please enter all fields")
                return

            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PURCHASE_ORDER (PURCHASE_ORDER_ID,PURCHASE_ORDER_PRODUCT,PURCHASE_ORDER_PRODUCT_QUANTITY,PURCHASE_ORDER_STATUS) \
            VALUES (?,?,?,?)",
                (
                    incoming_stock_id,
                    incoming_stock_product,
                    incoming_stock_quantity,
                    incoming_stock_status,
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
            add_to_incoming_stock_table()
            fetch_tbr_quantity()
            update_total_quantity_in_hand_label()
            update_total_quantity_to_be_received_label()
            new_window.destroy()

        def fetch_tbr_quantity():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT PURCHASE_ORDER_PRODUCT_QUANTITY FROM PURCHASE_ORDER WHERE PURCHASE_ORDER_PRODUCT = ? AND PURCHASE_ORDER_STATUS=?",
                (values[1], "To be Received"),
            )
            incoming_stock_quantity = cursor.fetchall()
            tbr = 0
            for x in incoming_stock_quantity:
                tbr += x[0]
            conn.commit()
            conn.close()
            return tbr

        def fetch_tbs_quantity():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT SALE_ORDER_PRODUCT_QUANTITY FROM SALE_ORDER_PRODUCT WHERE SALE_ORDER_PRODUCT = ?",
                (values[1],),
            )
            outgoing_stock_quantity = cursor.fetchall()
            tbs = 0
            for x in outgoing_stock_quantity:
                tbs += x[0]
            conn.commit()
            conn.close()
            return tbs

        product_details_frame = customtkinter.CTkFrame(new_window, border_width=2)
        product_details_title = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Details",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        product_id_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product ID:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_id_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[0]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_name_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Name:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_name_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[1]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_quantity_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Quantity:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_quantity_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[2]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_description_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Description:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_description_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[3]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )

        restock_frame = customtkinter.CTkFrame(new_window, border_width=2)
        restock_title = customtkinter.CTkLabel(
            restock_frame,
            text="Restock",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        restock_quantity_label = customtkinter.CTkLabel(
            restock_frame,
            text="Restock Quantity:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        restock_quantity_entry = customtkinter.CTkEntry(
            master=restock_frame,
            placeholder_text="Quantity",
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display", size=13),
            border_width=0,
        )

        restock_btn = customtkinter.CTkButton(
            master=restock_frame,
            text="Restock",
            command=add_incoming_stock,
            font=customtkinter.CTkFont("SF Pro Display", size=13),
            corner_radius=200,
            fg_color="#007FFF",
            text_color="black",
        )

        status_frame = customtkinter.CTkFrame(new_window, border_width=2)
        status_details_title = customtkinter.CTkLabel(
            status_frame,
            text="Status",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        total_tbs = customtkinter.CTkFrame(
            master=status_frame, width=100, height=100, fg_color="transparent"
        )
        total_tbs_details_1 = customtkinter.CTkLabel(
            total_tbs,
            text=(str(fetch_tbs_quantity()) + " Qty"),
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        total_tbs_details_2 = customtkinter.CTkLabel(
            total_tbs,
            text="To be Shipped",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        vertical_separator = customtkinter.CTkFrame(
            status_frame, width=2, height=80, fg_color="#CCCCCC"
        )
        total_tbr = customtkinter.CTkFrame(
            master=status_frame, width=100, height=100, fg_color="transparent"
        )
        total_tbr_details_1 = customtkinter.CTkLabel(
            total_tbr,
            text=(str(fetch_tbr_quantity()) + " Qty"),
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        total_tbr_details_2 = customtkinter.CTkLabel(
            total_tbr,
            text="To be Received",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )

        product_details_frame.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        product_details_title.grid(
            row=0, column=0, columnspan=2, sticky=W, padx=10, pady=10
        )
        product_id_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        product_id_label_details.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        product_name_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        product_name_label_details.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        product_quantity_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
        product_quantity_label_details.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        product_description_label.grid(row=4, column=0, sticky=W, padx=5, pady=5)
        product_description_label_details.grid(
            row=4, column=1, sticky=W, padx=5, pady=5
        )

        restock_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        restock_title.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        restock_quantity_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        restock_quantity_entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        restock_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        status_frame.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        status_details_title.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        total_tbs.grid(row=1, column=0, rowspan=5, padx=15, pady=15)
        total_tbs_details_1.pack(side=TOP)
        total_tbs_details_2.pack(side=BOTTOM)
        vertical_separator.grid(row=1, column=1, rowspan=5, pady=36)
        total_tbr.grid(row=1, column=3, rowspan=5, padx=15, pady=15)
        total_tbr_details_1.pack(side=TOP)
        total_tbr_details_2.pack(side=BOTTOM)

        new_window.mainloop()

    def fetch_task_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT TASK_ID,TASK_DESCRIPTION,TASK_ASSIGNED_TO,TASK_STATUS,TASK_DUE_DATE FROM TASK"
        )
        task = cursor.fetchall()
        conn.commit()
        conn.close()
        return task

    def fetch_worker_to_list():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT USERNAME FROM USER WHERE ACCESSLEVEL = 2")
        workers = cursor.fetchall()
        worker = []
        for x in workers:
            worker.append(x[0])
        conn.commit()
        conn.close()
        return worker

    def update_workers_to_list():
        workers = fetch_worker_to_list()
        assigned_worker_entry.configure(values=workers)

    def add_to_task_table():
        tasks = fetch_task_data()
        task_tree.delete(*task_tree.get_children())
        for task in tasks:
            task_tree.insert("", END, values=task, tags=task)

    def fetch_task_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(TASK_ID) FROM TASK")
        last_task_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_task_id

    def generate_task_id(prefix="TASK"):
        last_task_id = fetch_task_last_id()
        if last_task_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_task_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def add_new_task_details():
        task_id = generate_task_id("TASK")
        task_name = task_entry.get()
        assigned_worker = assigned_worker_entry.get()
        task_due_date = task_due_date_entry.get()

        if not (task_name):
            messagebox.showerror("Error", "Please enter all fields")
            return
        else:
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO TASK (TASK_ID,TASK_DESCRIPTION,TASK_ASSIGNED_TO,TASK_STATUS,TASK_DUE_DATE) \
            VALUES (?,?,?,?,?)",
                (task_id, task_name, assigned_worker, "Pending", task_due_date),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
        add_to_task_table()
        return

    def edit_task_details():
        selected_task_details = task_tree.focus()
        if not selected_task_details:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = task_tree.item(selected_task_details)["values"]
        new_task = task_entry.get()
        new_assigned_worker = assigned_worker_entry.get()
        new_due_date = task_due_date_entry.get()
        if not new_task:
            messagebox.showerror("Error", "Please enter all fields")
            return
        else:
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE TASK SET TASK_DESCRIPTION = ?, TASK_ASSIGNED_TO = ?, TASK_DUE_DATE = ? WHERE TASK_DESCRIPTION = ?",
                (new_task, new_assigned_worker, new_due_date, row[0]),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record successfully edited")
        add_to_task_table()

    def delete_task_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = task_tree.focus()
        row = task_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM TASK WHERE TASK_DESCRIPTION= ?", (row[0],))
        conn.commit()
        conn.close()
        add_to_task_table()

    def delete_task_record():
        selected_item = task_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_task_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    def fetch_purchase_order_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(PURCHASE_ORDER_ID) FROM PURCHASE_ORDER")
        last_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_id

    def generate_purchase_order_id(prefix="PO"):
        last_id = fetch_purchase_order_last_id()
        if last_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def fetch_incoming_stock_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PURCHASE_ORDER")
        incoming_stock = cursor.fetchall()
        conn.commit()
        conn.close()
        return incoming_stock

    def add_to_incoming_stock_table():
        incoming_stocks = fetch_incoming_stock_data()
        incoming_stock_tree.delete(*incoming_stock_tree.get_children())
        for incoming_stock in incoming_stocks:
            incoming_stock_tree.insert(
                "", END, values=incoming_stock, tags=incoming_stock
            )

    def update_purchase_order_status():
        new_status = purchase_order_status_entry.get()
        selected = incoming_stock_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = incoming_stock_tree.item(selected)["values"]
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE PURCHASE_ORDER SET PURCHASE_ORDER_STATUS = ? WHERE PURCHASE_ORDER_ID = ?",
            (new_status, row[0]),
        )
        if new_status == "Received":
            cursor.execute(
                "UPDATE PRODUCT SET PRODUCT_QUANTITY = PRODUCT_QUANTITY + ? WHERE PRODUCT_NAME = ?",
                (row[2], row[1]),
            )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")
        add_to_incoming_stock_table()
        add_to_product_table()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def fetch_sale_order_stock_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SALE_ORDER")
        sale_order = cursor.fetchall()
        conn.commit()
        conn.close()
        return sale_order

    def add_to_sale_order_table():
        outgoing_stocks = fetch_sale_order_stock_data()
        outgoing_stock_tree.delete(*outgoing_stock_tree.get_children())
        for outgoing_stock in outgoing_stocks:
            outgoing_stock_tree.insert("", END, values=outgoing_stock)

    def update_sales_order_status():
        new_status = sales_order_status_entry.get()
        selected = outgoing_stock_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = outgoing_stock_tree.item(selected)["values"]
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE SALE_ORDER SET SALE_ORDER_STATUS = ? WHERE SALE_ORDER_ID = ?",
            (new_status, row[0]),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")
        add_to_sale_order_table()
        add_to_product_table()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()


    def fetch_sale_order_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(SALE_ORDER_ID) FROM SALE_ORDER")
        last_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_id

    def generate_sale_order_id(prefix="SO"):
        last_id = fetch_sale_order_last_id()
        if last_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def on_sale_order_double_click(event):
        selected_item = outgoing_stock_tree.selection()[0]
        values = outgoing_stock_tree.item(selected_item, "values")

        sale_order_window = customtkinter.CTk()
        sale_order_window.title("Product Details")

        product_selection_frame = customtkinter.CTkFrame(
            master=sale_order_window, border_width=2
        )

        sale_order_product_table_frame = customtkinter.CTkFrame(
            master=sale_order_window
        )

        def fetch_sale_order_status(sale_order_id):
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SALE_ORDER_STATUS FROM SALE_ORDER WHERE SALE_ORDER_ID = ?", (sale_order_id,))
            status = cursor.fetchone()
            conn.close()
            return status[0] if status else None
        def fetch_sale_order_product_data():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM SALE_ORDER_PRODUCT WHERE SALE_ORDER_ID = ?", (values[0],)
            )
            sale_order = cursor.fetchall()
            conn.commit()
            conn.close()
            return sale_order

        def add_to_sale_order_product_table():
            sale_order_products = fetch_sale_order_product_data()
            sale_order_product_tree.delete(*sale_order_product_tree.get_children())
            for sale_order_product in sale_order_products:
                sale_order_product_tree.insert("", END, values=sale_order_product)

        def add_sale_order_product():
            sale_order_id = values[0]
            sale_order_product = product_selection_entry.get()
            sale_order_product_quantity = sales_quantity_entry.get()

            sale_order_status = fetch_sale_order_status(sale_order_id)
            if sale_order_status != "To be Packed":
                messagebox.showerror("Error", "Sale order status is not 'To be Packed'. Cannot add more products.")
                return

            if not sale_order_product_quantity:
                messagebox.showerror("Error", "Please enter all fields")
                return
            else:
                conn = sqlite3.connect("Inventory Management System.db")
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT PRODUCT_QUANTITY FROM PRODUCT WHERE PRODUCT_NAME = ?", (sale_order_product,),
                )
                product_quantity = cursor.fetchone()[0]
                if product_quantity < int(sale_order_product_quantity):
                    messagebox.showerror("Error", "Insufficient quantity")
                    return
                else:
                    conn = sqlite3.connect("Inventory Management System.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO SALE_ORDER_PRODUCT (SALE_ORDER_ID,SALE_ORDER_PRODUCT,SALE_ORDER_PRODUCT_QUANTITY) \
                    VALUES (?,?,?)",
                        (sale_order_id, sale_order_product, sale_order_product_quantity),
                    )
                    cursor.execute(
                        "UPDATE PRODUCT SET PRODUCT_QUANTITY = PRODUCT_QUANTITY - ? WHERE PRODUCT_NAME = ?",
                        (sale_order_product_quantity, sale_order_product),
                    )
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Data has been inserted")
            add_to_sale_order_product_table()
            add_to_product_table()
            update_low_stock_item_label()
            return

        select_product_label = customtkinter.CTkLabel(
            product_selection_frame,
            text="Select Product",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )

        product_selection_label = customtkinter.CTkLabel(
            product_selection_frame,
            text="Product to be purchase:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        product_selection_entry = customtkinter.CTkComboBox(
            master=product_selection_frame,
            values=fetch_product_to_list(),
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display"),
            border_width=0,
        )
        sales_quantity_label = customtkinter.CTkLabel(
            product_selection_frame,
            text="Purchase Quantity:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        sales_quantity_entry = customtkinter.CTkEntry(
            master=product_selection_frame,
            placeholder_text="Quantity",
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display"),
            border_width=0,
        )
        sales_btn = customtkinter.CTkButton(
            master=product_selection_frame,
            text="Add Item",
            command=add_sale_order_product,
            font=customtkinter.CTkFont("SF Pro Display"),
            corner_radius=200,
            fg_color="#007FFF",
            text_color="black",
        )

        style1 = ThemedStyle()
        style1.set_theme("equilux")
        style1.configure(
            "Treeview",
            font=("SF Pro Display", 10),
            rowheight=24,
            foreground="white",
            background="#2a2d2e",
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
        )
        style1.map("Treeview", background=[("selected", "#22559b")])
        style1.configure(
            "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
        )
        style1.map("Treeview.Heading", background=[("active", "#3484F0")])
        style1.configure(
            "DateEntry",
            font=customtkinter.CTkFont("SF Pro Display", 12),
            foreground="white",
            background="#2a2d2e",
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
        )

        sale_order_product_tree = ttk.Treeview(
            master=sale_order_product_table_frame, height=30
        )

        sale_order_product_verscrlbar = customtkinter.CTkScrollbar(
            master=sale_order_product_table_frame,
            orientation="vertical",
            command=sale_order_product_tree.yview,
        )
        sale_order_product_verscrlbar.pack(side="right", fill="y")

        sale_order_product_tree.configure(
            yscrollcommand=sale_order_product_verscrlbar.set
        )
        sale_order_product_tree["columns"] = (
            "SALEORDERID",
            "SALEORDERPRODUCT",
            "SALEORDERPRODUCTQUANTITY",
        )

        sale_order_product_tree.column("#0", width=0, stretch=tk.NO)
        sale_order_product_tree.column("SALEORDERID", anchor=tk.CENTER, width=200)
        sale_order_product_tree.column("SALEORDERPRODUCT", anchor=tk.CENTER, width=200)
        sale_order_product_tree.column("SALEORDERPRODUCTQUANTITY", anchor=tk.CENTER, width=200)

        sale_order_product_tree.heading("SALEORDERID", text="ID")
        sale_order_product_tree.heading("SALEORDERPRODUCT", text="Item")
        sale_order_product_tree.heading("SALEORDERPRODUCTQUANTITY", text="Quantity")

        sale_order_product_tree.pack(side="bottom", fill="both")

        product_selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
        select_product_label.grid(row=0, column=0, padx=10, pady=10)
        product_selection_label.grid(row=1, column=0, padx=10, pady=10)
        product_selection_entry.grid(row=1, column=1, padx=10, pady=10)
        sales_quantity_label.grid(row=2, column=0, padx=10, pady=10)
        sales_quantity_entry.grid(row=2, column=1, padx=10, pady=10)
        sales_btn.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        sale_order_product_table_frame.grid(row=0, column=1, padx=10, pady=10)

        add_to_sale_order_product_table()
        sale_order_window.mainloop()

    def low_stock_vs_total_item_pie_chart(canvas):
        data=[]

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT WHERE PRODUCT_QUANTITY < PRODUCT_MIN_STOCK")
        low_stock_items = cursor.fetchone()[0]
        data.append(low_stock_items)
        conn.commit()
        conn.close()

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT")
        total_items = cursor.fetchone()[0]
        data.append(total_items - low_stock_items)
        conn.commit()
        conn.close()

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#e5e5e5')  # Set the figure background color
        ax.set_facecolor('#e5e5e5')  # Set the axes background color
        ax.axis("equal")

        ax.pie(data, labels=["Low Stock", "In Stock"], autopct="%.2f%%", pctdistance=0.85)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)

        canvas.figure = fig
        canvas.draw()

    def bar_chart(canvas):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT PRODUCT_ID, PRODUCT_QUANTITY FROM PRODUCT")
        data = cursor.fetchall()
        conn.commit()
        conn.close()

        product_ids = [row[0] for row in data]
        product_quantities = [row[1] for row in data]

        fig1 = plt.Figure()
        ax = fig1.add_subplot(111)
        fig1.patch.set_facecolor('#e5e5e5')
        ax.set_facecolor('#e5e5e5')
        ax.bar(product_ids, product_quantities)
        ax.tick_params(axis='x', labelsize=5)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel('Product Name', fontsize=12)
        ax.set_ylabel('Product Quantity', fontsize=12)
        ax.set_title('Inventory', fontsize=14)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

        canvas.figure = fig1
        canvas.draw()


    def sort_treeview_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: sort_treeview_column(tv, col, not reverse))

    supervisor_dashboard_frame = customtkinter.CTkFrame(
        master=app, width=1280, height=720, border_width=0
    )
    supervisor_dashboard_frame.place(x=0, y=0)

    info_frame = customtkinter.CTkFrame(
        master=supervisor_dashboard_frame, width=1280, height=720
    )
    info_frame.place(x=0, y=0)
    info_tab = customtkinter.CTkTabview(master=info_frame, width=1280, height=720)
    info_tab.place(x=0, y=0)
    tab_0 = info_tab.add("Homepage")
    tab_1 = info_tab.add("Customer")
    tab_2 = info_tab.add("Supplier")
    tab_3 = info_tab.add("Product")
    tab_4 = info_tab.add("Task")
    tab_5 = info_tab.add("Incoming")
    tab_6 = info_tab.add("Outgoing")

    style = ThemedStyle()
    style.set_theme("equilux")
    style.configure(
        "Treeview",
        font=("SF Pro Display", 10),
        rowheight=24,
        foreground="white",
        background="#2a2d2e",
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", "#22559b")])
    style.configure(
        "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
    )
    style.map("Treeview.Heading", background=[("active", "#3484F0")])
    style.configure(
        "DateEntry",
        font=customtkinter.CTkFont(("SF Pro Display"), 12),
        foreground="white",
        background="#2a2d2e",
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
    )

    welcome_label = customtkinter.CTkLabel(
        master=tab_0,
        text=f"Hello, {username} ",
        font=customtkinter.CTkFont("SF Pro Display", 24, weight="bold"),
    )

    sales_activity_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    sales_activity_title = customtkinter.CTkLabel(
        sales_activity_frame,
        text="Sales Activity",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    total_to_be_packed_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_packed_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_packed_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Packed",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_1 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_to_be_shipped_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_shipped_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_shipped_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Shipped",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_2 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_to_be_delivered_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_delivered_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_delivered_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Delivered",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_3 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    inventory_summary_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    inventory_summary_title = customtkinter.CTkLabel(
        inventory_summary_frame,
        text="Inventory Summary",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    total_quantity_in_hand_1 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text=str(fetch_total_quantity_in_hand_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_quantity_in_hand_2 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text="Quantity In Hand",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_4 = customtkinter.CTkFrame(
        inventory_summary_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_quantity_to_be_received_1 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text=str(fetch_total_quantity_to_be_received_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_quantity_to_be_received_2 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text="Quantity To be Received",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_5 = customtkinter.CTkFrame(
        inventory_summary_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    product_details_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    product_details_title = customtkinter.CTkLabel(
        product_details_frame,
        text="Product Details",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    low_stock_items_1 = customtkinter.CTkLabel(
        master=product_details_frame,
        text=str(fetch_low_stock_item_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    low_stock_items_2 = customtkinter.CTkLabel(
        master=product_details_frame,
        text="Low Stock Items",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_6 = customtkinter.CTkFrame(
        product_details_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    all_items_1 = customtkinter.CTkLabel(
        master=product_details_frame,
        text=str(fetch_total_items_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    all_items_2 = customtkinter.CTkLabel(
        master=product_details_frame,
        text="Total Items",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_7 = customtkinter.CTkFrame(
        product_details_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    welcome_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    sales_activity_frame.grid(row=1, column=0, padx=10, pady=10)
    inventory_summary_frame.grid(row=1, column=1, padx=10, pady=10)
    product_details_frame.grid(row=1, column=2, padx=10, pady=10)
    fig = plt.Figure()
    fig.set_facecolor('#e5e5e5')
    canvas = FigureCanvasTkAgg(fig, master=tab_0)
    canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky="W")
    low_stock_vs_total_item_pie_chart(canvas)

    fig1 = plt.Figure()
    fig1.set_facecolor('#e5e5e5')
    canvas1 = FigureCanvasTkAgg(fig1, master=tab_0)
    canvas1.get_tk_widget().grid(row=2, column=1, padx=10, pady=10, columnspan=2)
    bar_chart(canvas1)

    sales_activity_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    total_to_be_packed_label_1.grid(row=1, column=0, padx=20, pady=5)
    total_to_be_packed_label_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_1.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    total_to_be_shipped_label_1.grid(row=1, column=2, padx=20, pady=5)
    total_to_be_shipped_label_2.grid(row=2, column=2, padx=20, pady=5)
    sales_activity_vertical_separator_2.grid(row=1, column=3, rowspan=2, padx=5, pady=5)
    total_to_be_delivered_label_1.grid(row=1, column=4, padx=20, pady=5)
    total_to_be_delivered_label_2.grid(row=2, column=4, padx=20, pady=5)
    # sales_activity_vertical_separator_3.grid(row=1, column=5, rowspan=2, padx=5, pady=5)

    inventory_summary_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    total_quantity_in_hand_1.grid(row=1, column=0, padx=20, pady=5)
    total_quantity_in_hand_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_4.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    total_quantity_to_be_received_1.grid(row=1, column=2, padx=20, pady=5)
    total_quantity_to_be_received_2.grid(row=2, column=2, padx=20, pady=5)
    # sales_activity_vertical_separator_5.grid(row=1, column=3, rowspan=2, padx=5, pady=5)

    product_details_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    low_stock_items_1.grid(row=1, column=0, padx=20, pady=5)
    low_stock_items_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_6.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    all_items_1.grid(row=1, column=2, padx=20, pady=5)
    all_items_2.grid(row=2, column=2, padx=20, pady=5)
    # sales_activity_vertical_separator_7.grid(row=1, column=3, rowspan=2, padx=5, pady=5)

    tab_0.columnconfigure(1, weight=1)

    customer_table_frame = customtkinter.CTkFrame(master=tab_1, width=1280, height=515)
    customer_table_frame.place(x=0, y=205)

    customer_tree = ttk.Treeview(master=customer_table_frame, height=18)

    customer_verscrlbar = customtkinter.CTkScrollbar(
        master=customer_table_frame, orientation="vertical", command=customer_tree.yview
    )
    customer_verscrlbar.pack(side="right", fill="y")

    customer_tree.configure(yscrollcommand=customer_verscrlbar.set)
    customer_tree["columns"] = (
        "CUSTOMERID",
        "CUSTOMERNAME",
        "CUSOTMEREMAILADDRESS",
        "CUSTOMERCONTACTNO",
    )

    customer_tree.column("#0", width=0, stretch=tk.NO)
    customer_tree.column("CUSTOMERID", anchor=tk.CENTER, width=313)
    customer_tree.column("CUSTOMERNAME", anchor=tk.CENTER, width=313)
    customer_tree.column("CUSOTMEREMAILADDRESS", anchor=tk.CENTER, width=313)
    customer_tree.column("CUSTOMERCONTACTNO", anchor=tk.CENTER, width=313)

    customer_tree.heading("CUSTOMERID", text="ID")
    customer_tree.heading("CUSTOMERNAME", text="Name")
    customer_tree.heading("CUSOTMEREMAILADDRESS", text="Email Address")
    customer_tree.heading("CUSTOMERCONTACTNO", text="Contact No.")

    customer_tree.pack(side="right", fill="both")
    customer_tree.bind("<Double-1>", on_customer_double_click)
    customer_tree.bind("<ButtonRelease>", display_customer_record)

    customer_menu_frame = customtkinter.CTkFrame(
        master=tab_1,
        border_width=2
    )

    insert_customer_data_label = customtkinter.CTkLabel(
        master=customer_menu_frame,
        text="Insert New Customer",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    customer_name_entry_label = customtkinter.CTkLabel(
        master=customer_menu_frame,
        text="Customer Name:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    customer_name_entry = customtkinter.CTkEntry(
        master=customer_menu_frame,
        placeholder_text="Name",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    customer_email_entry_label = customtkinter.CTkLabel(
        master=customer_menu_frame,
        text="Customer Email Address:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    customer_email_entry = customtkinter.CTkEntry(
        master=customer_menu_frame,
        placeholder_text="Email Address",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    customer_contact_entry_label = customtkinter.CTkLabel(
        master=customer_menu_frame,
        text="Customer Contact No.:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    customer_contact_entry = customtkinter.CTkEntry(
        master=customer_menu_frame,
        placeholder_text="Contact No.",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    addcustomer_btn = customtkinter.CTkButton(
        master=customer_menu_frame,
        text="Add",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=add_new_customer_details,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    editcustomer_btn = customtkinter.CTkButton(
        master=customer_menu_frame,
        text="Edit",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=edit_customer_details,
        compound="top",
        corner_radius=200,
        fg_color="#ADD8E6",
        text_color="black",
    )

    deletecustomer_btn = customtkinter.CTkButton(
        master=customer_menu_frame,
        text="Delete",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=delete_customer_record,
        compound="top",
        corner_radius=200,
        fg_color="#ff666d",
        text_color="black",
    )

    customer_menu_frame.grid(row=0, column=0)

    insert_customer_data_label.grid(row=0, column=0, sticky="w", padx=5, pady=5, columnspan=2)

    customer_name_entry_label.grid(row=1, column=0, padx=5, pady=5)
    customer_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    customer_email_entry_label.grid(row=1, column=2, padx=5, pady=5)
    customer_email_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    customer_contact_entry_label.grid(row=1, column=4, padx=5, pady=5)
    customer_contact_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    addcustomer_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    editcustomer_btn.grid(row=2, column=2, padx=5, pady=5, columnspan=2)
    deletecustomer_btn.grid(row=2, column=4, padx=5, pady=5, columnspan=2)

    tab_1.columnconfigure(0, weight=2)

    supplier_table_frame = customtkinter.CTkFrame(master=tab_2, width=1280, height=515)
    supplier_table_frame.place(x=0, y=205)

    supplier_tree = ttk.Treeview(master=supplier_table_frame, height=18)

    supplier_verscrlbar = customtkinter.CTkScrollbar(
        master=supplier_table_frame, orientation="vertical", command=supplier_tree.yview
    )
    supplier_verscrlbar.pack(side="right", fill="y")

    supplier_tree.configure(yscrollcommand=supplier_verscrlbar.set)
    supplier_tree["columns"] = (
        "SUPPLIERID",
        "SUPPLIERNAME",
        "SUPPLIEREMAILADDRESS",
        "SUPPLIERCONTACTNO",
    )

    supplier_tree.column("#0", width=0, stretch=tk.NO)
    supplier_tree.column("SUPPLIERID", anchor=tk.CENTER, width=313)
    supplier_tree.column("SUPPLIERNAME", anchor=tk.CENTER, width=313)
    supplier_tree.column("SUPPLIEREMAILADDRESS", anchor=tk.CENTER, width=313)
    supplier_tree.column("SUPPLIERCONTACTNO", anchor=tk.CENTER, width=313)

    supplier_tree.heading("SUPPLIERID", text="ID")
    supplier_tree.heading("SUPPLIERNAME", text="Name")
    supplier_tree.heading("SUPPLIEREMAILADDRESS", text="Email Address")
    supplier_tree.heading("SUPPLIERCONTACTNO", text="Contact No.")

    supplier_tree.pack(side="right", fill="both")
    supplier_tree.bind("<ButtonRelease>", display_supplier_record)

    supplier_menu_frame = customtkinter.CTkFrame(
        master=tab_2,
        border_width=2
    )

    insert_supplier_data_label = customtkinter.CTkLabel(
        master=supplier_menu_frame,
        text="Insert New Supplier",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    supplier_name_entry_label = customtkinter.CTkLabel(
        master=supplier_menu_frame,
        text="Supplier Name:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    supplier_name_entry = customtkinter.CTkEntry(
        master=supplier_menu_frame,
        placeholder_text="Name",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    supplier_email_entry_label = customtkinter.CTkLabel(
        master=supplier_menu_frame,
        text="Supplier Email Address:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    supplier_email_entry = customtkinter.CTkEntry(
        master=supplier_menu_frame,
        placeholder_text="Email Address",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    supplier_contact_entry_label = customtkinter.CTkLabel(
        master=supplier_menu_frame,
        text="Supplier Contact No.:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    supplier_contact_entry = customtkinter.CTkEntry(
        master=supplier_menu_frame,
        placeholder_text="Contact No.",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    addsupplier_btn = customtkinter.CTkButton(
        master=supplier_menu_frame,
        text="Add",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=add_new_supplier_details,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    editsupplier_btn = customtkinter.CTkButton(
        master=supplier_menu_frame,
        text="Edit",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=edit_supplier_details,
        compound="top",
        corner_radius=200,
        fg_color="#ADD8E6",
        text_color="black",
    )

    deletesupplier_btn = customtkinter.CTkButton(
        master=supplier_menu_frame,
        text="Delete",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=delete_supplier_record,
        compound="top",
        corner_radius=200,
        fg_color="#ff666d",
        text_color="black",
    )

    supplier_menu_frame.grid(row=0, column=0)

    insert_supplier_data_label.grid(row=0, column=0, sticky="w", padx=5, pady=5, columnspan=2)

    supplier_name_entry_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    supplier_name_entry.grid(row=1, column=1, padx=5, pady=5)
    supplier_email_entry_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)
    supplier_email_entry.grid(row=1, column=3, padx=5, pady=5)
    supplier_contact_entry_label.grid(row=1, column=4, sticky="w", padx=5, pady=5)
    supplier_contact_entry.grid(row=1, column=5, padx=5, pady=5)

    addsupplier_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    editsupplier_btn.grid(row=2, column=2, padx=5, pady=5, columnspan=2)
    deletesupplier_btn.grid(row=2, column=4, padx=5, pady=5, columnspan=2)

    tab_2.columnconfigure(0, weight=2)

    product_table_frame = customtkinter.CTkFrame(master=tab_3, width=1280, height=515)
    product_table_frame.place(x=0, y=205)

    product_tree = ttk.Treeview(master=product_table_frame, height=20)

    product_verscrlbar = customtkinter.CTkScrollbar(
        master=product_table_frame, orientation="vertical", command=product_tree.yview
    )
    product_verscrlbar.pack(side="right", fill="y")

    product_tree.configure(yscrollcommand=product_verscrlbar.set)
    product_tree["columns"] = (
        "PRODUCTID",
        "PRODUCTNAME",
        "PRODUCTQUANTITY",
        "PRODUCTDESCRIPTION",
        "PRODUCTMINSTOCK",
    )

    product_tree.column("#0", width=0, stretch=tk.NO)
    product_tree.column("PRODUCTID", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTNAME", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTQUANTITY", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTDESCRIPTION", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTMINSTOCK", anchor=tk.CENTER, width=250)

    product_tree.heading("PRODUCTID", text="ID", command=lambda: sort_treeview_column(product_tree, "PRODUCTID", False))
    product_tree.heading("PRODUCTNAME", text="Name")
    product_tree.heading("PRODUCTQUANTITY", text="Quantity")
    product_tree.heading("PRODUCTDESCRIPTION", text="Description")
    product_tree.heading("PRODUCTMINSTOCK", text="Min. Stock")

    product_tree.pack(side="bottom", fill="both")
    product_tree.bind("<Double-1>", on_product_double_click)
    product_tree.bind("<ButtonRelease>", display_product_record)

    search_entry = customtkinter.CTkEntry(tab_3,placeholder_text="Search", width=1050,)
    search_entry.grid(row=1,column=0, padx=10, pady=10)
    search_entry.bind("<KeyRelease>", search_product)

    product_menu_frame = customtkinter.CTkFrame(
        master=tab_3,
        border_width=2
    )

    insert_product_data_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Insert New Product",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    product_id_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product ID:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_id_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="ID",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_name_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Name:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_name_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Item",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_quantity_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Quantity:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_quantity_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Quantity",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_description_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Description:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_description_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Description",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_min_stock_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Min. Stock:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_min_stock_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Min. Stock",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    addproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Add Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=add_new_product_details,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    editproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Edit Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=edit_product_details,
        compound="top",
        corner_radius=200,
        fg_color="#ADD8E6",
        text_color="black",
    )

    deleteproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Delete Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=delete_product_record,
        compound="top",
        corner_radius=200,
        fg_color="#ff666d",
        text_color="black",
    )

    product_menu_frame.grid(row=0, column=0)

    insert_product_data_label.grid(
        row=0, column=0, sticky="w", padx=5, pady=5, columnspan=2
    )

    product_id_entry_label.grid(row=1, column=0, padx=5)
    product_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    product_name_entry_label.grid(row=1, column=2, padx=5)
    product_name_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    product_quantity_entry_label.grid(row=1, column=4, padx=5)
    product_quantity_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")
    product_description_entry_label.grid(row=2, column=0, padx=5)
    product_description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    product_min_stock_entry_label.grid(row=2, column=2, padx=5)
    product_min_stock_entry.grid(row=2, column=3, padx=5, pady=5)

    addproduct_btn.grid(row=3, column=0, padx=20, pady=5, columnspan=2)
    editproduct_btn.grid(row=3, column=2, padx=20, pady=5, columnspan=2)
    deleteproduct_btn.grid(row=3, column=4, padx=20, pady=5, columnspan=2)

    tab_3.columnconfigure(0, weight=2)

    task_table_frame = customtkinter.CTkFrame(master=tab_4, width=1280, height=515)
    task_table_frame.place(x=0, y=220)

    task_tree = ttk.Treeview(master=task_table_frame, height=20)

    task_verscrlbar = customtkinter.CTkScrollbar(
        master=task_table_frame, orientation="vertical", command=task_tree.yview
    )
    task_verscrlbar.pack(side="right", fill="y")

    task_tree.configure(yscrollcommand=task_verscrlbar.set)
    task_tree["columns"] = (
        "TASKID",
        "TASKDESCRIPTION",
        "ASSIGNEDTO",
        "STATUS",
        "DUEDATE",
    )

    task_tree.column("#0", width=0, stretch=tk.NO)
    task_tree.column("TASKID", anchor=tk.CENTER, width=250)
    task_tree.column("TASKDESCRIPTION", anchor=tk.CENTER, width=250)
    task_tree.column("ASSIGNEDTO", anchor=tk.CENTER, width=250)
    task_tree.column("STATUS", anchor=tk.CENTER, width=250)
    task_tree.column("DUEDATE", anchor=tk.CENTER, width=250)

    task_tree.heading("TASKID", text="Task ID")
    task_tree.heading("TASKDESCRIPTION", text="Task")
    task_tree.heading("ASSIGNEDTO", text="Assigned To")
    task_tree.heading("STATUS", text="Status")
    task_tree.heading("DUEDATE", text="Due Date")

    task_tree.pack(side="bottom", fill="both")
    task_tree.bind("<ButtonRelease>", display_product_record)

    task_tree.tag_configure("Pending", background="#FFBA00", foreground="black")
    task_tree.tag_configure("Completed", background="green", foreground="black")
    task_tree.tag_configure("Due", background="#FF7F7F", foreground="black")

    task_menu_frame = customtkinter.CTkFrame(master=tab_4, border_width=2)
    insert_task_data_label = customtkinter.CTkLabel(
        master=task_menu_frame,
        text="Assign New Task",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    task_label = customtkinter.CTkLabel(
        master=task_menu_frame,
        text="Task:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )
    task_entry = customtkinter.CTkEntry(
        master=task_menu_frame,
        placeholder_text="Task",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    assigned_worker_label = customtkinter.CTkLabel(
        master=task_menu_frame,
        text="Assigned To:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    assigned_worker_entry = customtkinter.CTkComboBox(
        master=task_menu_frame,
        values=fetch_worker_to_list(),
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    task_due_date_label = customtkinter.CTkLabel(
        master=task_menu_frame,
        text="Due Date:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    task_due_date_entry = DateEntry(
        master=task_menu_frame,
        date=datetime.today(),
        relief=GROOVE,
        font=customtkinter.CTkFont("SF Pro Display", 12),
        width=25,
    )

    addtask_btn = customtkinter.CTkButton(
        master=task_menu_frame,
        text="Add",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=add_new_task_details,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    edittask_btn = customtkinter.CTkButton(
        master=task_menu_frame,
        text="Edit",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=edit_task_details,
        compound="top",
        corner_radius=200,
        fg_color="#ADD8E6",
        text_color="black",
    )

    deletetask_btn = customtkinter.CTkButton(
        master=task_menu_frame,
        text="Delete",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=delete_task_record,
        compound="top",
        corner_radius=200,
        fg_color="#ff666d",
        text_color="black",
    )

    task_menu_frame.grid(row=0, column=0)
    insert_task_data_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    task_label.grid(row=1, column=0, padx=5, pady=5)
    task_entry.grid(row=1, column=1, padx=5, pady=5)
    assigned_worker_label.grid(row=2, column=0, padx=5, pady=5)
    assigned_worker_entry.grid(row=2, column=1, padx=5, pady=5)
    task_due_date_label.grid(row=3, column=0, padx=5, pady=5)
    task_due_date_entry.grid(row=3, column=1, padx=5, pady=5)
    addtask_btn.grid(row=4, column=0, padx=5, pady=5)
    edittask_btn.grid(row=4, column=1, padx=5, pady=5)
    deletetask_btn.grid(row=4, column=2, padx=5, pady=5)

    tab_4.columnconfigure(0, weight=1)

    incoming_stock_table_frame = customtkinter.CTkFrame(
        master=tab_5, width=1006, height=515
    )
    incoming_stock_table_frame.place(x=0, y=205)

    incoming_stock_tree = ttk.Treeview(master=incoming_stock_table_frame, height=20)

    incoming_stock_verscrlbar = customtkinter.CTkScrollbar(
        master=incoming_stock_table_frame,
        orientation="vertical",
        command=incoming_stock_tree.yview,
    )
    incoming_stock_verscrlbar.pack(side="right", fill="y")

    incoming_stock_tree.configure(yscrollcommand=incoming_stock_verscrlbar.set)
    incoming_stock_tree["columns"] = (
        "INCOMINGSTOCKID",
        "INCOMINGSTOCKNAME",
        "INCOMINGSTOCKQUANTITY",
        "INCOMINGSTOCKSTATUS",
    )

    incoming_stock_tree.column("#0", width=0, stretch=tk.NO)
    incoming_stock_tree.column("INCOMINGSTOCKID", anchor=tk.CENTER, width=310)
    incoming_stock_tree.column("INCOMINGSTOCKNAME", anchor=tk.CENTER, width=310)
    incoming_stock_tree.column("INCOMINGSTOCKQUANTITY", anchor=tk.CENTER, width=310)
    incoming_stock_tree.column("INCOMINGSTOCKSTATUS", anchor=tk.CENTER, width=320)

    incoming_stock_tree.heading("INCOMINGSTOCKID", text="ID")
    incoming_stock_tree.heading("INCOMINGSTOCKNAME", text="Name")
    incoming_stock_tree.heading("INCOMINGSTOCKQUANTITY", text="Quantity")
    incoming_stock_tree.heading("INCOMINGSTOCKSTATUS", text="Status")

    incoming_stock_tree.pack(side="bottom", fill="both")

    incoming_stock_tree.tag_configure(
        "To be Received", background="#FFBA00", foreground="black"
    )
    incoming_stock_tree.tag_configure(
        "Received", background="green", foreground="black"
    )

    incoming_stock_menu_frame = customtkinter.CTkFrame(master=tab_5, border_width=2)

    edit_purchase_order_status_label = customtkinter.CTkLabel(
        master=incoming_stock_menu_frame,
        text="Edit Purchase Order Status",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )
    purchase_order_status_label = customtkinter.CTkLabel(
        master=incoming_stock_menu_frame,
        text="Status:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )
    purchase_order_status_entry = customtkinter.CTkComboBox(
        master=incoming_stock_menu_frame,
        values=["To be Received", "Received"],
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    editpurchaseorder_btn = customtkinter.CTkButton(
        master=incoming_stock_menu_frame,
        text="Edit Status",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=update_purchase_order_status,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    incoming_stock_menu_frame.grid(row=0, column=0, pady=10)
    edit_purchase_order_status_label.grid(row=0, column=0, padx=10, pady=10)
    purchase_order_status_label.grid(row=1, column=0, padx=5, pady=5)
    purchase_order_status_entry.grid(row=1, column=1, padx=5, pady=5)
    editpurchaseorder_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

    tab_5.columnconfigure(0, weight=2)

    outgoing_stock_table_frame = customtkinter.CTkFrame(
        master=tab_6, width=1006, height=515
    )
    outgoing_stock_table_frame.place(x=0, y=205)

    outgoing_stock_tree = ttk.Treeview(master=outgoing_stock_table_frame, height=20)

    outgoing_stock_verscrlbar = customtkinter.CTkScrollbar(
        master=outgoing_stock_table_frame,
        orientation="vertical",
        command=outgoing_stock_tree.yview,
    )
    outgoing_stock_verscrlbar.pack(side="right", fill="y")

    outgoing_stock_tree.configure(yscrollcommand=outgoing_stock_verscrlbar.set)
    outgoing_stock_tree["columns"] = (
        "OUTGOINGSTOCKID",
        "OUTGOINGSTOCKNAME",
        "OUTGOINGSTOCKQUANTITY",
        "OUTGOINGSTOCKSTATUS"
    )

    outgoing_stock_tree.column("#0", width=0, stretch=tk.NO)
    outgoing_stock_tree.column("OUTGOINGSTOCKID", anchor=tk.CENTER, width=313)
    outgoing_stock_tree.column("OUTGOINGSTOCKNAME", anchor=tk.CENTER, width=313)
    outgoing_stock_tree.column("OUTGOINGSTOCKQUANTITY", anchor=tk.CENTER, width=313)
    outgoing_stock_tree.column("OUTGOINGSTOCKSTATUS", anchor=tk.CENTER, width=313)

    outgoing_stock_tree.heading("OUTGOINGSTOCKID", text="ID")
    outgoing_stock_tree.heading("OUTGOINGSTOCKNAME", text="Date Created")
    outgoing_stock_tree.heading("OUTGOINGSTOCKQUANTITY", text="Customer Name")
    outgoing_stock_tree.heading("OUTGOINGSTOCKSTATUS", text="Status")

    outgoing_stock_tree.pack(side="bottom", fill="both")

    outgoing_stock_tree.bind("<Double-1>", on_sale_order_double_click)

    outgoing_stock_menu_frame = customtkinter.CTkFrame(master=tab_6, border_width=2)

    edit_sales_order_status_label = customtkinter.CTkLabel(
        master=outgoing_stock_menu_frame,
        text="Edit Sales Order Status",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )
    sales_order_status_label = customtkinter.CTkLabel(
        master=outgoing_stock_menu_frame,
        text="Status:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )
    sales_order_status_entry = customtkinter.CTkComboBox(
        master=outgoing_stock_menu_frame,
        values=["To be Packed", "To be Shipped", "To be Delivered", "Delivered"],
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    editsalesorder_btn = customtkinter.CTkButton(
        master=outgoing_stock_menu_frame,
        text="Edit Status",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=update_sales_order_status,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    outgoing_stock_menu_frame.grid(row=0, column=0, pady=10)
    edit_sales_order_status_label.grid(row=0, column=0, padx=10, pady=10)
    sales_order_status_label.grid(row=1, column=0, padx=5, pady=5)
    sales_order_status_entry.grid(row=1, column=1, padx=5, pady=5)
    editsalesorder_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

    tab_6.columnconfigure(0, weight=2)

    add_to_customer_table()
    add_to_supplier_table()
    add_to_product_table()
    add_to_task_table()
    add_to_incoming_stock_table()
    add_to_sale_order_table()


def worker_dashboard(username):

    def fetch_to_be_packed_data():
        total_to_be_packed = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Packed",))
        to_be_packed_data = cursor.fetchone()[0]
        total_to_be_packed += to_be_packed_data
        conn.commit()
        conn.close()
        return total_to_be_packed

    def update_to_be_packed_label():
        new_count = fetch_to_be_packed_data()
        total_to_be_packed_label_1.configure(text=str(new_count))

    def fetch_to_be_shipped_data():
        total_to_be_shipped = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Shipped",))
        to_be_shipped_data = cursor.fetchone()[0]
        total_to_be_shipped += to_be_shipped_data
        conn.commit()
        conn.close()
        return total_to_be_shipped

    def update_to_be_shipped_label():
        new_count = fetch_to_be_shipped_data()
        total_to_be_shipped_label_1.configure(text=str(new_count))

    def fetch_to_be_delivered_data():
        total_to_be_delivered = 0
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(SALE_ORDER_STATUS) FROM SALE_ORDER WHERE SALE_ORDER_STATUS = ?", ("To be Delivered",))
        to_be_delivered_data = cursor.fetchone()[0]
        total_to_be_delivered += to_be_delivered_data
        conn.commit()
        conn.close()
        return total_to_be_delivered

    def update_to_be_delivered_label():
        new_count = fetch_to_be_delivered_data()
        total_to_be_delivered_label_1.configure(text=str(new_count))

    def fetch_total_quantity_in_hand_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(PRODUCT_QUANTITY) FROM PRODUCT")
        total_quantity_in_hand = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_quantity_in_hand

    def update_total_quantity_in_hand_label():
        new_count = fetch_total_quantity_in_hand_data()
        total_quantity_in_hand_1.configure(text=str(new_count))

    def fetch_total_quantity_to_be_received_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(PURCHASE_ORDER_PRODUCT_QUANTITY) FROM PURCHASE_ORDER WHERE PURCHASE_ORDER_STATUS = ?", ("To be Received",))
        total_quantity_to_be_received = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_quantity_to_be_received

    def update_total_quantity_to_be_received_label():
        new_count = fetch_total_quantity_to_be_received_data()
        total_quantity_to_be_received_1.configure(text=str(new_count))

    def fetch_low_stock_item_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT WHERE PRODUCT_QUANTITY < PRODUCT_MIN_STOCK")
        low_stock_items = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return low_stock_items

    def update_low_stock_item_label():
        new_count = fetch_low_stock_item_data()
        low_stock_items_1.configure(text=str(new_count))

    def fetch_total_items_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT")
        total_items = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return total_items

    def update_total_items_label():
        new_count = fetch_total_items_data()
        all_items_1.configure(text=str(new_count))
    def fetch_customer_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CUSTOMER")
        customer = cursor.fetchall()
        conn.commit()
        conn.close()
        return customer

    def clear_customer_entry_field():
        customer_name_entry.delete(0, END)
        customer_email_entry.delete(0, END)
        customer_contact_entry.delete(0, END)

    def display_customer_record(event):
        selected_item = customer_tree.focus()
        if selected_item:
            clear_customer_entry_field()
            row = customer_tree.item(selected_item)["values"]
            customer_name_entry.insert(0, row[1])
            customer_email_entry.insert(0, row[2])
            customer_contact_entry.insert(0, row[3])

    def fetch_customer_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(CUSTOMER_ID) FROM CUSTOMER")
        last_customer_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_customer_id

    def generate_customer_id(prefix="CUST"):
        last_customer_id = fetch_customer_last_id()
        if last_customer_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_customer_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def add_to_customer_table():
        customers = fetch_customer_data()
        customer_tree.delete(*customer_tree.get_children())
        for customer in customers:
            customer_tree.insert("", END, values=customer)

    def check_existing_customer(customer_check):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT CUSTOMER_NAME FROM CUSTOMER WHERE CUSTOMER_NAME = ?",
            (customer_check,),
        )
        existing_customer = cursor.fetchone()
        conn.commit()
        conn.close()
        return existing_customer

    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    def is_valid_contact_number(contact_number):
        return contact_number.isdigit()

    def add_new_customer_details():
        customer_id = generate_customer_id("CUST")
        customer_name = customer_name_entry.get()
        customer_email = customer_email_entry.get()
        customer_contactno = customer_contact_entry.get()

        if not (customer_name and customer_email and customer_contactno):
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not is_valid_email(customer_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not is_valid_contact_number(customer_contactno):
            messagebox.showerror("Error", "Contact number must be only digits")
            return

        if not check_existing_customer(customer_name):
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO CUSTOMER (CUSTOMER_ID,CUSTOMER_NAME,CUSTOMER_EMAIL,CUSTOMER_TEL) \
                VALUES (?,?,?,?)",
                (customer_id, customer_name, customer_email, customer_contactno),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
        else:
            messagebox.showerror(
                "Warning", "Duplicate customer! Please enter new customer."
            )
        add_to_customer_table()
        clear_customer_entry_field()
        return

    def edit_customer_details():
        selected_customer_details = customer_tree.focus()
        if not selected_customer_details:
            messagebox.showerror("Error", "Please select a record to edit")
            return

        row = customer_tree.item(selected_customer_details)["values"]
        new_customer_name = customer_name_entry.get()
        new_customer_email = customer_email_entry.get()
        new_customer_contactno = customer_contact_entry.get()

        if not (new_customer_name and new_customer_email and new_customer_contactno):
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not is_valid_email(new_customer_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not is_valid_contact_number(new_customer_contactno):
            messagebox.showerror("Error", "Contact number must be only digits")
            return

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE CUSTOMER SET CUSTOMER_NAME = ?, CUSTOMER_EMAIL = ?, CUSTOMER_TEL = ? WHERE CUSTOMER_NAME = ?",
            (new_customer_name, new_customer_email, new_customer_contactno, row[1]),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")
        add_to_customer_table()
        clear_customer_entry_field()

    def delete_customer_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = customer_tree.focus()
        row = customer_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM CUSTOMER WHERE CUSTOMER_NAME= ?", (row[1],))
        conn.commit()
        conn.close()
        add_to_customer_table()
        clear_customer_entry_field()

    def delete_customer_record():
        selected_item = customer_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_customer_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    def fetch_product_to_list():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT PRODUCT_NAME FROM PRODUCT")
        products = cursor.fetchall()
        product = []
        for x in products:
            product.append(x[0])
        conn.commit()
        conn.close()
        return product

    def on_customer_double_click(event):

        selected_item = customer_tree.selection()[0]
        values = customer_tree.item(selected_item, "values")

        def fetch_selected_customer_details():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM CUSTOMER WHERE CUSTOMER_NAME = ?", (values[1],)
            )
            customer_details = cursor.fetchall()
            conn.commit()
            conn.close()
            return customer_details

        def add_new_sale_order():
            sale_order_id = generate_sale_order_id("SO")
            sale_order_date = date.today().strftime("%m/%d/%Y")
            customer_name = values[1]

            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO SALE_ORDER (SALE_ORDER_ID,SALE_ORDER_DATE,SALE_ORDER_CUSTOMER,SALE_ORDER_STATUS) \
            VALUES (?,?,?,?)",
                (sale_order_id, sale_order_date, customer_name, "To be packed"),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
            add_to_sale_order_table()
            return

        sales_window = customtkinter.CTk()
        sales_window.title("Product Details")

        customer_id_label = customtkinter.CTkLabel(
            sales_window,
            text="Customer ID:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_id_label_details = customtkinter.CTkLabel(
            sales_window,
            text=f"{values[0]}",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_name_label = customtkinter.CTkLabel(
            sales_window,
            text="Customer Name:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_name_label_details = customtkinter.CTkLabel(
            sales_window,
            text=f"{values[1]}",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_email_label = customtkinter.CTkLabel(
            sales_window,
            text="Customer Email:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_email_label_details = customtkinter.CTkLabel(
            sales_window,
            text=f"{values[2]}",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_contact_label = customtkinter.CTkLabel(
            sales_window,
            text="Customer Contact No.:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        customer_contact_label_details = customtkinter.CTkLabel(
            sales_window,
            text=f"{values[3]}",
            font=customtkinter.CTkFont("SF Pro Display"),
        )

        sales_quantity_label = customtkinter.CTkLabel(
            sales_window,
            text="Purchase Quantity:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        sales_quantity_entry = customtkinter.CTkEntry(
            master=sales_window,
            placeholder_text="Name",
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display"),
            border_width=0,
        )

        product_selection_label = customtkinter.CTkLabel(
            sales_window,
            text="Product to be purchase:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        product_selection_entry = customtkinter.CTkComboBox(
            master=sales_window,
            values=fetch_product_to_list(),
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display"),
            border_width=0,
        )

        sales_btn = customtkinter.CTkButton(
            master=sales_window,
            text="Create Sales Order",
            width=150,
            height=50,
            command=add_new_sale_order,
            font=customtkinter.CTkFont("SF Pro Display"),
            corner_radius=200,
            fg_color="#007FFF",
            text_color="black",
        )

        customer_id_label.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=5)
        customer_id_label_details.grid(row=0, column=1, sticky=W, padx=5, pady=5)
        customer_name_label.grid(row=1, column=0, sticky=W, padx=(10, 5), pady=5)
        customer_name_label_details.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        customer_email_label.grid(row=2, column=0, sticky=W, padx=(10, 5), pady=5)
        customer_email_label_details.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        customer_contact_label.grid(row=3, column=0, sticky=W, padx=(10, 5), pady=5)
        customer_contact_label_details.grid(row=3, column=1, sticky=W, padx=5, pady=5)

        # sales_quantity_label.grid(row=4, column=0, sticky=W, padx=(10, 5), pady=5)
        # sales_quantity_entry.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        # product_selection_label.grid(row=5, column=0, sticky=W, padx=(10, 5), pady=5)
        # product_selection_entry.grid(row=5, column=1, sticky=W, padx=5, pady=5)
        sales_btn.grid(row=6, column=0, columnspan=2, pady=20)

        sales_window.columnconfigure(0, weight=1)
        sales_window.columnconfigure(1, weight=1)
        sales_window.columnconfigure(2, weight=1)
        sales_window.columnconfigure(3, weight=1)
        sales_window.columnconfigure(4, weight=1)
        sales_window.columnconfigure(5, weight=1)
        sales_window.columnconfigure(6, weight=1)

        sales_window.mainloop()

    def fetch_supplier_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SUPPLIER")
        supplier = cursor.fetchall()
        conn.commit()
        conn.close()
        return supplier

    def add_to_supplier_table():
        suppliers = fetch_supplier_data()
        supplier_tree.delete(*supplier_tree.get_children())
        for supplier in suppliers:
            supplier_tree.insert("", END, values=supplier)

    def clear_supplier_entry_field():
        supplier_name_entry.delete(0, END)
        supplier_email_entry.delete(0, END)
        supplier_contact_entry.delete(0, END)

    def display_supplier_record(event):
        selected_item = supplier_tree.focus()
        if selected_item:
            clear_supplier_entry_field()
            row = supplier_tree.item(selected_item)["values"]
            supplier_name_entry.insert(0, row[1])
            supplier_email_entry.insert(0, row[2])
            supplier_contact_entry.insert(0, row[3])

    def fetch_supplier_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(SUPPLIER_ID ) FROM SUPPLIER")
        last_supplier_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_supplier_id

    def generate_supplier_id(prefix="SUPP"):
        last_supplier_id = fetch_supplier_last_id()
        if last_supplier_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_supplier_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def check_existing_supplier(supplier_check):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUPPLIER_NAME FROM SUPPLIER WHERE SUPPLIER_NAME = ?",
            (supplier_check,),
        )
        existing_supplier = cursor.fetchone()
        conn.commit()
        conn.close()
        return existing_supplier

    def add_new_supplier_details():
        supplier_id = generate_supplier_id("SUPP")
        supplier_name = supplier_name_entry.get()
        supplier_email = supplier_email_entry.get()
        supplier_contactno = supplier_contact_entry.get()

        if not (supplier_name and supplier_email and supplier_contactno):
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not is_valid_email(supplier_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not is_valid_contact_number(supplier_contactno):
            messagebox.showerror("Error", "Contact number must be only digits")
            return

        if not check_existing_supplier(supplier_name):
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO SUPPLIER (SUPPLIER_ID,SUPPLIER_NAME,SUPPLIER_EMAIL,SUPPLIER_TEL) \
                VALUES (?,?,?,?)",
                (supplier_id, supplier_name, supplier_email, supplier_contactno),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
        else:
            messagebox.showerror(
                "Warning", "Duplicate supplier! Please enter new supplier."
            )

        add_to_supplier_table()
        clear_supplier_entry_field()
        return

    def edit_supplier_details():
        selected_supplier_details = supplier_tree.focus()
        if not selected_supplier_details:
            messagebox.showerror("Error", "Please select a record to edit")
            return

        row = supplier_tree.item(selected_supplier_details)["values"]
        new_supplier_name = supplier_name_entry.get()
        new_supplier_email = supplier_email_entry.get()
        new_supplier_contactno = supplier_contact_entry.get()

        if not (new_supplier_name and new_supplier_email and new_supplier_contactno):
            messagebox.showerror("Error", "Please enter all fields")
            return

        if not is_valid_email(new_supplier_email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        if not is_valid_contact_number(new_supplier_contactno):
            messagebox.showerror("Error", "Contact number must be only digits")
            return

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE SUPPLIER SET SUPPLIER_NAME = ?, SUPPLIER_EMAIL = ?, SUPPLIER_TEL = ? WHERE SUPPLIER_NAME = ?",
            (new_supplier_name, new_supplier_email, new_supplier_contactno, row[1]),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")

        add_to_supplier_table()
        clear_supplier_entry_field()

    def delete_supplier_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = supplier_tree.focus()
        row = supplier_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM SUPPLIER WHERE SUPPLIER_NAME= ?", (row[1],))
        conn.commit()
        conn.close()
        add_to_supplier_table()
        clear_supplier_entry_field()

    def delete_supplier_record():
        selected_item = supplier_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_supplier_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    def fetch_product_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PRODUCT")
        product = cursor.fetchall()
        conn.commit()
        conn.close()
        return product

    def add_to_product_table():
        products = fetch_product_data()
        product_tree.delete(*product_tree.get_children())
        for product in products:
            product_tree.insert("", END, values=product)

    def clear_product_entry_field():
        product_id_entry.delete(0, END)
        product_name_entry.delete(0, END)
        product_quantity_entry.delete(0, END)
        product_description_entry.delete(0, END)
        product_min_stock_entry.delete(0, END)

    def display_product_record(event):
        selected_item = product_tree.focus()
        if selected_item:
            clear_product_entry_field()
            row = product_tree.item(selected_item)["values"]
            product_id_entry.insert(0, [row[0]])
            product_name_entry.insert(0, row[1])
            product_quantity_entry.insert(0, row[2])
            product_description_entry.insert(0, row[3])
            product_min_stock_entry.insert(0, [row[4]])

    def check_existing_product(product_check):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUPPLIER_NAME FROM SUPPLIER WHERE SUPPLIER_NAME = ?",
            (product_check,),
        )
        existing_supplier = cursor.fetchone()
        conn.commit()
        conn.close()
        return existing_supplier

    def add_new_product_details():
        product_id = product_id_entry.get()
        product_name = product_name_entry.get()
        product_quantity = product_quantity_entry.get()
        product_description = product_description_entry.get()
        product_min_stock = product_min_stock_entry.get()

        if not (product_name and product_quantity and product_description):
            messagebox.showerror("Error", "Please enter all fields")
            return
        elif not check_existing_product(product_name):
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PRODUCT (PRODUCT_ID,PRODUCT_NAME,PRODUCT_QUANTITY,PRODUCT_STATUS,PRODUCT_MIN_STOCK) \
            VALUES (?,?,?,?,?)",
                (
                    product_id,
                    product_name,
                    product_quantity,
                    product_description,
                    product_min_stock,
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
        else:
            messagebox.showerror(
                "Warning", "Duplicate customer! Please enter new customer."
            )
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()
        return

    def edit_product_details():
        selected_product_details = product_tree.focus()
        if not selected_product_details:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = product_tree.item(selected_product_details)["values"]
        new_product_id = product_id_entry.get()
        new_product_name = product_name_entry.get()
        new_product_quantity = product_quantity_entry.get()
        new_product_description = product_description_entry.get()
        new_product_min_stock = product_min_stock_entry.get()
        if not new_product_name:
            messagebox.showerror("Error", "Please enter all fields")
            return
        else:
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE PRODUCT SET PRODUCT_ID = ?, PRODUCT_NAME = ?, PRODUCT_QUANTITY = ?, PRODUCT_STATUS = ?, PRODUCT_MIN_STOCK = ? WHERE PRODUCT_NAME = ?",
                (
                    new_product_id,
                    new_product_name,
                    new_product_quantity,
                    new_product_description,
                    new_product_min_stock,
                    row[1],
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Record successfully edited")
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def delete_product_database():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        selected_item = product_tree.focus()
        row = product_tree.item(selected_item)["values"]
        cursor.execute("DELETE FROM PRODUCT WHERE PRODUCT_NAME= ?", (row[1],))
        conn.commit()
        conn.close()
        add_to_product_table()
        clear_product_entry_field()
        fetch_product_to_list()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def delete_product_record():
        selected_item = product_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        confirmation = messagebox.askyesno(
            "Are you sure?", "Are you sure that you want to delete the selected record?"
        )
        if confirmation:
            delete_product_database()
            messagebox.showinfo("Success", "Record successfully deleted")
            return

    def search_product(event):
        search_term = search_entry.get().lower()
        products = fetch_product_data()
        product_tree.delete(*product_tree.get_children())
        for product in products:
            if search_term in str(product).lower():
                product_tree.insert("", tk.END, values=product)

    def on_product_double_click(event):

        selected_item = product_tree.selection()[0]
        values = product_tree.item(selected_item, "values")

        def fetch_selected_product_details():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCT WHERE PRODUCT_NAME = ?", (values[1],))
            product_details = cursor.fetchall()
            conn.commit()
            conn.close()
            return product_details

        new_window = customtkinter.CTk()
        new_window.title("Product Details")
        # new_window.geometry("500x400")

        def add_incoming_stock():
            incoming_stock_id = generate_purchase_order_id("PO")
            incoming_stock_product = values[1]
            incoming_stock_quantity = restock_quantity_entry.get()
            incoming_stock_status = "To be Received"

            if not incoming_stock_quantity:
                messagebox.showerror("Error", "Please enter all fields")
                return

            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO PURCHASE_ORDER (PURCHASE_ORDER_ID,PURCHASE_ORDER_PRODUCT,PURCHASE_ORDER_PRODUCT_QUANTITY,PURCHASE_ORDER_STATUS) \
            VALUES (?,?,?,?)",
                (
                    incoming_stock_id,
                    incoming_stock_product,
                    incoming_stock_quantity,
                    incoming_stock_status,
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data has been inserted")
            add_to_incoming_stock_table()
            fetch_tbr_quantity()
            update_total_quantity_in_hand_label()
            update_total_quantity_to_be_received_label()
            new_window.destroy()

        def fetch_tbr_quantity():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT PURCHASE_ORDER_PRODUCT_QUANTITY FROM PURCHASE_ORDER WHERE PURCHASE_ORDER_PRODUCT = ? AND PURCHASE_ORDER_STATUS=?",
                (values[1], "To be Received"),
            )
            incoming_stock_quantity = cursor.fetchall()
            tbr = 0
            for x in incoming_stock_quantity:
                tbr += x[0]
            conn.commit()
            conn.close()
            return tbr

        def fetch_tbs_quantity():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT SALE_ORDER_PRODUCT_QUANTITY FROM SALE_ORDER_PRODUCT WHERE SALE_ORDER_PRODUCT = ?",
                (values[1],),
            )
            outgoing_stock_quantity = cursor.fetchall()
            tbs = 0
            for x in outgoing_stock_quantity:
                tbs += x[0]
            conn.commit()
            conn.close()
            return tbs

        product_details_frame = customtkinter.CTkFrame(new_window, border_width=2)
        product_details_title = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Details",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        product_id_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product ID:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_id_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[0]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_name_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Name:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_name_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[1]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_quantity_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Quantity:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_quantity_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[2]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_description_label = customtkinter.CTkLabel(
            product_details_frame,
            text="Product Description:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        product_description_label_details = customtkinter.CTkLabel(
            product_details_frame,
            text=f"{values[3]}",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )

        restock_frame = customtkinter.CTkFrame(new_window, border_width=2)
        restock_title = customtkinter.CTkLabel(
            restock_frame,
            text="Restock",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        restock_quantity_label = customtkinter.CTkLabel(
            restock_frame,
            text="Restock Quantity:",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        restock_quantity_entry = customtkinter.CTkEntry(
            master=restock_frame,
            placeholder_text="Quantity",
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display", size=13),
            border_width=0,
        )

        restock_btn = customtkinter.CTkButton(
            master=restock_frame,
            text="Restock",
            command=add_incoming_stock,
            font=customtkinter.CTkFont("SF Pro Display", size=13),
            corner_radius=200,
            fg_color="#007FFF",
            text_color="black",
        )

        status_frame = customtkinter.CTkFrame(new_window, border_width=2)
        status_details_title = customtkinter.CTkLabel(
            status_frame,
            text="Status",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )
        total_tbs = customtkinter.CTkFrame(
            master=status_frame, width=100, height=100, fg_color="transparent"
        )
        total_tbs_details_1 = customtkinter.CTkLabel(
            total_tbs,
            text=(str(fetch_tbs_quantity()) + " Qty"),
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        total_tbs_details_2 = customtkinter.CTkLabel(
            total_tbs,
            text="To be Shipped",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        vertical_separator = customtkinter.CTkFrame(
            status_frame, width=2, height=80, fg_color="#CCCCCC"
        )
        total_tbr = customtkinter.CTkFrame(
            master=status_frame, width=100, height=100, fg_color="transparent"
        )
        total_tbr_details_1 = customtkinter.CTkLabel(
            total_tbr,
            text=(str(fetch_tbr_quantity()) + " Qty"),
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )
        total_tbr_details_2 = customtkinter.CTkLabel(
            total_tbr,
            text="To be Received",
            font=customtkinter.CTkFont("SF Pro Display", size=13),
        )

        product_details_frame.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        product_details_title.grid(
            row=0, column=0, columnspan=2, sticky=W, padx=10, pady=10
        )
        product_id_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        product_id_label_details.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        product_name_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        product_name_label_details.grid(row=2, column=1, sticky=W, padx=5, pady=5)
        product_quantity_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
        product_quantity_label_details.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        product_description_label.grid(row=4, column=0, sticky=W, padx=5, pady=5)
        product_description_label_details.grid(
            row=4, column=1, sticky=W, padx=5, pady=5
        )

        restock_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        restock_title.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        restock_quantity_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        restock_quantity_entry.grid(row=1, column=1, sticky=W, padx=5, pady=5)
        restock_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        status_frame.grid(row=0, column=1, sticky=W, padx=10, pady=10)
        status_details_title.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        total_tbs.grid(row=1, column=0, rowspan=5, padx=15, pady=15)
        total_tbs_details_1.pack(side=TOP)
        total_tbs_details_2.pack(side=BOTTOM)
        vertical_separator.grid(row=1, column=1, rowspan=5, pady=36)
        total_tbr.grid(row=1, column=3, rowspan=5, padx=15, pady=15)
        total_tbr_details_1.pack(side=TOP)
        total_tbr_details_2.pack(side=BOTTOM)

        new_window.mainloop()

    def fetch_task_data_worker():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT TASK_DESCRIPTION,TASK_STATUS,TASK_DUE_DATE FROM TASK WHERE TASK_ASSIGNED_TO = ?",
            (username,),
        )
        task = cursor.fetchall()
        conn.commit()
        conn.close()
        return task

    def add_to_task_table():
        tasks = fetch_task_data_worker()
        task_tree.delete(*task_tree.get_children())
        for task in tasks:
            task_tree.insert("", END, values=task, tags=task)

    def check_task_status():
        task_tree.tag_configure("Pending", background="#FFBA00", foreground="black")
        task_tree.tag_configure("Completed", background="green", foreground="black")
        task_tree.tag_configure("Due", background="#FF7F7F", foreground="black")

    def check_task_due_date():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT TASK_DUE_DATE, TASK_DESCRIPTION FROM TASK WHERE TASK_ASSIGNED_TO = ? AND TASK_STATUS = ?",
            (username, "Pending"),
        )
        tasks = cursor.fetchall()
        conn.commit()
        conn.close()

        today = datetime.today()

        due_task = 0

        for task in tasks:
            due_date_str = task[0]
            due_date = datetime.strptime(due_date_str, "%m/%d/%y")
            if due_date < today:
                due_task += 1
                conn = sqlite3.connect("Inventory Management System.db")
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE TASK SET TASK_STATUS = ? WHERE TASK_DESCRIPTION = ?",
                    ("Due", task[1]),
                )
                conn.commit()
                conn.close()

        check_task_status()
        add_to_task_table()
        return due_task

    def complete_task():
        selected_task = task_tree.focus()
        if not selected_task:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = task_tree.item(selected_task)["values"]
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE TASK SET TASK_STATUS = ? WHERE TASK_DESCRIPTION = ?",
            ("Completed", row[0]),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")
        check_task_status()
        add_to_task_table()

    def fetch_incoming_stock_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PURCHASE_ORDER")
        incoming_stock = cursor.fetchall()
        conn.commit()
        conn.close()
        return incoming_stock

    def add_to_incoming_stock_table():
        incoming_stocks = fetch_incoming_stock_data()
        incoming_stock_tree.delete(*incoming_stock_tree.get_children())
        for incoming_stock in incoming_stocks:
            incoming_stock_tree.insert(
                "", END, values=incoming_stock, tags=incoming_stock
            )

    def update_purchase_order_status():
        new_status = purchase_order_status_entry.get()
        selected = incoming_stock_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = incoming_stock_tree.item(selected)["values"]
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE PURCHASE_ORDER SET PURCHASE_ORDER_STATUS = ? WHERE PURCHASE_ORDER_ID = ?",
            (new_status, row[0]),
        )
        if new_status == "Received":
            cursor.execute(
                "UPDATE PRODUCT SET PRODUCT_QUANTITY = PRODUCT_QUANTITY + ? WHERE PRODUCT_NAME = ?",
                (row[2], row[1]),
            )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")
        add_to_incoming_stock_table()
        add_to_product_table()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def check_pending_task():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT TASK_STATUS FROM TASK WHERE TASK_ASSIGNED_TO = ?", (username,)
        )
        list_of_task_status = cursor.fetchall()
        conn.commit()
        conn.close()
        pending_task = 0
        for x in list_of_task_status:
            if x[0] == "Pending":
                pending_task += 1
        if pending_task >= 1:
            toast = Notification(
                app_id="IMS",
                title="Pending Task",
                msg=f"There are {pending_task} pending task",
                duration="short",
            )
            toast.set_audio(audio.Default, loop=False)
            toast.show()
        return list_of_task_status

    def fetch_purchase_order_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(PURCHASE_ORDER_ID) FROM PURCHASE_ORDER")
        last_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_id

    def generate_purchase_order_id(prefix="PO"):
        last_id = fetch_purchase_order_last_id()
        if last_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def update_sales_order_status():
        new_status = sales_order_status_entry.get()
        selected = outgoing_stock_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to edit")
            return
        row = outgoing_stock_tree.item(selected)["values"]
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE SALE_ORDER SET SALE_ORDER_STATUS = ? WHERE SALE_ORDER_ID = ?",
            (new_status, row[0]),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record successfully edited")
        add_to_sale_order_table()
        add_to_product_table()
        update_to_be_packed_label()
        update_to_be_shipped_label()
        update_to_be_delivered_label()
        update_total_quantity_in_hand_label()
        update_total_quantity_to_be_received_label()
        update_low_stock_item_label()
        update_total_items_label()

    def fetch_sale_order_stock_data():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SALE_ORDER")
        sale_order = cursor.fetchall()
        conn.commit()
        conn.close()
        return sale_order

    def add_to_sale_order_table():
        outgoing_stocks = fetch_sale_order_stock_data()
        outgoing_stock_tree.delete(*outgoing_stock_tree.get_children())
        for outgoing_stock in outgoing_stocks:
            outgoing_stock_tree.insert("", END, values=outgoing_stock)

    def fetch_sale_order_last_id():
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(SALE_ORDER_ID) FROM SALE_ORDER")
        last_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return last_id

    def generate_sale_order_id(prefix="SO"):
        last_id = fetch_sale_order_last_id()
        if last_id is None:
            return f"{prefix}-001"
        else:
            number_part = str(last_id.split("-")[-1])
            new_number = int(number_part) + 1
            return f"{prefix}-{new_number:03d}"

    def on_sale_order_double_click(event):
        selected_item = outgoing_stock_tree.selection()[0]
        values = outgoing_stock_tree.item(selected_item, "values")

        sale_order_window = customtkinter.CTk()
        sale_order_window.title("Product Details")

        product_selection_frame = customtkinter.CTkFrame(
            master=sale_order_window, border_width=2
        )

        sale_order_product_table_frame = customtkinter.CTkFrame(
            master=sale_order_window
        )

        def fetch_sale_order_product_data():
            conn = sqlite3.connect("Inventory Management System.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM SALE_ORDER_PRODUCT WHERE SALE_ORDER_ID = ?", (values[0],)
            )
            sale_order = cursor.fetchall()
            conn.commit()
            conn.close()
            return sale_order

        def add_to_sale_order_product_table():
            sale_order_products = fetch_sale_order_product_data()
            sale_order_product_tree.delete(*sale_order_product_tree.get_children())
            for sale_order_product in sale_order_products:
                sale_order_product_tree.insert("", END, values=sale_order_product)

        def add_sale_order_product():
            sale_order_id = values[0]
            sale_order_product = product_selection_entry.get()
            sale_order_product_quantity = sales_quantity_entry.get()

            if not sale_order_product_quantity:
                messagebox.showerror("Error", "Please enter all fields")
                return
            else:
                conn = sqlite3.connect("Inventory Management System.db")
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT PRODUCT_QUANTITY FROM PRODUCT WHERE PRODUCT_NAME = ?", (sale_order_product,),
                )
                product_quantity = cursor.fetchone()[0]
                if product_quantity < int(sale_order_product_quantity):
                    messagebox.showerror("Error", "Insufficient quantity")
                    return
                else:
                    conn = sqlite3.connect("Inventory Management System.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO SALE_ORDER_PRODUCT (SALE_ORDER_ID,SALE_ORDER_PRODUCT,SALE_ORDER_PRODUCT_QUANTITY) \
                    VALUES (?,?,?)",
                        (sale_order_id, sale_order_product, sale_order_product_quantity),
                    )
                    cursor.execute(
                        "UPDATE PRODUCT SET PRODUCT_QUANTITY = PRODUCT_QUANTITY - ? WHERE PRODUCT_NAME = ?",
                        (sale_order_product_quantity, sale_order_product),
                    )
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Data has been inserted")
            add_to_sale_order_product_table()
            add_to_product_table()
            update_low_stock_item_label()
            return

        select_product_label = customtkinter.CTkLabel(
            product_selection_frame,
            text="Select Product",
            font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
        )

        product_selection_label = customtkinter.CTkLabel(
            product_selection_frame,
            text="Product to be purchase:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        product_selection_entry = customtkinter.CTkComboBox(
            master=product_selection_frame,
            values=fetch_product_to_list(),
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display"),
            border_width=0,
        )
        sales_quantity_label = customtkinter.CTkLabel(
            product_selection_frame,
            text="Purchase Quantity:",
            font=customtkinter.CTkFont("SF Pro Display"),
        )
        sales_quantity_entry = customtkinter.CTkEntry(
            master=product_selection_frame,
            placeholder_text="Quantity",
            width=230,
            height=30,
            font=customtkinter.CTkFont("SF Pro Display"),
            border_width=0,
        )
        sales_btn = customtkinter.CTkButton(
            master=product_selection_frame,
            text="Add Item",
            command=add_sale_order_product,
            font=customtkinter.CTkFont("SF Pro Display"),
            corner_radius=200,
            fg_color="#007FFF",
            text_color="black",
        )

        style1 = ThemedStyle()
        style1.set_theme("equilux")
        style1.configure(
            "Treeview",
            font=("SF Pro Display", 10),
            rowheight=24,
            foreground="white",
            background="#2a2d2e",
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
        )
        style1.map("Treeview", background=[("selected", "#22559b")])
        style1.configure(
            "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
        )
        style1.map("Treeview.Heading", background=[("active", "#3484F0")])
        style1.configure(
            "DateEntry",
            font=customtkinter.CTkFont("SF Pro Display", 12),
            foreground="white",
            background="#2a2d2e",
            fieldbackground="#343638",
            bordercolor="#343638",
            borderwidth=0,
        )

        sale_order_product_tree = ttk.Treeview(
            master=sale_order_product_table_frame, height=30
        )

        sale_order_product_verscrlbar = customtkinter.CTkScrollbar(
            master=sale_order_product_table_frame,
            orientation="vertical",
            command=sale_order_product_tree.yview,
        )
        sale_order_product_verscrlbar.pack(side="right", fill="y")

        sale_order_product_tree.configure(
            yscrollcommand=sale_order_product_verscrlbar.set
        )
        sale_order_product_tree["columns"] = (
            "SALEORDERID",
            "SALEORDERPRODUCT",
            "SALEORDERPRODUCTQUANTITY",
        )

        sale_order_product_tree.column("#0", width=0, stretch=tk.NO)
        sale_order_product_tree.column("SALEORDERID", anchor=tk.CENTER, width=200)
        sale_order_product_tree.column("SALEORDERPRODUCT", anchor=tk.CENTER, width=200)
        sale_order_product_tree.column("SALEORDERPRODUCTQUANTITY", anchor=tk.CENTER, width=200)

        sale_order_product_tree.heading("SALEORDERID", text="ID")
        sale_order_product_tree.heading("SALEORDERPRODUCT", text="Item")
        sale_order_product_tree.heading("SALEORDERPRODUCTQUANTITY", text="Quantity")

        sale_order_product_tree.pack(side="bottom", fill="both")

        product_selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NW)
        select_product_label.grid(row=0, column=0, padx=10, pady=10)
        product_selection_label.grid(row=1, column=0, padx=10, pady=10)
        product_selection_entry.grid(row=1, column=1, padx=10, pady=10)
        sales_quantity_label.grid(row=2, column=0, padx=10, pady=10)
        sales_quantity_entry.grid(row=2, column=1, padx=10, pady=10)
        sales_btn.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        sale_order_product_table_frame.grid(row=0, column=1, padx=10, pady=10)

        add_to_sale_order_product_table()
        sale_order_window.mainloop()


    def low_stock_vs_total_item_pie_chart(canvas):
        data=[]

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT WHERE PRODUCT_QUANTITY < PRODUCT_MIN_STOCK")
        low_stock_items = cursor.fetchone()[0]
        data.append(low_stock_items)
        conn.commit()
        conn.close()

        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(PRODUCT_ID) FROM PRODUCT")
        total_items = cursor.fetchone()[0]
        data.append(total_items - low_stock_items)
        conn.commit()
        conn.close()

        fig = plt.Figure()
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#e5e5e5')  # Set the figure background color
        ax.set_facecolor('#e5e5e5')  # Set the axes background color
        ax.axis("equal")

        ax.pie(data, labels=["Low Stock", "In Stock"], autopct="%.2f%%", pctdistance=0.85)

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)

        canvas.figure = fig
        canvas.draw()

    def bar_chart(canvas):
        conn = sqlite3.connect("Inventory Management System.db")
        cursor = conn.cursor()
        cursor.execute("SELECT PRODUCT_ID, PRODUCT_QUANTITY FROM PRODUCT")
        data = cursor.fetchall()
        conn.commit()
        conn.close()

        product_ids = [row[0] for row in data]
        product_quantities = [row[1] for row in data]

        fig1 = plt.Figure()
        ax = fig1.add_subplot(111)
        fig1.patch.set_facecolor('#e5e5e5')
        ax.set_facecolor('#e5e5e5')
        ax.bar(product_ids, product_quantities)
        ax.tick_params(axis='x', labelsize=5)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_xlabel('Product Name', fontsize=12)
        ax.set_ylabel('Product Quantity', fontsize=12)
        ax.set_title('Inventory', fontsize=14)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

        canvas.figure = fig1
        canvas.draw()

    def sort_treeview_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: sort_treeview_column(tv, col, not reverse))

    worker_dashboard_frame = customtkinter.CTkFrame(
        master=app, width=1280, height=720, border_width=0
    )
    worker_dashboard_frame.place(x=0, y=0)

    info_frame = customtkinter.CTkFrame(
        master=worker_dashboard_frame, width=1280, height=720
    )
    info_frame.place(x=0, y=0)
    info_tab = customtkinter.CTkTabview(master=info_frame, width=1280, height=720)
    info_tab.place(x=0, y=0)
    tab_0 = info_tab.add("Homepage")
    tab_1 = info_tab.add("Customer")
    tab_2 = info_tab.add("Supplier")
    tab_3 = info_tab.add("Product")
    tab_4 = info_tab.add("Task")
    tab_5 = info_tab.add("Incoming Stock")
    tab_6 = info_tab.add("Outgoing Stock")

    style = ThemedStyle()
    style.set_theme("equilux")
    style.configure(
        "Treeview",
        font=("SF Pro Display", 10),
        rowheight=24,
        foreground="white",
        background="#2a2d2e",
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", "#22559b")])
    style.configure(
        "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
    )
    style.map("Treeview.Heading", background=[("active", "#3484F0")])
    style.configure(
        "DateEntry",
        font=customtkinter.CTkFont("SF Pro Display", 12),
        foreground="white",
        background="#2a2d2e",
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
    )

    welcome_label = customtkinter.CTkLabel(
        master=tab_0,
        text=f"Hello, {username} ",
        font=customtkinter.CTkFont("SF Pro Display", 24, weight="bold"),
    )

    sales_activity_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    sales_activity_title = customtkinter.CTkLabel(
        sales_activity_frame,
        text="Sales Activity",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    total_to_be_packed_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_packed_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_packed_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Packed",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_1 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_to_be_shipped_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_shipped_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_shipped_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Shipped",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_2 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_to_be_delivered_label_1 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text=str(fetch_to_be_delivered_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_to_be_delivered_label_2 = customtkinter.CTkLabel(
        master=sales_activity_frame,
        text="To be Delivered",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_3 = customtkinter.CTkFrame(
        sales_activity_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    inventory_summary_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    inventory_summary_title = customtkinter.CTkLabel(
        inventory_summary_frame,
        text="Inventory Summary",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    total_quantity_in_hand_1 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text=str(fetch_total_quantity_in_hand_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_quantity_in_hand_2 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text="Quantity In Hand",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_4 = customtkinter.CTkFrame(
        inventory_summary_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    total_quantity_to_be_received_1 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text=str(fetch_total_quantity_to_be_received_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    total_quantity_to_be_received_2 = customtkinter.CTkLabel(
        master=inventory_summary_frame,
        text="Quantity To be Received",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_5 = customtkinter.CTkFrame(
        inventory_summary_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    product_details_frame = customtkinter.CTkFrame(
        tab_0, corner_radius=10, border_width=2
    )

    product_details_title = customtkinter.CTkLabel(
        product_details_frame,
        text="Product Details",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=15),
    )

    low_stock_items_1 = customtkinter.CTkLabel(
        master=product_details_frame,
        text=str(fetch_low_stock_item_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    low_stock_items_2 = customtkinter.CTkLabel(
        master=product_details_frame,
        text="Low Stock Items",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_6 = customtkinter.CTkFrame(
        product_details_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    all_items_1 = customtkinter.CTkLabel(
        master=product_details_frame,
        text=str(fetch_total_items_data()),
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    all_items_2 = customtkinter.CTkLabel(
        master=product_details_frame,
        text="Total Items",
        font=customtkinter.CTkFont("SF Pro Display", size=13),
    )

    sales_activity_vertical_separator_7 = customtkinter.CTkFrame(
        product_details_frame, width=2, height=50, fg_color="#CCCCCC"
    )

    welcome_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    sales_activity_frame.grid(row=1, column=0, padx=10, pady=10)
    inventory_summary_frame.grid(row=1, column=1, padx=10, pady=10)
    product_details_frame.grid(row=1, column=2, padx=10, pady=10)
    fig = plt.Figure()
    fig.set_facecolor('#e5e5e5')
    canvas = FigureCanvasTkAgg(fig, master=tab_0)
    canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10, columnspan=3, sticky="W")
    low_stock_vs_total_item_pie_chart(canvas)

    fig1 = plt.Figure()
    fig1.set_facecolor('#e5e5e5')
    canvas1 = FigureCanvasTkAgg(fig1, master=tab_0)
    canvas1.get_tk_widget().grid(row=2, column=1, padx=10, pady=10, columnspan=2)
    bar_chart(canvas1)


    sales_activity_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    total_to_be_packed_label_1.grid(row=1, column=0, padx=20, pady=5)
    total_to_be_packed_label_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_1.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    total_to_be_shipped_label_1.grid(row=1, column=2, padx=20, pady=5)
    total_to_be_shipped_label_2.grid(row=2, column=2, padx=20, pady=5)
    sales_activity_vertical_separator_2.grid(row=1, column=3, rowspan=2, padx=5, pady=5)
    total_to_be_delivered_label_1.grid(row=1, column=4, padx=20, pady=5)
    total_to_be_delivered_label_2.grid(row=2, column=4, padx=20, pady=5)
    # sales_activity_vertical_separator_3.grid(row=1, column=5, rowspan=2, padx=5, pady=5)

    inventory_summary_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    total_quantity_in_hand_1.grid(row=1, column=0, padx=20, pady=5)
    total_quantity_in_hand_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_4.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    total_quantity_to_be_received_1.grid(row=1, column=2, padx=20, pady=5)
    total_quantity_to_be_received_2.grid(row=2, column=2, padx=20, pady=5)
    # sales_activity_vertical_separator_5.grid(row=1, column=3, rowspan=2, padx=5, pady=5)

    product_details_title.grid(row=0, column=0, sticky=W, padx=10, pady=10,columnspan=2)
    low_stock_items_1.grid(row=1, column=0, padx=20, pady=5)
    low_stock_items_2.grid(row=2, column=0, padx=20, pady=5)
    sales_activity_vertical_separator_6.grid(row=1, column=1, rowspan=2, padx=5, pady=5)
    all_items_1.grid(row=1, column=2, padx=20, pady=5)
    all_items_2.grid(row=2, column=2, padx=20, pady=5)
    # sales_activity_vertical_separator_7.grid(row=1, column=3, rowspan=2, padx=5, pady=5)

    tab_0.columnconfigure(1, weight=1)

    customer_table_frame = customtkinter.CTkFrame(master=tab_1, width=1280, height=515)
    customer_table_frame.place(x=0, y=205)

    customer_tree = ttk.Treeview(master=customer_table_frame, height=18)

    customer_verscrlbar = customtkinter.CTkScrollbar(
        master=customer_table_frame, orientation="vertical", command=customer_tree.yview
    )
    customer_verscrlbar.pack(side="right", fill="y")

    customer_tree.configure(yscrollcommand=customer_verscrlbar.set)
    customer_tree["columns"] = (
        "CUSTOMERID",
        "CUSTOMERNAME",
        "CUSOTMEREMAILADDRESS",
        "CUSTOMERCONTACTNO",
    )

    customer_tree.column("#0", width=0, stretch=tk.NO)
    customer_tree.column("CUSTOMERID", anchor=tk.CENTER, width=313)
    customer_tree.column("CUSTOMERNAME", anchor=tk.CENTER, width=313)
    customer_tree.column("CUSOTMEREMAILADDRESS", anchor=tk.CENTER, width=313)
    customer_tree.column("CUSTOMERCONTACTNO", anchor=tk.CENTER, width=313)

    customer_tree.heading("CUSTOMERID", text="ID")
    customer_tree.heading("CUSTOMERNAME", text="Name")
    customer_tree.heading("CUSOTMEREMAILADDRESS", text="Email Address")
    customer_tree.heading("CUSTOMERCONTACTNO", text="Contact No.")

    customer_tree.pack(side="right", fill="both")
    customer_tree.bind("<Double-1>", on_customer_double_click)
    customer_tree.bind("<ButtonRelease>", display_customer_record)

    customer_menu_frame = customtkinter.CTkFrame(
        master=tab_1,
        border_width=2
    )

    insert_customer_data_label = customtkinter.CTkLabel(
        master=customer_menu_frame,
        text="Insert New Customer",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    customer_name_entry_label = customtkinter.CTkLabel(
        master=customer_menu_frame,
        text="Customer Name:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    customer_name_entry = customtkinter.CTkEntry(
        master=customer_menu_frame,
        placeholder_text="Name",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    customer_email_entry_label = customtkinter.CTkLabel(
        master=customer_menu_frame,
        text="Customer Email Address:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    customer_email_entry = customtkinter.CTkEntry(
        master=customer_menu_frame,
        placeholder_text="Email Address",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    customer_contact_entry_label = customtkinter.CTkLabel(
        master=customer_menu_frame,
        text="Customer Contact No.:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    customer_contact_entry = customtkinter.CTkEntry(
        master=customer_menu_frame,
        placeholder_text="Contact No.",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    addcustomer_btn = customtkinter.CTkButton(
        master=customer_menu_frame,
        text="Add",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=add_new_customer_details,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    editcustomer_btn = customtkinter.CTkButton(
        master=customer_menu_frame,
        text="Edit",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=edit_customer_details,
        compound="top",
        corner_radius=200,
        fg_color="#ADD8E6",
        text_color="black",
    )

    deletecustomer_btn = customtkinter.CTkButton(
        master=customer_menu_frame,
        text="Delete",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=delete_customer_record,
        compound="top",
        corner_radius=200,
        fg_color="#ff666d",
        text_color="black",
    )

    customer_menu_frame.grid(row=0, column=0)

    insert_customer_data_label.grid(row=0, column=0, sticky="w", padx=5, pady=5, columnspan=2)

    customer_name_entry_label.grid(row=1, column=0, padx=5, pady=5)
    customer_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    customer_email_entry_label.grid(row=1, column=2, padx=5, pady=5)
    customer_email_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    customer_contact_entry_label.grid(row=1, column=4, padx=5, pady=5)
    customer_contact_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    addcustomer_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    editcustomer_btn.grid(row=2, column=2, padx=5, pady=5, columnspan=2)
    deletecustomer_btn.grid(row=2, column=4, padx=5, pady=5, columnspan=2)

    tab_1.columnconfigure(0, weight=2)

    supplier_table_frame = customtkinter.CTkFrame(master=tab_2, width=1280, height=515)
    supplier_table_frame.place(x=0, y=205)

    supplier_tree = ttk.Treeview(master=supplier_table_frame, height=18)

    supplier_verscrlbar = customtkinter.CTkScrollbar(
        master=supplier_table_frame, orientation="vertical", command=supplier_tree.yview
    )
    supplier_verscrlbar.pack(side="right", fill="y")

    supplier_tree.configure(yscrollcommand=supplier_verscrlbar.set)
    supplier_tree["columns"] = (
        "SUPPLIERID",
        "SUPPLIERNAME",
        "SUPPLIEREMAILADDRESS",
        "SUPPLIERCONTACTNO",
    )

    supplier_tree.column("#0", width=0, stretch=tk.NO)
    supplier_tree.column("SUPPLIERID", anchor=tk.CENTER, width=313)
    supplier_tree.column("SUPPLIERNAME", anchor=tk.CENTER, width=313)
    supplier_tree.column("SUPPLIEREMAILADDRESS", anchor=tk.CENTER, width=313)
    supplier_tree.column("SUPPLIERCONTACTNO", anchor=tk.CENTER, width=313)

    supplier_tree.heading("SUPPLIERID", text="ID")
    supplier_tree.heading("SUPPLIERNAME", text="Name")
    supplier_tree.heading("SUPPLIEREMAILADDRESS", text="Email Address")
    supplier_tree.heading("SUPPLIERCONTACTNO", text="Contact No.")

    supplier_tree.pack(side="right", fill="both")
    supplier_tree.bind("<ButtonRelease>", display_supplier_record)

    supplier_menu_frame = customtkinter.CTkFrame(
        master=tab_2,
        border_width=2
    )

    insert_supplier_data_label = customtkinter.CTkLabel(
        master=supplier_menu_frame,
        text="Insert New Supplier",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    supplier_name_entry_label = customtkinter.CTkLabel(
        master=supplier_menu_frame,
        text="Supplier Name:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    supplier_name_entry = customtkinter.CTkEntry(
        master=supplier_menu_frame,
        placeholder_text="Name",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    supplier_email_entry_label = customtkinter.CTkLabel(
        master=supplier_menu_frame,
        text="Supplier Email Address:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    supplier_email_entry = customtkinter.CTkEntry(
        master=supplier_menu_frame,
        placeholder_text="Email Address",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    supplier_contact_entry_label = customtkinter.CTkLabel(
        master=supplier_menu_frame,
        text="Supplier Contact No.:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    supplier_contact_entry = customtkinter.CTkEntry(
        master=supplier_menu_frame,
        placeholder_text="Contact No.",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    addsupplier_btn = customtkinter.CTkButton(
        master=supplier_menu_frame,
        text="Add",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=add_new_supplier_details,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    editsupplier_btn = customtkinter.CTkButton(
        master=supplier_menu_frame,
        text="Edit",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=edit_supplier_details,
        compound="top",
        corner_radius=200,
        fg_color="#ADD8E6",
        text_color="black",
    )

    deletesupplier_btn = customtkinter.CTkButton(
        master=supplier_menu_frame,
        text="Delete",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=delete_supplier_record,
        compound="top",
        corner_radius=200,
        fg_color="#ff666d",
        text_color="black",
    )

    supplier_menu_frame.grid(row=0, column=0)

    insert_supplier_data_label.grid(row=0, column=0, sticky="w", padx=5, pady=5, columnspan=2)

    supplier_name_entry_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    supplier_name_entry.grid(row=1, column=1, padx=5, pady=5)
    supplier_email_entry_label.grid(row=1, column=2, sticky="w", padx=5, pady=5)
    supplier_email_entry.grid(row=1, column=3, padx=5, pady=5)
    supplier_contact_entry_label.grid(row=1, column=4, sticky="w", padx=5, pady=5)
    supplier_contact_entry.grid(row=1, column=5, padx=5, pady=5)

    addsupplier_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
    editsupplier_btn.grid(row=2, column=2, padx=5, pady=5, columnspan=2)
    deletesupplier_btn.grid(row=2, column=4, padx=5, pady=5, columnspan=2)

    tab_2.columnconfigure(0, weight=2)

    product_table_frame = customtkinter.CTkFrame(master=tab_3, width=1280, height=515)
    product_table_frame.place(x=0, y=205)

    product_tree = ttk.Treeview(master=product_table_frame, height=20)

    product_verscrlbar = customtkinter.CTkScrollbar(
        master=product_table_frame, orientation="vertical", command=product_tree.yview
    )
    product_verscrlbar.pack(side="right", fill="y")

    product_tree.configure(yscrollcommand=product_verscrlbar.set)
    product_tree["columns"] = (
        "PRODUCTID",
        "PRODUCTNAME",
        "PRODUCTQUANTITY",
        "PRODUCTDESCRIPTION",
        "PRODUCTMINSTOCK",
    )

    product_tree.column("#0", width=0, stretch=tk.NO)
    product_tree.column("PRODUCTID", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTNAME", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTQUANTITY", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTDESCRIPTION", anchor=tk.CENTER, width=250)
    product_tree.column("PRODUCTMINSTOCK", anchor=tk.CENTER, width=250)

    product_tree.heading("PRODUCTID", text="ID", command=lambda: sort_treeview_column(product_tree, "PRODUCTID", False))
    product_tree.heading("PRODUCTNAME", text="Name")
    product_tree.heading("PRODUCTQUANTITY", text="Quantity")
    product_tree.heading("PRODUCTDESCRIPTION", text="Description")
    product_tree.heading("PRODUCTMINSTOCK", text="Min. Stock")

    product_tree.pack(side="bottom", fill="both")
    product_tree.bind("<Double-1>", on_product_double_click)
    product_tree.bind("<ButtonRelease>", display_product_record)

    search_entry = customtkinter.CTkEntry(tab_3,placeholder_text="Search", width=1050,)
    search_entry.grid(row=1,column=0, padx=10, pady=10)
    search_entry.bind("<KeyRelease>", search_product)

    product_menu_frame = customtkinter.CTkFrame(
        master=tab_3,
        border_width=2
    )

    insert_product_data_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Insert New Product",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )

    product_id_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product ID:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_id_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="ID",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_name_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Name:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_name_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Item",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_quantity_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Quantity:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_quantity_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Quantity",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_description_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Description:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_description_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Description",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    product_min_stock_entry_label = customtkinter.CTkLabel(
        master=product_menu_frame,
        text="Product Min. Stock:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )

    product_min_stock_entry = customtkinter.CTkEntry(
        master=product_menu_frame,
        placeholder_text="Min. Stock",
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )

    addproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Add Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=add_new_product_details,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    editproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Edit Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=edit_product_details,
        compound="top",
        corner_radius=200,
        fg_color="#ADD8E6",
        text_color="black",
    )

    deleteproduct_btn = customtkinter.CTkButton(
        master=product_menu_frame,
        text="Delete Product",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=delete_product_record,
        compound="top",
        corner_radius=200,
        fg_color="#ff666d",
        text_color="black",
    )

    product_menu_frame.grid(row=0, column=0)

    insert_product_data_label.grid(
        row=0, column=0, sticky="w", padx=5, pady=5, columnspan=2
    )

    product_id_entry_label.grid(row=1, column=0, padx=5)
    product_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    product_name_entry_label.grid(row=1, column=2, padx=5)
    product_name_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    product_quantity_entry_label.grid(row=1, column=4, padx=5)
    product_quantity_entry.grid(row=1, column=5, padx=5, pady=5, sticky="w")
    product_description_entry_label.grid(row=2, column=0, padx=5)
    product_description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    product_min_stock_entry_label.grid(row=2, column=2, padx=5)
    product_min_stock_entry.grid(row=2, column=3, padx=5, pady=5)

    addproduct_btn.grid(row=3, column=0, padx=20, pady=5, columnspan=2)
    editproduct_btn.grid(row=3, column=2, padx=20, pady=5, columnspan=2)
    deleteproduct_btn.grid(row=3, column=4, padx=20, pady=5, columnspan=2)

    product_menu_frame.columnconfigure(1, weight=3)

    tab_3.columnconfigure(0, weight=2)

    task_table_frame = customtkinter.CTkFrame(master=tab_4, width=1280, height=515)
    task_table_frame.place(x=0, y=205)

    task_tree = ttk.Treeview(master=task_table_frame, height=20)

    task_verscrlbar = customtkinter.CTkScrollbar(
        master=task_table_frame, orientation="vertical", command=task_tree.yview
    )
    task_verscrlbar.pack(side="right", fill="y")

    task_tree.configure(yscrollcommand=task_verscrlbar.set)
    task_tree["columns"] = ("TASKDESCRIPTION", "TASKSTATUS", "DUEDATE")

    task_tree.column("#0", width=0, stretch=tk.NO)
    task_tree.column("TASKDESCRIPTION", anchor=tk.CENTER, width=418)
    task_tree.column("TASKSTATUS", anchor=tk.CENTER, width=418)
    task_tree.column("DUEDATE", anchor=tk.CENTER, width=418)

    task_tree.heading("TASKDESCRIPTION", text="Task")
    task_tree.heading("TASKSTATUS", text="Status")
    task_tree.heading("DUEDATE", text="Due Date")

    task_tree.pack(side="bottom", fill="both")
    task_tree.bind("<ButtonRelease>", display_product_record)

    completetask_btn = customtkinter.CTkButton(
        master=tab_4,
        text="Complete Task",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=complete_task,
        compound="top",
        corner_radius=200,
        text_color="black",
        width=150,
        height=50,
    )
    completetask_btn.pack(anchor="center", pady=20)

    incoming_stock_table_frame = customtkinter.CTkFrame(
        master=tab_5, width=1006, height=515
    )
    incoming_stock_table_frame.place(x=0, y=205)

    incoming_stock_tree = ttk.Treeview(master=incoming_stock_table_frame, height=20)

    incoming_stock_verscrlbar = customtkinter.CTkScrollbar(
        master=incoming_stock_table_frame,
        orientation="vertical",
        command=incoming_stock_tree.yview,
    )
    incoming_stock_verscrlbar.pack(side="right", fill="y")

    incoming_stock_tree.configure(yscrollcommand=incoming_stock_verscrlbar.set)
    incoming_stock_tree["columns"] = (
        "INCOMINGSTOCKID",
        "INCOMINGSTOCKNAME",
        "INCOMINGSTOCKQUANTITY",
        "INCOMINGSTOCKSTATUS",
    )

    incoming_stock_tree.column("#0", width=0, stretch=tk.NO)
    incoming_stock_tree.column("INCOMINGSTOCKID", anchor=tk.CENTER, width=310)
    incoming_stock_tree.column("INCOMINGSTOCKNAME", anchor=tk.CENTER, width=310)
    incoming_stock_tree.column("INCOMINGSTOCKQUANTITY", anchor=tk.CENTER, width=310)
    incoming_stock_tree.column("INCOMINGSTOCKSTATUS", anchor=tk.CENTER, width=320)

    incoming_stock_tree.heading("INCOMINGSTOCKID", text="ID")
    incoming_stock_tree.heading("INCOMINGSTOCKNAME", text="Name")
    incoming_stock_tree.heading("INCOMINGSTOCKQUANTITY", text="Quantity")
    incoming_stock_tree.heading("INCOMINGSTOCKSTATUS", text="Status")

    incoming_stock_tree.pack(side="bottom", fill="both")

    incoming_stock_menu_frame = customtkinter.CTkFrame(master=tab_5, border_width=2)

    incoming_stock_tree.tag_configure(
        "To be Received", background="#FFBA00", foreground="black"
    )
    incoming_stock_tree.tag_configure(
        "Received", background="green", foreground="black"
    )

    edit_purchase_order_status_label = customtkinter.CTkLabel(
        master=incoming_stock_menu_frame,
        text="Edit Purchase Order Status",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )
    purchase_order_status_label = customtkinter.CTkLabel(
        master=incoming_stock_menu_frame,
        text="Status:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )
    purchase_order_status_entry = customtkinter.CTkComboBox(
        master=incoming_stock_menu_frame,
        values=["To be Received", "Received"],
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    editpurchaseorder_btn = customtkinter.CTkButton(
        master=incoming_stock_menu_frame,
        text="Edit Status",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=update_purchase_order_status,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    incoming_stock_menu_frame.grid(row=0, column=0, pady=10)
    edit_purchase_order_status_label.grid(row=0, column=0, padx=10, pady=10)
    purchase_order_status_label.grid(row=1, column=0, padx=5, pady=5)
    purchase_order_status_entry.grid(row=1, column=1, padx=5, pady=5)
    editpurchaseorder_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

    tab_5.columnconfigure(0, weight=1)

    outgoing_stock_table_frame = customtkinter.CTkFrame(
        master=tab_6, width=1006, height=515
    )
    outgoing_stock_table_frame.place(x=0, y=205)

    outgoing_stock_tree = ttk.Treeview(master=outgoing_stock_table_frame, height=20)

    outgoing_stock_verscrlbar = customtkinter.CTkScrollbar(
        master=outgoing_stock_table_frame,
        orientation="vertical",
        command=outgoing_stock_tree.yview,
    )
    outgoing_stock_verscrlbar.pack(side="right", fill="y")

    outgoing_stock_tree.configure(yscrollcommand=outgoing_stock_verscrlbar.set)
    outgoing_stock_tree["columns"] = (
        "OUTGOINGSTOCKID",
        "OUTGOINGSTOCKNAME",
        "OUTGOINGSTOCKQUANTITY",
        "OUTGOINGSTOCKSTATUS"
    )

    outgoing_stock_tree.column("#0", width=0, stretch=tk.NO)
    outgoing_stock_tree.column("OUTGOINGSTOCKID", anchor=tk.CENTER, width=313)
    outgoing_stock_tree.column("OUTGOINGSTOCKNAME", anchor=tk.CENTER, width=313)
    outgoing_stock_tree.column("OUTGOINGSTOCKQUANTITY", anchor=tk.CENTER, width=313)
    outgoing_stock_tree.column("OUTGOINGSTOCKSTATUS", anchor=tk.CENTER, width=313)

    outgoing_stock_tree.heading("OUTGOINGSTOCKID", text="ID")
    outgoing_stock_tree.heading("OUTGOINGSTOCKNAME", text="Date Created")
    outgoing_stock_tree.heading("OUTGOINGSTOCKQUANTITY", text="Customer Name")
    outgoing_stock_tree.heading("OUTGOINGSTOCKSTATUS", text="Status")

    outgoing_stock_tree.pack(side="bottom", fill="both")

    outgoing_stock_tree.bind("<Double-1>", on_sale_order_double_click)

    outgoing_stock_menu_frame = customtkinter.CTkFrame(master=tab_6, border_width=2)

    edit_sales_order_status_label = customtkinter.CTkLabel(
        master=outgoing_stock_menu_frame,
        text="Edit Sales Order Status",
        font=customtkinter.CTkFont("SF Pro Display", weight="bold", size=20),
    )
    sales_order_status_label = customtkinter.CTkLabel(
        master=outgoing_stock_menu_frame,
        text="Status:",
        font=customtkinter.CTkFont("SF Pro Display"),
    )
    sales_order_status_entry = customtkinter.CTkComboBox(
        master=outgoing_stock_menu_frame,
        values=["To be Packed", "To be Shipped", "To be Delivered", "Delivered"],
        width=230,
        height=30,
        font=customtkinter.CTkFont("SF Pro Display"),
        border_width=0,
    )
    editsalesorder_btn = customtkinter.CTkButton(
        master=outgoing_stock_menu_frame,
        text="Edit Status",
        font=customtkinter.CTkFont("SF Pro Display"),
        command=update_sales_order_status,
        compound="top",
        corner_radius=200,
        fg_color="#007FFF",
        text_color="black",
    )

    outgoing_stock_menu_frame.grid(row=0, column=0, pady=10)
    edit_sales_order_status_label.grid(row=0, column=0, padx=10, pady=10)
    sales_order_status_label.grid(row=1, column=0, padx=5, pady=5)
    sales_order_status_entry.grid(row=1, column=1, padx=5, pady=5)
    editsalesorder_btn.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

    tab_6.columnconfigure(0, weight=2)

    add_to_customer_table()
    add_to_supplier_table()
    add_to_product_table()
    add_to_task_table()
    check_task_status()
    check_pending_task()
    check_task_due_date()
    add_to_incoming_stock_table()
    add_to_sale_order_table()


login_page()
#admin_dashboard("admin")
#supervisor_dashboard("supervisor")
#worker_dashboard("worker1")
app.mainloop()
