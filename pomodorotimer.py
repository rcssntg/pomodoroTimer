import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import winsound  # Built-in module for Windows sound

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sophia's Pomodoro Timer")
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Add protocol for closing the window
        self.setup_ui()
        self.running = False
        self.work_time = 25 * 60  # 25 minutes
        self.break_time = 5 * 60  # 5 minutes
        self.remaining_time = self.work_time
        self.theme = "light"
        self.apply_theme()

    def setup_ui(self):
        # Set the window size and position
        window_width = 400
        window_height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

        # Current Time Label
        self.current_time_label = tk.Label(self.root, text="", font=("Helvetica", 20))
        self.current_time_label.pack()

        # Timer Label
        self.timer_label = tk.Label(self.root, text="25:00", font=("Helvetica", 40))
        self.timer_label.pack()

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)

        # Control Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        self.start_button = tk.Button(button_frame, text="Start", font=("Helvetica", 12), command=self.start_timer)
        self.start_button.pack(side="left", padx=5)
        self.stop_button = tk.Button(button_frame, text="Stop", font=("Helvetica", 12), command=self.stop_timer)
        self.stop_button.pack(side="left", padx=5)
        self.reset_button = tk.Button(button_frame, text="Reset", font=("Helvetica", 12), command=self.reset_timer)
        self.reset_button.pack(side="left", padx=5)

        # Theme Toggle Button
        self.theme_button = tk.Button(self.root, text="Toggle Dark Mode", font=("Helvetica", 12), command=self.toggle_theme)
        self.theme_button.pack(pady=10)

        # Start the current time update loop
        self.update_current_time()

    def apply_theme(self):
        if self.theme == "light":
            self.root.configure(bg="white")
            self.current_time_label.configure(bg="white", fg="black")
            self.timer_label.configure(bg="white", fg="black")
            self.theme_button.configure(text="Toggle Dark Mode", bg="lightgray", fg="black")
        else:
            self.root.configure(bg="black")
            self.current_time_label.configure(bg="black", fg="white")
            self.timer_label.configure(bg="black", fg="white")
            self.theme_button.configure(text="Toggle Light Mode", bg="gray", fg="white")

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()

    def update_current_time(self):
        self.current_time_label.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_current_time)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.countdown(self.remaining_time)

    def stop_timer(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def reset_timer(self):
        self.stop_timer()
        self.remaining_time = self.work_time
        self.update_timer_label()
        self.progress['value'] = 0

    def countdown(self, seconds):
        if self.running:
            minutes, sec = divmod(seconds, 60)
            self.timer_label.config(text=f'{minutes:02d}:{sec:02d}')
            self.progress['value'] = ((self.work_time - seconds) / self.work_time) * 100
            if seconds > 0:
                self.remaining_time = seconds - 1
                self.root.after(1000, self.countdown, seconds - 1)
            else:
                self.timer_label.config(text="Time's up!")
                self.start_button.config(state="normal")
                self.stop_button.config(state="disabled")
                self.play_beep_sound()
                # Automatically switch to break time after work session ends
                self.remaining_time = self.break_time
                self.start_button.config(state="normal")

    def play_beep_sound(self):
        winsound.Beep(1000, 1000)  # Frequency: 1000 Hz, Duration: 1000 ms (1 second)

    def update_timer_label(self):
        minutes, sec = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f'{minutes:02d}:{sec:02d}')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
