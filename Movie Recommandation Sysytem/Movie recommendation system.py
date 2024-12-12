import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import pandas as pd
from PIL import Image, ImageTk

def load_model():
    file_path = filedialog.askopenfilename(filetypes=[("Pickle or CSV files", "*.pkl *.csv")])
    if file_path:
        try:
            global model, data
            if file_path.endswith('.pkl'):
                with open(file_path, 'rb') as file:
                    content = pickle.load(file)
                    if isinstance(content, tuple) and len(content) == 2:
                        model, data = content
                        messagebox.showinfo("Success", "Model and data loaded successfully!")
                    else:
                        messagebox.showerror("Error", "Invalid .pkl file format. Please ensure the file contains a tuple of (model, data).")
            elif file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
                model = None
                messagebox.showinfo("Success", "Data loaded successfully from CSV file!")
            else:
                messagebox.showerror("Error", "Unsupported file type.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model and data: {str(e)}")

def recommend_movies():
    if data is None:
        messagebox.showwarning("Model/Data Not Loaded", "Please load data first.")
        return
    
    movie_name = entry.get()
    if not movie_name:
        messagebox.showwarning("Input Error", "Please enter a movie name!")
        return

    try:
        if model:
            recommended_movies = model.get_recommendations(movie_name, data)
        else:
            similar_movies = data[data['title'].str.contains(movie_name, case=False, na=False)]
            recommended_movies = similar_movies['title'].tolist() if not similar_movies.empty else ["No recommendations available."]
        
        result = "\n".join(recommended_movies)
        recommendation_box.config(state=tk.NORMAL)
        recommendation_box.delete(1.0, tk.END)
        recommendation_box.insert(tk.END, result)
        recommendation_box.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to recommend movies: {str(e)}")

# Main application
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("500x400")

# Load background image
try:
    bg_image = Image.open("C:/Users/HARSHIT JAISWAL/OneDrive/Desktop/Movie Recommandation Sysytem/background.jpg")
    bg_image = bg_image.resize((500, 400), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
except FileNotFoundError:
    messagebox.showerror("Error", "Background image not found. Please ensure 'background.jpg' is in the correct directory.")
    bg_photo = None

canvas = tk.Canvas(root, width=500, height=400)
canvas.pack(fill="both", expand=True)

if bg_photo:
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# UI Elements on the Canvas
load_button = tk.Button(root, text="Load Model & Data", command=load_model, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="raised", width=20)
canvas.create_window(250, 50, window=load_button)  # Place on canvas

label = tk.Label(root, text="Enter a movie you like:", font=("Arial", 12), bg="#F0F8FF", fg="#333333")
canvas.create_window(250, 100, window=label)  # Place on canvas

entry = tk.Entry(root, width=40, font=("Arial", 12), bd=3, relief="solid", fg="#333333", bg="#FFFFFF")
canvas.create_window(250, 140, window=entry)  # Place on canvas

recommend_button = tk.Button(root, text="Recommend Movies", command=recommend_movies, font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="raised", width=20)
canvas.create_window(250, 180, window=recommend_button)  # Place on canvas

recommendation_box = tk.Text(root, height=6, width=40, font=("Arial", 12), bg="#F0F8FF", fg="#333333", bd=3, relief="solid", wrap=tk.WORD)
recommendation_box.config(state=tk.DISABLED)
canvas.create_window(250, 260, window=recommendation_box)  # Place on canvas

model = None
data = None

root.mainloop()
