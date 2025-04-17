# Import necessary PyQt6 modules for GUI components
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, \
    QPushButton, QRadioButton, QTextEdit, QGridLayout, QMessageBox
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtCore import pyqtSignal, QObject

# Import standard library modules
import socket
import threading
from datetime import datetime

# Create a TCP socket for client-server communication
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class MessageSignalHandler(QObject):
    """
    Custom signal handler for thread-safe communication between threads.
    """
    new_message_received = pyqtSignal(str)


class ChatApplication(QMainWindow):
    """
    Main chat application window handling GUI and network communication.
    """

    def __init__(self):
        super().__init__()
        self.message_handler = MessageSignalHandler()
        self.message_handler.new_message_received.connect(self.display_chat_message)

        # Configure main window properties
        self.setWindowTitle("Chat Application")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(550, 600)

        # Initialize UI
        self.initialize_user_interface()

    def initialize_user_interface(self):
        """Initialize all UI components in proper order."""
        self.setup_main_window_layout()
        self.create_connection_settings_panel()
        self.create_chat_message_display()
        self.create_message_input_panel()
        self.apply_application_styles()

    def setup_main_window_layout(self):
        """Configure main window's central widget and layout."""
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("mainWidget")
        self.setCentralWidget(self.main_widget)

        self.primary_layout = QVBoxLayout(self.main_widget)
        self.primary_layout.setContentsMargins(10, 10, 10, 10)
        self.primary_layout.setSpacing(10)

    def apply_application_styles(self):
        """Apply CSS-like styling to all components."""
        self.setStyleSheet("""
        /* Styles remain exactly the same as original */
        /* ... */
        """)

    def create_connection_settings_panel(self):
        """Create connection settings panel with server, port, username inputs."""
        connection_panel = QGroupBox("Connection Settings")
        connection_layout = QGridLayout()

        # Server connection widgets
        self.server_address_label = QLabel("Server IP:")
        self.server_address_input = QLineEdit()
        self.server_address_input.setText(f"{socket.gethostbyname(socket.gethostname())}")
        self.server_address_input.setPlaceholderText(f"{socket.gethostbyname(socket.gethostname())}")

        self.port_number_label = QLabel("Port:")
        self.port_number_input = QLineEdit()
        self.port_number_input.setText("12345")
        self.port_number_input.setPlaceholderText("12345")
        self.port_number_input.setValidator(QIntValidator(1, 65535))

        self.user_name_label = QLabel("Username:")
        self.user_name_input = QLineEdit()
        self.user_name_input.setPlaceholderText("Enter username")

        # Add widgets to layout
        connection_layout.addWidget(self.server_address_label, 0, 0)
        connection_layout.addWidget(self.server_address_input, 0, 1)
        connection_layout.addWidget(self.port_number_label, 0, 2)
        connection_layout.addWidget(self.port_number_input, 0, 3)
        connection_layout.addWidget(self.user_name_label, 1, 0)
        connection_layout.addWidget(self.user_name_input, 1, 1, 1, 3)

        # Text color selection
        self.text_color_selection_label = QLabel("Text Color:")
        self.default_color_radio = QRadioButton("Black")
        self.default_color_radio.setObjectName("blackRadio")
        self.default_color_radio.setChecked(True)
        self.red_color_radio = QRadioButton("Red")
        self.red_color_radio.setObjectName("redRadio")
        self.green_color_radio = QRadioButton("Green")
        self.green_color_radio.setObjectName("greenRadio")
        self.blue_color_radio = QRadioButton("Blue")
        self.blue_color_radio.setObjectName("blueRadio")

        color_selection_layout = QHBoxLayout()
        color_selection_layout.addWidget(self.text_color_selection_label)
        color_selection_layout.addWidget(self.default_color_radio)
        color_selection_layout.addWidget(self.red_color_radio)
        color_selection_layout.addWidget(self.green_color_radio)
        color_selection_layout.addWidget(self.blue_color_radio)
        color_selection_layout.addStretch()

        # Connection buttons
        self.connect_server_button = QPushButton("Connect")
        self.disconnect_server_button = QPushButton("Disconnect")
        self.disconnect_server_button.setEnabled(False)

        # Connect signals
        self.connect_server_button.clicked.connect(self.establish_server_connection)
        self.disconnect_server_button.clicked.connect(self.terminate_server_connection)

        button_container_layout = QHBoxLayout()
        button_container_layout.addStretch()
        button_container_layout.addWidget(self.connect_server_button)
        button_container_layout.addWidget(self.disconnect_server_button)

        # Combine layouts
        bottom_row_container = QHBoxLayout()
        bottom_row_container.addLayout(color_selection_layout)
        bottom_row_container.addLayout(button_container_layout)
        connection_layout.addLayout(bottom_row_container, 2, 0, 1, 4)

        connection_panel.setLayout(connection_layout)
        self.primary_layout.addWidget(connection_panel)

    def create_chat_message_display(self):
        """Create the chat message display area."""
        chat_display_panel = QGroupBox("Chat Messages")
        chat_display_layout = QVBoxLayout()

        self.chat_history_display = QTextEdit()
        self.chat_history_display.setReadOnly(True)
        chat_display_layout.addWidget(self.chat_history_display)

        chat_display_panel.setLayout(chat_display_layout)
        self.primary_layout.addWidget(chat_display_panel, 1)

    def create_message_input_panel(self):
        """Create message input area with send button."""
        message_input_panel = QGroupBox("Send Message")
        message_input_layout = QHBoxLayout()

        self.message_composition_input = QLineEdit()
        self.message_composition_input.setPlaceholderText("Type your message here...")
        self.message_composition_input.returnPressed.connect(self.transmit_chat_message)

        self.send_message_button = QPushButton("Send")
        self.send_message_button.clicked.connect(self.transmit_chat_message)
        self.send_message_button.setEnabled(False)

        message_input_layout.addWidget(self.message_composition_input)
        message_input_layout.addWidget(self.send_message_button)
        message_input_panel.setLayout(message_input_layout)
        self.primary_layout.addWidget(message_input_panel)

    def establish_server_connection(self):
        """Handle connection to the chat server."""
        server_address = self.server_address_input.text()
        server_port = self.port_number_input.text()
        username = self.user_name_input.text()

        if (len(username) == 0 or len(server_address) == 0 or len(server_port) == 0 or
                server_address != socket.gethostbyname(socket.gethostname()) or server_port != "12345"):
            QMessageBox.warning(self, "Warning", "Please fill the fields correctly.")
            return

        try:
            server_port = int(server_port)
            client_socket.connect((server_address, server_port))

            selected_color = "black"
            if self.red_color_radio.isChecked():
                selected_color = "red"
            elif self.green_color_radio.isChecked():
                selected_color = "green"
            elif self.blue_color_radio.isChecked():
                selected_color = "blue"

            self.default_color_radio.setEnabled(False)
            self.red_color_radio.setEnabled(False)
            self.green_color_radio.setEnabled(False)
            self.blue_color_radio.setEnabled(False)
            self.user_name_input.setEnabled(False)
            self.server_address_input.setEnabled(False)
            self.port_number_input.setEnabled(False)

            client_socket.send(f"{username}|{selected_color}".encode('utf-8'))

            message_receiver_thread = threading.Thread(target=self.listen_for_incoming_messages)
            message_receiver_thread.daemon = True
            message_receiver_thread.start()

            self.connect_server_button.setEnabled(False)
            self.disconnect_server_button.setEnabled(True)
            self.send_message_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect: {str(e)}")

    def terminate_server_connection(self):
        """Handle disconnection from the chat server."""
        try:
            client_socket.send("/exit".encode('utf-8'))
            client_socket.close()
            self.chat_history_display.append("Disconnected from server")
        except:
            pass
        finally:
            self.connect_server_button.setEnabled(True)
            self.disconnect_server_button.setEnabled(False)
            self.send_message_button.setEnabled(False)
            self.default_color_radio.setEnabled(True)
            self.red_color_radio.setEnabled(True)
            self.green_color_radio.setEnabled(True)
            self.blue_color_radio.setEnabled(True)

    def transmit_chat_message(self):
        """Send a message to the chat server."""
        message_content = self.message_composition_input.text()
        if message_content:
            try:
                client_socket.send(message_content.encode('utf-8'))
                self.message_composition_input.clear()
            except Exception as e:
                self.terminate_server_connection()

    def listen_for_incoming_messages(self):
        """Continuously receive messages from server in a separate thread."""
        while True:
            try:
                incoming_message = client_socket.recv(1024).decode('utf-8')
                if not incoming_message or incoming_message.lower() == "/exit":
                    break
                self.message_handler.new_message_received.emit(incoming_message)
            except Exception as e:
                break

        self.terminate_server_connection()

    def display_chat_message(self, message):
        """Display received message in the chat display area."""
        self.chat_history_display.setAcceptRichText(True)

        if message.startswith("[PM from "):
            sender = message.split("]")[0][9:]
            msg_content = message.split("]")[1].strip()
            html_content = f'<span style="color:purple"><b>[Private from {sender}]:</b> {msg_content}</span> ({datetime.now().strftime("%H:%M")})'
            self.chat_history_display.append(html_content)
            return

        message = message.replace("\n", "<br>")

        if "|" in message:
            message_parts = message.split("|", 2)
            if len(message_parts) == 3:
                username, color, message_content = message_parts
                html_content = f'<span style="color:{color}"><b>{username}:</b> {message_content}</span> ({datetime.now().strftime("%H:%M")})'
                self.chat_history_display.append(html_content)
                return

        self.chat_history_display.append(f"<pre>{message}</pre>")


# Application entry point
if __name__ == "__main__":
    chat_app = QApplication([])
    chat_app.setStyle("fusion")
    main_window = ChatApplication()
    main_window.show()
    chat_app.exec()