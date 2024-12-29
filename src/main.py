import sys
import secrets
import string
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QSpinBox,
)


class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the User Interface"""
        self.setWindowTitle("Random Password Generator")
        self.setGeometry(200, 200, 400, 400)  # Adjusted window size

        layout = QVBoxLayout()

        self.label = QLabel("Generated Password:")
        layout.addWidget(self.label)

        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        layout.addWidget(self.password_field)

        self.length_label = QLabel("Password Length:")
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(8, 64)
        self.length_spinbox.setValue(12)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_spinbox)

        # Adding checkboxes for user selection
        self.include_numbers = QCheckBox("Include Numbers")
        self.include_lowercase = QCheckBox("Include Lowercase Characters")
        self.include_uppercase = QCheckBox("Include Uppercase Characters")
        self.include_symbols = QCheckBox("Include Symbols")
        self.include_special_characters = QCheckBox("Include Special Characters")
        self.no_similar = QCheckBox("No Similar Characters")
        self.no_duplicates = QCheckBox("No Duplicate Characters")
        self.no_sequential = QCheckBox("No Sequential Characters")
        self.begin_with_letter = QCheckBox("Begin With A Letter")

        # Add checkboxes to the layout
        layout.addWidget(self.include_numbers)
        layout.addWidget(self.include_lowercase)
        layout.addWidget(self.include_uppercase)
        layout.addWidget(self.include_symbols)
        layout.addWidget(self.include_special_characters)
        layout.addWidget(self.no_similar)
        layout.addWidget(self.no_duplicates)
        layout.addWidget(self.no_sequential)
        layout.addWidget(self.begin_with_letter)

        # Generate button
        self.generate_button = QPushButton("Generate Password")
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)

        # Set layout to the window
        self.setLayout(layout)

    def generate_password(self):
        """Generate a secure password based on user preferences"""
        length = self.length_spinbox.value()

        # Create character set based on user selections
        characters = self.create_character_set()

        # If no characters are selected, display an error message
        if not characters:
            self.password_field.setText("Please select at least one option.")
            return

        # If "Begin With A Letter" is selected, restrict the first character to letters
        if self.begin_with_letter.isChecked():
            characters = string.ascii_letters

        # Generate a secure password based on selected options
        password = self.generate_secure_password(length, characters)

        # Display the generated password
        self.password_field.setText(password)

    def create_character_set(self):
        """Create the character set based on selected options"""
        characters = ""

        # Include numbers if selected
        if self.include_numbers.isChecked():
            characters += string.digits
        # Include lowercase letters if selected
        if self.include_lowercase.isChecked():
            characters += string.ascii_lowercase
        # Include uppercase letters if selected
        if self.include_uppercase.isChecked():
            characters += string.ascii_uppercase
        # Include symbols if selected
        if self.include_symbols.isChecked():
            characters += string.punctuation
        # Include special characters if selected
        if self.include_special_characters.isChecked():
            special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
            characters += special_characters

        return characters

    def generate_secure_password(self, length, characters):
        """Generate a password while ensuring no duplicates, sequential, or similar characters"""
        password = ""

        while len(password) < length:
            char = secrets.choice(characters)

            # Ensure no duplicates if option is selected
            if self.no_duplicates.isChecked() and char in password:
                continue

            # Ensure no sequential characters if option is selected
            if (
                self.no_sequential.isChecked()
                and len(password) > 1
                and abs(ord(password[-1]) - ord(char)) == 1
            ):
                continue

            # Ensure no similar characters if option is selected
            if self.no_similar.isChecked() and char in "il1Lo0O":
                continue

            # Append the valid character to the password
            password += char

        return password


if __name__ == "__main__":
    # Create the application and window
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()

    # Run the application
    sys.exit(app.exec_())