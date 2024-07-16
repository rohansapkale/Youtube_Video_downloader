import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import os
from PIL import Image, ImageTk

def download_video():
    video_url = url_entry.get()
    output_path = os.getcwd()
    selected_quality = quality_var.get()
    
    try:
        yt = YouTube(video_url)
        
        # You need to set the cookies if the video is age-restricted
        if yt.age_restricted:
            cookies_file = filedialog.askopenfilename(title="Select Cookies File", filetypes=[("Cookies Files", "*.txt")])
            if cookies_file:
                yt = YouTube(video_url, cookies=cookies_file)
            else:
                raise ValueError("No cookies file selected.")
        
        # Get the stream based on selected quality
        stream = yt.streams.filter(progressive=True, file_extension='mp4', res=selected_quality).first()
        
        # If no stream is found for the selected quality, raise an error
        if not stream:
            raise ValueError("No video found for the selected quality.")
        
        output_file = os.path.join(output_path, stream.default_filename)
        stream.download(output_path)
        messagebox.showinfo("Success", f"Download successful! Video saved as: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def choose_output_path():
    selected_path = filedialog.askdirectory()
    output_path_var.set(selected_path)

def open_main_gui():
    welcome_window.destroy()
    root.deiconify()

# Create the welcome window
welcome_window = tk.Tk()
welcome_window.title("Welcome to YouTube Video Downloader")

# Get screen width and height
screen_width = welcome_window.winfo_screenwidth()
screen_height = welcome_window.winfo_screenheight()

# Set window size and position
window_width = 400
window_height = 300
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
welcome_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set background color to black
welcome_window.configure(bg='black')

# Welcome message
welcome_label = tk.Label(welcome_window, text="Welcome to YouTube Video Downloader!", bg='black', fg='white', font=('Helvetica', 16))
welcome_label.pack(pady=20)

# Loading GIF
loading_image = Image.open("loading.png")
loading_photo = ImageTk.PhotoImage(loading_image)
loading_label = tk.Label(welcome_window, image=loading_photo, bg='black')
loading_label.image = loading_photo
loading_label.pack(side=tk.BOTTOM, pady=20)

# Hide the window after 5 seconds and open the main GUI
welcome_window.after(5000, open_main_gui)

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Set window size and position
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set background color to black
root.configure(bg='black')

# Instructions label
instructions_label = tk.Label(root, text="Enter the YouTube video URL and select the output path and video quality.", bg='black', fg='white')
instructions_label.pack(pady=10)

# URL entry
url_frame = tk.Frame(root, bg='black')
url_frame.pack(pady=5)

tk.Label(url_frame, text="YouTube Video URL:", bg='black', fg='white').pack(side=tk.LEFT)
url_entry = tk.Entry(url_frame, width=50)
url_entry.pack(side=tk.LEFT)

# Output path selection
output_path_frame = tk.Frame(root, bg='black')
output_path_frame.pack(pady=5)

tk.Label(output_path_frame, text="Output Path:", bg='black', fg='white').pack(side=tk.LEFT)
output_path_var = tk.StringVar()
output_path_var.set(os.getcwd())  # Set default value to current directory
output_path_entry = tk.Entry(output_path_frame, textvariable=output_path_var, width=40)
output_path_entry.pack(side=tk.LEFT)
output_path_button = tk.Button(output_path_frame, text="Browse", command=choose_output_path)
output_path_button.pack(side=tk.LEFT)

# Quality selection
quality_frame = tk.Frame(root, bg='black')
quality_frame.pack(pady=5)

tk.Label(quality_frame, text="Video Quality:", bg='black', fg='white').pack(side=tk.LEFT)
quality_var = tk.StringVar()
quality_var.set("720p")  # Set default quality
quality_options = ["144p", "240p", "360p", "480p", "720p", "1080p"]
quality_menu = tk.OptionMenu(quality_frame, quality_var, *quality_options)
quality_menu.config(width=10)  # Adjust width here
quality_menu.pack(side=tk.LEFT)
selected_quality_label = tk.Label(quality_frame, textvariable=quality_var, bg='black', fg='white', padx=10)
selected_quality_label.pack(side=tk.LEFT)

# Download button
def on_enter(e):
    download_button.config(bg='dark blue')
    
def on_leave(e):
    download_button.config(bg='blue')

download_button = tk.Button(root, text="Download Video", command=download_video, bg='blue', fg='white')
download_button.pack(pady=10)
download_button.bind("<Enter>", on_enter)
download_button.bind("<Leave>", on_leave)

# Hide the main window initially
root.withdraw()

# Run the main event loop
welcome_window.mainloop()
