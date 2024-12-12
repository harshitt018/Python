import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import sqlite3

# For data initilizatoin. 
def initialize_database():
    conn = sqlite3.connect('blood_bank.db')
    cursor = conn.cursor()

    # Records of the donar.
    cursor.execute('''CREATE TABLE IF NOT EXISTS donors (
                    donor_id INTEGER PRIMARY KEY,
                    name TEXT,
                    blood_group TEXT,
                    age INTEGER,
                    contact_no TEXT)''')

    conn.commit()
    conn.close()

# Too search and display the record
def search_record():
    donor_id = entry_id.get()

    if not donor_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid numeric Donor ID")
        return

    conn = sqlite3.connect('blood_bank.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donors WHERE donor_id=?", (donor_id,))
    record = cursor.fetchone()

    if record:
        entry_name.delete(0, tk.END)
        entry_name.insert(0, record[1])

        entry_blood_group.delete(0, tk.END)
        entry_blood_group.insert(0, record[2])

        entry_age.delete(0, tk.END)
        entry_age.insert(0, record[3])

        entry_contact_no.delete(0, tk.END)
        entry_contact_no.insert(0, record[4])
    else:
        messagebox.showerror("Error", "Donor not found")
    
    conn.close()

# To modify the record
def modify_record():
    donor_id = entry_id.get()
    name = entry_name.get()
    blood_group = entry_blood_group.get()
    age = entry_age.get()
    contact_no = entry_contact_no.get()

    if not donor_id or not name or not blood_group or not age or not contact_no:
        messagebox.showerror("Error", "All fields are required")
        return
    
    if not donor_id.isdigit():
        messagebox.showerror("Error", "Donor ID must be a number")
        return
    
    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Error", "Age must be a positive number")
        return

    if len(contact_no) != 10 or not contact_no.isdigit():
        messagebox.showerror("Error", "Contact number must be a 10-digit number")
        return

    conn = sqlite3.connect('blood_bank.db')
    cursor = conn.cursor()

    cursor.execute('''UPDATE donors SET name=?, blood_group=?, age=?, contact_no=? WHERE donor_id=?''',
                   (name, blood_group, age, contact_no, donor_id))

    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Record updated successfully")
    else:
        messagebox.showerror("Error", "Donor not found")

    conn.close()

# To clear fields
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_blood_group.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_contact_no.delete(0, tk.END)

# To display all donors in a table
def display_all_donors():
    conn = sqlite3.connect('blood_bank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    records = cursor.fetchall()
    conn.close()

    # Clear the tree view before inserting new rows
    for row in donor_table.get_children():
        donor_table.delete(row)

    for row in records:
        donor_table.insert('', 'end', values=row)

# Function to add a new record to the database
def add_record():
    name = entry_name.get()
    blood_group = entry_blood_group.get()
    age = entry_age.get()
    contact_no = entry_contact_no.get()

    if not name or not blood_group or not age or not contact_no:
        messagebox.showerror("Error", "All fields are required")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Error", "Age must be a positive number")
        return

    if len(contact_no) != 10 or not contact_no.isdigit():
        messagebox.showerror("Error", "Contact number must be a 10-digit number")
        return

    conn = sqlite3.connect('blood_bank.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO donors (name, blood_group, age, contact_no) VALUES (?, ?, ?, ?)''',
                   (name, blood_group, age, contact_no))

    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Record added successfully")
    clear_fields()
    display_all_donors()

# Function to delete a donor from the database
def delete_record():
    donor_id = entry_id.get()

    if not donor_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid numeric Donor ID")
        return

    conn = sqlite3.connect('blood_bank.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM donors WHERE donor_id=?", (donor_id,))

    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Success", "Record deleted successfully")
        clear_fields()
        display_all_donors()
    else:
        messagebox.showerror("Error", "Donor not found")

    conn.close()

# Function to verify login credentials
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "raj" and password == "123":
        login_window.destroy()  # Close the login window
        initialize_database()  # Initialize the database
        main_window()  # Launch the main application window
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to create the main application window
def main_window():
    # Create the main window
    root = tk.Tk()
    root.title("Advanced Blood Bank Record Modifier")

    # Load and display the logo image
    image_path = "Blood_bank-removebg-preview.png"  # Path to the uploaded image
    img = Image.open(image_path)
    img = img.resize((300, 150), Image.LANCZOS)  # Resize the image as needed
    photo = ImageTk.PhotoImage(img)

    logo_label = tk.Label(root, image=photo)
    logo_label.grid(row=0, column=0, padx=20, pady=20)

    # Creating a frame for the form input
    form_frame = ttk.LabelFrame(root, text="Donor Details", padding=(20, 10))
    form_frame.grid(row=1, column=0, padx=20, pady=20)

    # Labels and entries for input
    ttk.Label(form_frame, text="Donor ID:").grid(row=0, column=0, padx=10, pady=10)
    global entry_id
    entry_id = ttk.Entry(form_frame)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(form_frame, text="Name:").grid(row=1, column=0, padx=10, pady=10)
    global entry_name
    entry_name = ttk.Entry(form_frame)
    entry_name.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(form_frame, text="Blood Group:").grid(row=2, column=0, padx=10, pady=10)
    global entry_blood_group
    entry_blood_group = ttk.Entry(form_frame)
    entry_blood_group.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(form_frame, text="Age:").grid(row=3, column=0, padx=10, pady=10)
    global entry_age
    entry_age = ttk.Entry(form_frame)
    entry_age.grid(row=3, column=1, padx=10, pady=10)

    ttk.Label(form_frame, text="Contact No.:").grid(row=4, column=0, padx=10, pady=10)
    global entry_contact_no
    entry_contact_no = ttk.Entry(form_frame)
    entry_contact_no.grid(row=4, column=1, padx=10, pady=10)

    # Buttons for actions
    button_frame = ttk.Frame(form_frame)
    button_frame.grid(row=5, column=0, columnspan=2, pady=10)

    ttk.Button(button_frame, text="Add", command=add_record).grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Search", command=search_record).grid(row=0, column=1, padx=10)
    ttk.Button(button_frame, text="Modify", command=modify_record).grid(row=0, column=2, padx=10)
    ttk.Button(button_frame, text="Delete", command=delete_record).grid(row=0, column=3, padx=10)
    ttk.Button(button_frame, text="Clear", command=clear_fields).grid(row=0, column=4, padx=10)
    # Exit button to close the application properly
    ttk.Button(button_frame, text="Exit", command=root.destroy).grid(row=0, column=5, padx=10)

    # Table to display donor records
    table_frame = ttk.LabelFrame(root, text="All Donors", padding=(20, 10))
    table_frame.grid(row=2, column=0, padx=20, pady=20)

    columns = ("ID", "Name", "Blood Group", "Age", "Contact No")
    global donor_table
    donor_table = ttk.Treeview(table_frame, columns=columns, show="headings")
    donor_table.grid(row=0, column=0)

    for col in columns:
        donor_table.heading(col, text=col)

    # Add a scrollbar to the table
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=donor_table.yview)
    donor_table.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Button to display all records
    ttk.Button(root, text="Show All Donors", command=display_all_donors).grid(row=3, column=0, padx=10, pady=10)

    root.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

# Login form
ttk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
entry_username = ttk.Entry(login_window)
entry_username.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
entry_password = ttk.Entry(login_window, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

ttk.Button(login_window, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)

login_window.mainloop()
