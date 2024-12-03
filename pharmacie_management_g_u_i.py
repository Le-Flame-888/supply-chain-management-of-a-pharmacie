import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('Pharmacie.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    batch_no TEXT,
    expiry_date TEXT,
    quantity INTEGER,
    reorder_level INTEGER
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact TEXT,
    address TEXT
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicines_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY(medicines_id) REFERENCES medicines(id)
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicines_id INTEGER,
    suppliers_id INTEGER,
    quantity INTEGER,
    order_date DATE,
    status TEXT,
    FOREIGN KEY(medicines_id) REFERENCES medicines(id),
    FOREIGN KEY(suppliers_id) REFERENCES suppliers(id)
)
""")

conn.commit()


def add_medicine():
    try:
        name = name_entry.get()
        batch_no = batch_entry.get()
        expiry_date = expiry_entry.get()
        quantity = quantity_entry.get()
        reorder_level = reorder_entry.get()

        if not (name and batch_no and expiry_date and quantity and reorder_level):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        cursor.execute("""
            INSERT INTO medicines (name, batch_no, expiry_date, quantity, reorder_level)
            VALUES (?, ?, ?, ?, ?)
        """, (name, batch_no, expiry_date, int(quantity), int(reorder_level)))
        conn.commit()
        messagebox.showinfo("Success", "Medicine added successfully")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_sales():
    try:
        quantity = quantity_entry.get()
        saledate = saledate_entry.get()
        prix = prix_entry.get()

        if not (quantity and saledate and prix):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        cursor.execute("""
            INSERT INTO sales (medicines_id, quantity, price)
            VALUES (?, ?, ?)
        """, (1, int(quantity), float(prix)))  # Assuming a dummy medicine_id for now
        conn.commit()
        messagebox.showinfo("Success", "Sale added successfully")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_fields():
    name_entry.delete(0, tk.END)
    batch_entry.delete(0, tk.END)
    expiry_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    reorder_entry.delete(0, tk.END)


def check_stock():
    try:
        cursor.execute("SELECT name FROM medicines WHERE quantity <= reorder_level")
        low_stock = cursor.fetchall()
        for medicine in low_stock:
            print(f"Low stock alert: {medicine[0]}")
    except Exception as e:
        print(f"Error checking stock: {str(e)}")


# GUI setup
app = tk.Tk()
app.title("Pharmacy Supply Chain Management")

tk.Label(app, text="Medicine Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(app)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(app, text="Batch No:").grid(row=1, column=0, padx=10, pady=5)
batch_entry = tk.Entry(app)
batch_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="Expiry Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
expiry_entry = tk.Entry(app)
expiry_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="Quantity:").grid(row=3, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(app)
quantity_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(app, text="Reorder Level:").grid(row=4, column=0, padx=10, pady=5)
reorder_entry = tk.Entry(app)
reorder_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Button(app, text="Add Medicine", command=add_medicine).grid(row=5, column=0, columnspan=2, pady=10)

app.mainloop()