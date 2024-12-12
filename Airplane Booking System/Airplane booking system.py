import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import sqlite3

conn = sqlite3.connect('airplane_booking.db')
cursor = conn.cursor()

def recreate_table():
    cursor.execute('DROP TABLE IF EXISTS bookings')
    cursor.execute('''CREATE TABLE bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        flight TEXT NOT NULL,
        date TEXT NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        gender TEXT NOT NULL
    )''')
    conn.commit()

recreate_table()

user_data = {
    "admin": "password",
    "harshit": "jaiswal"
}

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username in user_data and password == user_data[username]:
        messagebox.showinfo("Login", "Login Successful")
        root.withdraw()
        show_booking_screen()
    else:
        messagebox.showerror("Login", "Invalid Username or Password")

def show_booking_screen():
    booking_screen = tk.Toplevel(root)
    booking_screen.title("Book Your Flight")
    booking_screen.configure(bg="#e3f2fd")
    booking_screen.geometry("500x600")
    center_window(booking_screen)

    label_font = ("Helvetica", 14, "bold")
    entry_font = ("Arial", 12)
    button_font = ("Verdana", 12, "bold")
    highlight_color = "#1e88e5"

    tk.Label(booking_screen, text="Passenger Name", bg="#e3f2fd", font=label_font, fg=highlight_color).grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(booking_screen, font=entry_font)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(booking_screen, text="Flight Number", bg="#e3f2fd", font=label_font, fg=highlight_color).grid(row=1, column=0, padx=10, pady=5)
    flight_entry = tk.Entry(booking_screen, font=entry_font)
    flight_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(booking_screen, text="Date", bg="#e3f2fd", font=label_font, fg=highlight_color).grid(row=2, column=0, padx=10, pady=5)
    date_var = tk.StringVar()
    date_entry = tk.Entry(booking_screen, textvariable=date_var, font=entry_font)
    date_entry.grid(row=2, column=1, padx=10, pady=5)
    date_button = tk.Button(booking_screen, text="📅", command=lambda: open_calendar(date_var), font=("Arial", 12), bg="#e3f2fd")
    date_button.grid(row=2, column=2, padx=5)

    tk.Label(booking_screen, text="Source", bg="#e3f2fd", font=label_font, fg=highlight_color).grid(row=3, column=0, padx=10, pady=5)
    source_entry = tk.Entry(booking_screen, font=entry_font)
    source_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(booking_screen, text="Destination", bg="#e3f2fd", font=label_font, fg=highlight_color).grid(row=4, column=0, padx=10, pady=5)
    destination_entry = tk.Entry(booking_screen, font=entry_font)
    destination_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(booking_screen, text="Gender", bg="#e3f2fd", font=label_font, fg=highlight_color).grid(row=5, column=0, padx=10, pady=5)
    gender_var = tk.StringVar()
    gender_dropdown = ttk.Combobox(booking_screen, textvariable=gender_var, font=entry_font)
    gender_dropdown['values'] = ('Male', 'Female', 'Other')
    gender_dropdown.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(
        booking_screen,
        text="Book",
        command=lambda: book_ticket(
            name_entry.get(),
            flight_entry.get(),
            date_var.get(),
            source_entry.get(),
            destination_entry.get(),
            gender_var.get()
        ),
        bg="#43a047",
        fg="white",
        font=button_font
    ).grid(row=6, columnspan=2, pady=10)

    tk.Button(
        booking_screen,
        text="View Bookings",
        command=view_list,
        bg="#1e88e5",
        fg="white",
        font=button_font
    ).grid(row=7, columnspan=2, pady=10)

def open_calendar(date_var):
    cal_popup = tk.Toplevel(root)
    cal_popup.title("Select Date")
    cal_popup.geometry("250x250")
    calendar = Calendar(cal_popup, date_pattern="yyyy-mm-dd")
    calendar.pack(pady=10)
    tk.Button(
        cal_popup,
        text="Select",
        command=lambda: [date_var.set(calendar.get_date()), cal_popup.destroy()],
        bg="#1976d2",
        fg="white"
    ).pack(pady=10)

def book_ticket(name, flight, date, source, destination, gender):
    try:
        cursor.execute('INSERT INTO bookings (name, flight, date, source, destination, gender) VALUES (?, ?, ?, ?, ?, ?)',
                       (name, flight, date, source, destination, gender))
        conn.commit()
        messagebox.showinfo("Booking", "Ticket Booked Successfully")
    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Error", str(e))

def view_list():
    list_window = tk.Toplevel(root)
    list_window.title("View Bookings")
    list_window.configure(bg="#fffde7")
    list_window.geometry("600x400")
    center_window(list_window)

    tree = ttk.Treeview(list_window, columns=("ID", "Name", "Flight", "Date", "Source", "Destination", "Gender"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Flight", text="Flight")
    tree.heading("Date", text="Date")
    tree.heading("Source", text="Source")
    tree.heading("Destination", text="Destination")
    tree.heading("Gender", text="Gender")
    tree.pack(pady=10)

    cursor.execute('SELECT * FROM bookings')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

    tk.Button(
        list_window,
        text="Delete Selected",
        command=lambda: delete_list(tree),
        bg="#d32f2f",
        fg="white",
        font=("Verdana", 12, "bold")
    ).pack(pady=10)

def delete_list(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showinfo("Delete", "No bookings available to delete.")
        return
    item_id = tree.item(selected_item[0], 'values')[0]
    tree.delete(selected_item[0])
    cursor.execute('DELETE FROM bookings WHERE id=?', (item_id,))
    conn.commit()
    messagebox.showinfo("Delete", "Record Deleted Successfully")

def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

root = tk.Tk()
root.title("Welcome to the Airplane Ticket Booking System")
root.configure(bg="#ffe0b2")
root.geometry("400x300")
center_window(root)

tk.Label(root, text="Student: Harshit Jaiswal", bg="#ffe0b2", fg="blue", font=("Georgia", 18, "bold")).grid(row=0, columnspan=2, pady=10)

tk.Label(root, text="Username", bg="#ffe0b2", font=("Calibri", 14), fg="darkred").grid(row=1, column=0, padx=10, pady=5)
username_entry = tk.Entry(root, font=("Calibri", 14))
username_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Password", bg="#ffe0b2", font=("Calibri", 14), fg="darkred").grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show='*', font=("Calibri", 14))
password_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Login", command=login, bg="#1976d2", fg="white", font=("Arial", 14, "bold")).grid(row=3, columnspan=2, pady=10)

root.mainloop()
