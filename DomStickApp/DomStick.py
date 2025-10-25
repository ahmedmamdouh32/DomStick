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
        # Title with compact styling
        title_frame = tk.Frame(self.frame, bg="white")
        title_frame.pack(fill=tk.X, pady=(15, 5))

        title_label = tk.Label(title_frame, text="Configuration Settings",
                               bg="white", fg=theme_color,
                               font=("Segoe UI", 16, "bold"))
        title_label.pack()

        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Customize your DomStick device settings",
                                  bg="white", fg="#666666",
                                  font=("Segoe UI", 9))
        subtitle_label.pack(pady=(2, 0))

        # Configuration content area - more compact
        content_frame = tk.Frame(self.frame, bg="white", relief="flat", bd=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Main container for both sections
        main_container = tk.Frame(content_frame, bg="#F8F9FA", relief="flat", bd=1)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left side - Joystick Section (more compact)
        joystick_frame = tk.Frame(main_container, bg="white", relief="flat", bd=1,
                                  highlightbackground="#E0E0E0", highlightthickness=1)
        joystick_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=8)

        # Joystick header with accent color
        joystick_header = tk.Frame(joystick_frame, bg=theme_color, height=25)
        joystick_header.pack(fill=tk.X)
        joystick_header.pack_propagate(False)

        tk.Label(joystick_header, text="Joystick Controls",
                 bg=theme_color, fg="white", font=("Segoe UI", 10, "bold")).pack(pady=3)

        # Joystick buttons in a cross layout (more compact)
        joystick_buttons_frame = tk.Frame(joystick_frame, bg="white")
        joystick_buttons_frame.pack(expand=True, pady=12)

        # Top button
        self.joystick_up = tk.Button(joystick_buttons_frame, text="↑",
                                     font=("Consolas", 14, "bold"), width=3, height=1,
                                     bg="#E3F2FD", fg=theme_color, relief="groove",
                                     activebackground="#BBDEFB", activeforeground=theme_color)
        self.joystick_up.grid(row=0, column=1, pady=4)

        # Middle row (Left, Center, Right)
        self.joystick_left = tk.Button(joystick_buttons_frame, text="←",
                                       font=("Consolas", 14, "bold"), width=3, height=1,
                                       bg="#E3F2FD", fg=theme_color, relief="groove",
                                       activebackground="#BBDEFB", activeforeground=theme_color)
        self.joystick_left.grid(row=1, column=0, padx=4)

        # Center push button with accent color
        self.joystick_center = tk.Button(joystick_buttons_frame, text="PUSH",
                                         font=("Consolas", 10, "bold"), width=4, height=2,
                                         bg=theme_color, fg="white", relief="groove",
                                         activebackground="#005A9E", activeforeground="white")
        self.joystick_center.grid(row=1, column=1, padx=2, pady=2)

        self.joystick_right = tk.Button(joystick_buttons_frame, text="→",
                                        font=("Consolas", 14, "bold"), width=3, height=1,
                                        bg="#E3F2FD", fg=theme_color, relief="groove",
                                        activebackground="#BBDEFB", activeforeground=theme_color)
        self.joystick_right.grid(row=1, column=2, padx=4)

        # Bottom button
        self.joystick_down = tk.Button(joystick_buttons_frame, text="↓",
                                       font=("Consolas", 14, "bold"), width=3, height=1,
                                       bg="#E3F2FD", fg=theme_color, relief="groove",
                                       activebackground="#BBDEFB", activeforeground=theme_color)
        self.joystick_down.grid(row=2, column=1, pady=4)

        # Right side - Push Buttons Section (more compact)
        push_buttons_frame = tk.Frame(main_container, bg="white", relief="flat", bd=1,
                                      highlightbackground="#E0E0E0", highlightthickness=1)
        push_buttons_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=8)

        # Push Buttons header with accent color
        push_header = tk.Frame(push_buttons_frame, bg=theme_color, height=25)
        push_header.pack(fill=tk.X)
        push_header.pack_propagate(False)

        tk.Label(push_header, text="Action Buttons",
                 bg=theme_color, fg="white", font=("Segoe UI", 10, "bold")).pack(pady=3)

        # Push buttons container
        buttons_container = tk.Frame(push_buttons_frame, bg="white")
        buttons_container.pack(expand=True, pady=12)

        # Push buttons stacked vertically with compact styling
        button_style = {
            "font": ("Consolas", 12, "bold"),
            "width": 9,
            "height": 1,
            "bg": "#E3F2FD",
            "fg": "#0078D7",
            "relief": "groove",
            "activebackground": "#E0E0E0",
            "activeforeground": "#333333"
        }

        self.push_top = tk.Button(buttons_container, text="TOP", **button_style)
        self.push_top.pack(pady=3)

        self.push_bottom = tk.Button(buttons_container, text="BOTTOM", **button_style)
        self.push_bottom.pack(pady=3)

        self.push_right = tk.Button(buttons_container, text="RIGHT", **button_style)
        self.push_right.pack(pady=3)

        self.push_left = tk.Button(buttons_container, text="LEFT", **button_style)
        self.push_left.pack(pady=3)

        # Serial Settings Section (compact)
        serial_frame = tk.Frame(content_frame, bg="white", relief="flat", bd=1,
                                highlightbackground="#E0E0E0", highlightthickness=1)
        serial_frame.pack(fill=tk.X, pady=(8, 0))

        # Serial settings header
        serial_header = tk.Frame(serial_frame, bg=theme_color, height=28)
        serial_header.pack(fill=tk.X)
        serial_header.pack_propagate(False)

        tk.Label(serial_header, text="Serial Communication Settings",
                 bg=theme_color, fg="white", font=("Segoe UI", 11, "bold")).pack(pady=5)

        # Serial settings in 2x2 grid with compact spacing
        serial_grid = tk.Frame(serial_frame, bg="white")
        serial_grid.pack(pady=12, padx=20)

        # Style for serial labels
        label_style = {"bg": "white", "font": ("Segoe UI", 9), "fg": "#555555"}

        # Row 1
        tk.Label(serial_grid, text="Baud Rate:", **label_style).grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self.baud_combo = ttk.Combobox(serial_grid, values=["9600", "19200", "38400", "57600", "115200"],
                                       state="readonly", width=8, font=("Segoe UI", 8))
        self.baud_combo.set("9600")
        self.baud_combo.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(serial_grid, text="Stop Bits:", **label_style).grid(row=0, column=2, padx=8, pady=4, sticky="w")
        self.stop_bits_combo = ttk.Combobox(serial_grid, values=["1", "2"], state="readonly", width=8,
                                            font=("Segoe UI", 8))
        self.stop_bits_combo.set("1")
        self.stop_bits_combo.grid(row=0, column=3, padx=8, pady=4)

        # Row 2
        tk.Label(serial_grid, text="Data Bits:", **label_style).grid(row=1, column=0, padx=8, pady=4, sticky="w")
        self.data_bits_combo = ttk.Combobox(serial_grid, values=["5", "6", "7", "8"], state="readonly", width=8,
                                            font=("Segoe UI", 8))
        self.data_bits_combo.set("8")
        self.data_bits_combo.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(serial_grid, text="Parity:", **label_style).grid(row=1, column=2, padx=8, pady=4, sticky="w")
        self.parity_combo = ttk.Combobox(serial_grid, values=["None", "Even", "Odd"], state="readonly", width=8,
                                         font=("Segoe UI", 8))
        self.parity_combo.set("None")
        self.parity_combo.grid(row=1, column=3, padx=8, pady=4)

        # Bottom buttons frame - compact
        buttons_frame = tk.Frame(self.frame, bg="white")
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=15)

        # Add a separator line
        separator = tk.Frame(buttons_frame, bg="#E0E0E0", height=1)
        separator.pack(fill=tk.X, pady=(0, 10))

        # Button container for side-by-side layout
        button_container = tk.Frame(buttons_frame, bg="white")
        button_container.pack(fill=tk.X)

        # Back button (left side)
        close_button = tk.Button(button_container, text="← Back", bg="#6C757D", fg="white",
                                 font=("Segoe UI", 9, "bold"), width=10, height=1,
                                 command=self.close_configuration, relief="flat",
                                 activebackground="#5A6268", activeforeground="white")
        close_button.pack(side=tk.LEFT, padx=5)

        # Save button (right side) - with empty function for now
        save_button = tk.Button(button_container, text="Save Settings", bg=theme_color, fg="white",
                                font=("Segoe UI", 9, "bold"), width=12, height=1,
                                relief="flat", activebackground="#005A9E", activeforeground="white",
                                command=self.save_settings)
        save_button.pack(side=tk.RIGHT, padx=5)

    def save_settings(self):
        """Empty function for Save button - to be implemented later"""
        print("Save button clicked - functionality to be implemented")
        # This function doesn't do anything yet, as requested

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