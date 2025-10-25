import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import serial
import serial.tools.list_ports
import threading
from pynput.keyboard import Controller, Key

theme_color = "#0078D7"  # "#254C99"


class ConfigurationPage:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = tk.Frame(self.parent, bg="white")

        # Create configuration page content
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.frame, text="Configuration Settings",
                               bg="white", fg=theme_color,
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=20)

        # Configuration content area
        content_frame = tk.Frame(self.frame, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # COM Port Settings section
        tk.Label(content_frame, text="COM Port Settings:",
                 bg="white", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 0))

        # Main settings frame for 2x2 layout
        settings_frame = tk.Frame(content_frame, bg="white")
        settings_frame.pack(fill=tk.X, pady=10)

        # Left side frame (Baud rate + Data bits)
        left_frame = tk.Frame(settings_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Right side frame (Stop bits + Parity)
        right_frame = tk.Frame(settings_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # -------------------- LEFT SIDE --------------------
        # Baud rate selection (top left)
        baud_frame = tk.Frame(left_frame, bg="white")
        baud_frame.pack(fill=tk.X, pady=5)
        tk.Label(baud_frame, text="Baud Rate:",
                 bg="white", font=("Consolas", 10)).pack(side=tk.LEFT, padx=(0, 10))

        self.baud_combo = ttk.Combobox(baud_frame,
                                       values=["9600", "19200", "38400", "57600", "115200", "230400", "460800",
                                               "921600"],
                                       state="readonly", width=10)
        self.baud_combo.set("9600")  # Default value
        self.baud_combo.pack(side=tk.LEFT)

        # Data bits selection (bottom left)
        data_bits_frame = tk.Frame(left_frame, bg="white")
        data_bits_frame.pack(fill=tk.X, pady=5)
        tk.Label(data_bits_frame, text="Data Bits:",
                 bg="white", font=("Consolas", 10)).pack(side=tk.LEFT, padx=(0, 10))

        self.data_bits_combo = ttk.Combobox(data_bits_frame,
                                            values=["5", "6", "7", "8"],
                                            state="readonly", width=8)
        self.data_bits_combo.set("8")  # Default value
        self.data_bits_combo.pack(side=tk.LEFT)

        # -------------------- RIGHT SIDE --------------------
        # Stop bits selection (top right)
        stop_bits_frame = tk.Frame(right_frame, bg="white")
        stop_bits_frame.pack(fill=tk.X, pady=5)
        tk.Label(stop_bits_frame, text="Stop Bits:",
                 bg="white", font=("Consolas", 10)).pack(side=tk.LEFT, padx=(0, 10))

        self.stop_bits_combo = ttk.Combobox(stop_bits_frame,
                                            values=["1", "2"],
                                            state="readonly", width=8)
        self.stop_bits_combo.set("1")  # Default value
        self.stop_bits_combo.pack(side=tk.LEFT)

        # Parity selection (bottom right)
        parity_frame = tk.Frame(right_frame, bg="white")
        parity_frame.pack(fill=tk.X, pady=5)
        tk.Label(parity_frame, text="Parity:",
                 bg="white", font=("Consolas", 10)).pack(side=tk.LEFT, padx=(0, 10))

        self.parity_combo = ttk.Combobox(parity_frame,
                                         values=["None", "Even", "Odd"],
                                         state="readonly", width=8)
        self.parity_combo.set("None")  # Default value
        self.parity_combo.pack(side=tk.LEFT)

        # Add more space before buttons
        tk.Frame(content_frame, bg="white", height=30).pack()

        # Bottom buttons frame
        buttons_frame = tk.Frame(self.frame, bg="white")
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        # Close button (left side)
        close_button = tk.Button(buttons_frame, text="Back", bg="#6C757D", fg="white",
                                 font=("Consolas", 10, "bold"), width=10,
                                 command=self.close_configuration)
        close_button.pack(side=tk.LEFT, padx=5)

        # Save button (right side)
        save_button = tk.Button(buttons_frame, text="Save", bg=theme_color, fg="white",
                                font=("Consolas", 10, "bold"), width=10)
        save_button.pack(side=tk.RIGHT, padx=5)
    def close_configuration(self):
        """Return to main page"""
        self.main_app.show_main_page()

    def show(self):
        """Show the configuration page"""
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        """Hide the configuration page"""
        self.frame.pack_forget()


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

        # Configuration page
        self.config_page = ConfigurationPage(self.root, self)

        # Create main page
        self.main_frame = tk.Frame(self.root, bg="white")
        self.create_main_page()

        # Show main page initially
        self.show_main_page()

    def create_main_page(self):
        # -------------------- Toolbar --------------------
        toolbar = tk.Frame(self.main_frame, bg=theme_color, height=50)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        # Configuration button (left side)
        config_button = tk.Button(toolbar, text="⚙", bg=theme_color, fg="white",
                                  font=("Segoe UI", 12, "bold"), width=3, height=1,
                                  command=self.show_configuration, relief="flat", cursor="hand2")
        config_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Title (center)
        title_label = tk.Label(toolbar, text="DomStick", bg=theme_color,
                               fg="white", font=("Segoe UI", 14, "bold"))
        title_label.pack(side=tk.LEFT, expand=True, pady=10)

        # -------------------- Domstick Image --------------------
        img = Image.open("Resources\\DomStick.png")
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        self.domstick_img = ImageTk.PhotoImage(img)

        img_label = tk.Label(self.main_frame, image=self.domstick_img, bg="white")
        img_label.pack(pady=25)

        # -------------------- Port Selection + Connect --------------------
        port_frame = tk.Frame(self.main_frame, bg="white")
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
        self.status_label = tk.Label(self.main_frame, text="", bg="white", fg="#0078D7", font=("Segoe UI", 12, "bold"))
        self.status_label.pack(side=tk.BOTTOM, pady=25)
        self.refresh_ports()

    def show_main_page(self):
        """Show the main application page"""
        self.config_page.hide()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def show_configuration(self):
        """Show the configuration page"""
        self.main_frame.pack_forget()
        self.config_page.show()

    # -------------------- Functions --------------------
    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports() if "Bluetooth" in port.description]
        self.port_menu["values"] = ports
        if ports:
            self.port_menu.current(0)
            self.status_label.config(text="Choose a port to connect", fg="#0078D7")
        else:
            self.status_label.config(text="Is your Bluetooth open ?", fg="#FF6B6B")
            self.port_menu.set("")  # clearing the combo box menu

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
            # time.sleep(1)  # slight delay for visual effect
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