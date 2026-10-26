import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

SERIAL_PORT = 'COM3'  # Change if needed
BAUD_RATE = 115200
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Serial Error: {e}")
    ser = None  # Handle case where serial port fails to open

# Data Storage
MAX_DATA_POINTS = 100  # Store last 100 data points
voltage_data = deque(maxlen=MAX_DATA_POINTS)
current_data = deque(maxlen=MAX_DATA_POINTS)
power_data = deque(maxlen=MAX_DATA_POINTS)
timestamps = deque(maxlen=MAX_DATA_POINTS)  # Store timestamps

# GUI Setup
root = tk.Tk()
root.title("Solar Panel IV Characteristics")
root.geometry("1000x600")  # Initial size

# Frames
frame_left = tk.Frame(root)  # Graph section
frame_right = tk.Frame(root, padx=15)  # Stats section
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_right.pack(side=tk.RIGHT, fill=tk.Y)

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_left)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Labels for efficiency & parameters
labels = {
    "Max Power": ttk.Label(frame_right, text="Max Power: 0W"),
    "Voltage Range": ttk.Label(frame_right, text="Voltage: 0V - 0V"),
    "Current Range": ttk.Label(frame_right, text="Current: 0A - 0A"),
    "Latest Voltage": ttk.Label(frame_right, text="Latest Voltage: 0.00V", font=("Arial", 12)),
    "Latest Current": ttk.Label(frame_right, text="Latest Current: 0.00A", font=("Arial", 12)),
}

for lbl in labels.values():
    lbl.pack(pady=5)

# Function to Update Font Sizes Dynamically
def update_font_size(event=None):
    width = root.winfo_width()
    height = root.winfo_height()
    
    base_size = min(width, height) // 40  # Adjust size relative to window
    font_size = max(10, base_size)  # Prevents text from being too small
    axis_font_size = max(8, base_size - 2)  # Slightly smaller for axis labels

    for lbl in labels.values():
        lbl.config(font=("Arial", font_size))

    # Update graph text sizes
    ax.title.set_fontsize(font_size + 2)  # Slightly larger title
    ax.xaxis.label.set_fontsize(axis_font_size)
    ax.yaxis.label.set_fontsize(axis_font_size)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(axis_font_size)

    canvas.draw()

root.bind("<Configure>", update_font_size)  # Adjust font size on window resize

# Function to update graph and UI
def update(frame):
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line or "," not in line:
                print("Invalid data format, skipping...")
                return

            voltage, current = map(float, line.split(','))  # Expecting "VOLTAGE,CURRENT"
            power = voltage * current

            current_time = datetime.now().strftime("%H:%M:%S")  # Get real-time timestamp

            # Append new values
            voltage_data.append(voltage)
            current_data.append(current)
            power_data.append(power)
            timestamps.append(current_time)  # Append real-time timestamp

            # Update UI labels
            labels["Max Power"].config(text=f"Max Power: {max(power_data):.2f}W")
            labels["Voltage Range"].config(text=f"Voltage: {min(voltage_data):.2f}V - {max(voltage_data):.2f}V")
            labels["Current Range"].config(text=f"Current: {min(current_data):.2f}A - {max(current_data):.2f}A")
            labels["Latest Voltage"].config(text=f"Latest Voltage: {voltage:.2f}V")
            labels["Latest Current"].config(text=f"Latest Current: {current:.2f}A")

            print(f"Test Data: Voltage={voltage:.2f}V, Current={current:.2f}A, Time={current_time}")

        
        except ValueError:
            print("Invalid data received, skipping...")
            return

    
    # Update Graph
    ax.clear()
    ax.plot(range(len(timestamps)), voltage_data, label="Voltage (V)", color='r')
    ax.plot(range(len(timestamps)), current_data, label="Current (A)", color='b')
    ax.plot(range(len(timestamps)), power_data, label="Power (W)", color='g')

    # Keep y-axis scaling dynamic
    ax.set_ylim(0, max(max(voltage_data, default=1), max(current_data, default=1), max(power_data, default=1)) + 1)

    # Dynamic X-Axis Shifting
    if len(timestamps) > 12:
        ax.set_xlim(len(timestamps) - 12, len(timestamps) - 1)  # Properly shifting x-axis
    else:
        ax.set_xlim(0, len(timestamps) - 1)

    # Set X-Ticks Only for the Last 12 Values
    visible_indices = list(range(max(0, len(timestamps) - 12), len(timestamps)))
    ax.set_xticks(visible_indices)  # Only set ticks for last 12 values
    ax.set_xticklabels([timestamps[i] for i in visible_indices], rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin to prevent cropping


    ax.legend()
    ax.set_title("Real-Time IV Characteristics")
    ax.set_xlabel("Time (HH:MM:SS)")
    ax.set_ylabel("Voltage (V) / Current (A) / Power (W)")

    update_font_size()
    canvas.draw()


# Run Animation
ani = animation.FuncAnimation(fig, update, interval=1000)  # Update every second

# Run Main Application
root.mainloop()