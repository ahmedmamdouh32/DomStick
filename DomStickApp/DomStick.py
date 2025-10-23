import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import serial.tools.list_ports
import threading
from pynput.keyboard import Controller, Key

theme_color = "#0078D7"  # "#254C99"


class DomstickApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DomStick Controller")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        self.root.configure(bg="white")

        # Variables
        self.selected_port = tk.StringVar()
        self.serial_connection = None
        self.listening_thread = None
        self.stop_thread = False
        self.keyboard = Controller()

        # -------------------- Toolbar --------------------
        toolbar = tk.Frame(self.root, bg=theme_color, height=50)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(toolbar, text="DomStick", bg=theme_color,
                               fg="white", font=("Segoe UI", 14, "bold"))
        title_label.pack(pady=10)

        # -------------------- Domstick Image --------------------
        img = Image.open("Resources\\DomStick.png")
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        self.domstick_img = ImageTk.PhotoImage(img)

        img_label = tk.Label(self.root, image=self.domstick_img, bg="white")
        img_label.pack(pady=25)

        # -------------------- Port Selection + Connect --------------------
        port_frame = tk.Frame(self.root, bg="white")
        port_frame.pack()

        # Top refresh button
        refresh_button = tk.Button(port_frame, text="⟳", bg=theme_color, fg="white",
                                   font=("Segoe UI", 10, "bold"), width=3, height=1,
                                   command=self.refresh_ports, relief="flat", cursor="hand2")
        refresh_button.pack(anchor="w", pady=(0, 3), padx=121)  # align to the right above combo box

        # Bottom row (label, combobox, connect)
        bottom_row = tk.Frame(port_frame, bg="white")
        bottom_row.pack()

        tk.Label(bottom_row, text="Select COM Port:", bg="white", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)

        self.port_menu = ttk.Combobox(bottom_row, textvariable=self.selected_port, width=15, state="readonly")
        self.port_menu.pack(side=tk.LEFT, padx=5)

        self.connect_button = tk.Button(bottom_row, text="Connect", bg=theme_color, fg="white",
                                        font=("Segoe UI", 9, "bold"), width=10,
                                        command=self.start_connection_thread)
        self.connect_button.pack(side=tk.LEFT, padx=5)

        # -------------------- Status Message --------------------
        self.status_label = tk.Label(self.root, text="", bg="white", fg="#0078D7", font=("Segoe UI", 12, "bold"))
        self.status_label.pack(side=tk.BOTTOM, pady=25)
        self.refresh_ports()

    # -------------------- Functions --------------------
    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports() if "Bluetooth" in port.description]
        self.port_menu["values"] = ports
        if ports:
            self.port_menu.current(0)
            self.status_label.config(text="Choose a port to connect", fg="#0078D7")
        else:
            self.status_label.config(text="Is your Bluetooth open ?", fg="#FF6B6B")
            self.port_menu.set("")  #clearing the combo box menu

    def start_connection_thread(self):
        """Start background connection thread."""
        port_name = self.selected_port.get()
        if not port_name:
            self.status_label.config(text="Please select a COM port.", fg="#FF6B6B")
            return

        self.status_label.config(text=f"Connecting to {port_name}...", fg="#0078D7")
        threading.Thread(target=self.connect_port, args=(port_name,), daemon=True).start()

    def connect_port(self, port_name):
        """Try connecting to the selected COM port in a background thread."""
        try:
            #time.sleep(1)  # slight delay for visual effect
            self.serial_connection = serial.Serial(port_name, 9600, timeout=1)
            self.status_label.config(text=f"Connected to {port_name}", fg="green")
            self.connect_button.config(text="Disconnect", command=self.disconnect)
            self.stop_thread = False
            self.start_listening_thread()
        except Exception as e:
            print(e)
            self.status_label.config(text=f"Failed to connect to {port_name}", fg="#FF6B6B")
            self.serial_connection = None

    def disconnect(self):
        """Disconnect serial port and stop listening thread."""
        self.stop_thread = True
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.serial_connection = None
        self.connect_button.config(text="Connect", command=self.start_connection_thread)
        self.status_label.config(text="Disconnected", fg="#FF6B6B")

    def start_listening_thread(self):
        """Start thread to listen for incoming serial data."""
        self.listening_thread = threading.Thread(target=self.listen_serial, daemon=True)
        self.listening_thread.start()

    def listen_serial(self):
        """Listen to incoming serial data and send HID commands."""
        map_press = {
            b'U': Key.up,
            b'D': Key.down,
            b'L': Key.left,
            b'R': Key.right,
            b'E': Key.enter
        }
        map_release = {k.lower(): v for k, v in map_press.items()}

        self.status_label.config(text="Connected Successfully", fg="green")

        try:
            while not self.stop_thread and self.serial_connection and self.serial_connection.is_open:
                c = self.serial_connection.read(1)
                if not c:
                    continue
                if c in map_press:
                    self.keyboard.press(map_press[c])
                else:
                    try:
                        self.keyboard.release(map_release[c])
                    except KeyError:
                        pass
        except Exception as e:
            print("Error in listener:", e)
        finally:
            if not self.stop_thread:
                self.status_label.config(text="Connection lost.", fg="#FF6B6B")
                self.disconnect()


# -------------------- Run App --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DomstickApp(root)
    root.mainloop()