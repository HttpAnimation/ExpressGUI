import re
import subprocess
import tkinter as tk
from tkinter import ttk
import webbrowser


def get_current_location():
    command = ["expressvpn", "status"]
    output = subprocess.check_output(command, text=True)
    match = re.search(r"Connected to (.+)", output)
    if match:
        return match.group(1)
    return None


def connect_to_location(location):
    current_location = get_current_location()
    if current_location:
        disconnect()

    location_name = re.sub(r"\s+\S+.*$", "", location).strip()
    command = ["expressvpn", "connect", location_name]
    subprocess.run(command)


def disconnect():
    command = ["expressvpn", "disconnect"]
    subprocess.run(command)


def open_github():
    webbrowser.open("https://github.com/HttpAnimation/ExpressGUI")


def main():
    # Get the list of ExpressVPN locations
    command = ["expressvpn", "list", "all"]
    output = subprocess.check_output(command, text=True)
    locations = output.splitlines()

    # Create the GUI
    window = tk.Tk()
    window.title("ExpressGUI")
    window.configure(bg="#1c1c1c")  # Set background color to dark gray

    # Set the size of the GUI window
    window.geometry("500x600")

    # Create a frame to hold the canvas and scrollbar
    frame = tk.Frame(window, bg="#1c1c1c")  # Set frame background color to dark gray
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas with a scrollbar
    canvas = tk.Canvas(frame, bg="#1c1c1c", highlightthickness=0)  # Set canvas background color to dark gray
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas for the buttons
    inner_frame = tk.Frame(canvas, bg="#1c1c1c")  # Set inner frame background color to dark gray
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    for location in locations:
        btn = tk.Button(inner_frame, text=location, command=lambda loc=location: connect_to_location(loc),
                        bg="#2a2a2a", fg="#ffffff", bd=0, pady=10, padx=15, relief=tk.FLAT,
                        activebackground="#363636", activeforeground="#ffffff",
                        font=("Arial", 10, "bold"))
        btn.pack(pady=5)

    # GitHub button
    github_btn = tk.Button(window, text="GitHub", command=open_github,
                           bg="#1976D2", fg="#ffffff", bd=0, pady=10, padx=15, relief=tk.FLAT,
                           activebackground="#0D47A1", activeforeground="#ffffff",
                           font=("Arial", 10, "bold"))
    github_btn.pack(side=tk.RIGHT, pady=10, padx=10)

        # Disconnect button
    disconnect_btn = tk.Button(window, text="Disconnect", command=disconnect,
                               bg="#c62828", fg="#ffffff", bd=0, pady=10, padx=15, relief=tk.FLAT,
                               activebackground="#b71c1c", activeforeground="#ffffff",
                               font=("Arial", 10, "bold"))
    disconnect_btn.pack(pady=10)

    # Configure the canvas to scroll properly
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind the scrollbar to the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=canvas.yview)

    window.mainloop()


if __name__ == "__main__":
    main()
