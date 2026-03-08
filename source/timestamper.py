import sys
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os

# FILE_NAME = "timestamps.txt"


if getattr(sys, 'frozen', False):
    # setting base directory when in exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)

FILE_NAME = os.path.join(BASE_DIR, "timestamps.txt")

class TimeStamper:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Stamper")

        root.iconbitmap("icon.ico")

        self.root.geometry("450x600")

        self.timestamps = []
        self.last_timestamp = None

        title = ttk.Label(root, text="TimeStamper", font=("Arial", 24))
        title.pack(pady=10)

        self.current_time_label = ttk.Label(root, text="", font=("Arial", 14))
        self.current_time_label.pack()

        self.elapsed_label = ttk.Label(root, text="Time since last: N/A", font=("Arial", 14))
        self.elapsed_label.pack(pady=5)

        record_btn = tk.Button(
            root,
            text="RECORD TIMESTAMP\n(Press SPACE)",
            font=("Arial", 16),
            height=2,
            width=22,
            bg="#4CAF50",
            fg="white",
            command=self.record_timestamp
        )

        record_btn.pack(pady=10)

        clear_btn = tk.Button(
            root,
            text="CLEAR History",
            font=("Arial", 12),
            height=1,
            width=20,
            bg="#cc4444",
            fg="white",
            command=self.clear_history
        )
        clear_btn.pack()

        # time stamp table
        columns = ("date", "time", "delta")
        self.table = ttk.Treeview(root, columns=columns, show="headings", height=15)

        self.table.heading("date", text="Date")
        self.table.heading("time", text="Time (AM/PM)")
        self.table.heading("delta", text="Δ Since Last")

        self.table.column("date", width=150, anchor="center")
        self.table.column("time", width=150, anchor="center")
        self.table.column("delta", width=120, anchor="center")

        self.table.pack(pady=10, fill="both", expand=True)

        root.bind("<space>", self.space_pressed)

        self.load_timestamps()
        self.update_clock()

    def space_pressed(self, event):
        self.record_timestamp()

    def format_delta(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"

    def record_timestamp(self):
        now = datetime.now()

        save_format = now.strftime("%Y-%m-%d %H:%M:%S")

        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%I:%M:%S %p")

        delta = ""
        if self.last_timestamp:
            diff = int((now - self.last_timestamp).total_seconds())
            delta = self.format_delta(diff)

        # INSERT AT TOP
        self.table.insert("", 0, values=(date, time, delta))

        self.timestamps.append(now)
        self.last_timestamp = now

        with open(FILE_NAME, "a") as f:
            f.write(save_format + "\n")

    def load_timestamps(self):
        if not os.path.exists(FILE_NAME):
            return

        with open(FILE_NAME) as f:
            lines = [line.strip() for line in f if line.strip()]

        lines.reverse()  # newest first

        prev = None

        for line in reversed(lines):   # keeps track of difference in time
            dt = datetime.strptime(line, "%Y-%m-%d %H:%M:%S")

            date = dt.strftime("%Y-%m-%d")
            time = dt.strftime("%I:%M:%S %p")

            delta = ""
            if prev:
                diff = int((dt - prev).total_seconds())
                delta = self.format_delta(diff)

            self.table.insert("", 0, values=(date, time, delta))

            self.timestamps.append(dt)
            prev = dt

        if self.timestamps:
            self.last_timestamp = self.timestamps[-1]

    def clear_history(self):
        self.timestamps.clear()
        self.last_timestamp = None

        for row in self.table.get_children():
            self.table.delete(row)

        open(FILE_NAME, "w").close()

    def update_clock(self):
        now = datetime.now()

        self.current_time_label.config(
            text="Current Time: " + now.strftime("%I:%M:%S %p")

        )

        if self.last_timestamp:
            elapsed = int((now - self.last_timestamp).total_seconds())
            self.elapsed_label.config(
                text="Time since last: " + self.format_delta(elapsed)
            )
        else:
            self.elapsed_label.config(text="Time since last: N/A")

        self.root.after(1000, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    app = TimeStamper(root)
    root.mainloop()