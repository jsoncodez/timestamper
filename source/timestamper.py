import sys
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(__file__)

FILE_NAME = os.path.join(BASE_DIR, "timestamps.txt")


class TimeStamper:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Stamper")

        root.iconbitmap("icon.ico")
        self.root.geometry("700x600")

        self.timestamps = []
        self.last_timestamp = None

        title = tk.Label(root, text="TimeStamper", font=("Segoe UI", 24))
        title.pack(pady=10)

        self.current_time_label = tk.Label(root, text="", font=("Segoe UI", 14))
        self.current_time_label.pack()

        self.elapsed_label = tk.Label(root, text="Time since last: N/A", font=("Segoe UI", 14))
        self.elapsed_label.pack(pady=5)

        record_btn = tk.Button(
            root,
            text="RECORD TIMESTAMP\n(Press SPACE)",
            font=("Segoe UI", 16),
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
            font=("Segoe UI", 12),
            height=1,
            width=20,
            bg="#cc4444",
            fg="white",
            command=self.clear_history
        )
        clear_btn.pack()

        columns = ("date", "time", "delta", "note")
        self.table = ttk.Treeview(root, columns=columns, show="headings", height=15)

        self.table.heading("date", text="Date")
        self.table.heading("time", text="Time (AM/PM)")
        self.table.heading("delta", text="Δ Since Last")
        self.table.heading("note", text="Note")

        self.table.column("date", width=150, anchor="center")
        self.table.column("time", width=150, anchor="center")
        self.table.column("delta", width=120, anchor="center")
        self.table.column("note", width=200, anchor="center")

        self.table.pack(pady=10, fill="both", expand=True)

        root.bind("<space>", self.space_pressed)

        self.load_timestamps()
        self.update_clock()

        self.table.bind("<Double-1>", self.start_edit)
        self.edit_entry = None

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
        note = ""

        if self.last_timestamp:
            diff = int((now - self.last_timestamp).total_seconds())
            delta = self.format_delta(diff)
        else:
            delta = "00:00:00"

        self.table.insert("", 0, values=(date, time, delta, note))

        self.timestamps.append(now)
        self.last_timestamp = now

        with open(FILE_NAME, "a") as f:
            f.write(f"{save_format}|{delta}|{note}\n")

    def start_edit(self, event):
        region = self.table.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.table.identify_row(event.y)
        column = self.table.identify_column(event.x)

        if column != "#4":
            return

        x, y, width, height = self.table.bbox(row_id, column)
        value = self.table.set(row_id, "note")

        self.edit_entry = ttk.Entry(self.table)
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.insert(0, value)
        self.edit_entry.focus()

        self.edit_entry.bind("<Return>", lambda e: self.save_edit(row_id))
        self.edit_entry.bind("<FocusOut>", lambda e: self.save_edit(row_id))

    def save_edit(self, row_id):
        if self.edit_entry:
            new_value = self.edit_entry.get()
            self.table.set(row_id, "note", new_value)
            self.edit_entry.destroy()
            self.edit_entry = None
        self.save_note()

    def save_note(self):
        with open(FILE_NAME, "w") as f:
            for item in self.table.get_children()[::-1]:  # oldest first
                date, time, delta, note = self.table.item(item)["values"]

                dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M:%S %p")
                save_format = dt.strftime("%Y-%m-%d %H:%M:%S")

                f.write(f"{save_format}|{delta}|{note}\n")

    def load_timestamps(self):
        if not os.path.exists(FILE_NAME):
            return

        with open(FILE_NAME) as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            parts = line.split("|")

            if len(parts) == 1:
                # OLD FORMAT SUPPORT
                dt = datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
                delta = ""
                note = ""
            else:
                dt = datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
                delta = parts[1]
                note = parts[2] if len(parts) > 2 else ""

            date = dt.strftime("%Y-%m-%d")
            time = dt.strftime("%I:%M:%S %p")

            self.table.insert("", 0, values=(date, time, delta, note))
            self.timestamps.append(dt)

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


