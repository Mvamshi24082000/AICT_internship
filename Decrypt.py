import sys  
import cv2  
import os  
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox)  

# Encrypted image path (change this path according to your system)
Image_path = r"C:\Users\vamsh\Downloads\AICTE_Encryption_Decryption_Project-main\AICTE_Encryption_Decryption_Project-main\encryptedImage.png"

# Creating a GUI class for the decryption application
class DecryptGUI(QWidget):
    def __init__(self):
        super().__init__()  # Calling the constructor of the QWidget class

        self.setWindowTitle("Image Decryption")  #  window title
        self.setGeometry(100, 100, 400, 200)  #  window size and position

        layout = QVBoxLayout()  
        self.label = QLabel("Enter passcode for decryption:")  #  label for the password input
        layout.addWidget(self.label)  # Adding the label to the layout

        self.password_input = QLineEdit(self)  #   text input field for the password
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hiding the input text for password
        layout.addWidget(self.password_input)  # Adding the password input

        self.Decrypt_button = QPushButton("Decrypt Image", self) 
        self.Decrypt_button.clicked.connect(self.Decrypt_image)  
        layout.addWidget(self.Decrypt_button) 
        self.setLayout(layout)  # Setting the layout for the window

    def extract_hidden_data(self, img):
        """
        This function extracts the hidden password and message from the encrypted image.
        The message is stored in the pixel values of the image.
        """
        n, m, z = 0, 0, 0  # Initial pixel position
        password_length = int(img[n, m, z])  # Extracting the password length from the first pixel
        message_length = int(img[n + 1, m + 1, (z + 1) % 3])  # Extracting the message length from the second pixel
        n += 2  # Moving to the next pixel for password extraction
        m += 2
        z = (z + 2) % 3  # Moving to the next color channel

        # Extracting the password from the image pixel values
        extracted_password = "".join(chr(int(img[n + i, m + i, (z + i) % 3])) for i in range(password_length))
        n += password_length  # Moving to the next pixel for message extraction
        m += password_length
        z = (z + password_length) % 3  # Updating the color channel index

        # Extracting the secret message from the image pixel values
        message = "".join(chr(int(img[n + i, m + i, (z + i) % 3])) for i in range(message_length))
        return extracted_password, message  # Returning extracted password and message

    def Decrypt_image(self):
        """
        This function reads the encrypted image, extracts the hidden password and message,
        and verifies the entered password.
        """
        password_attempt = self.password_input.text()  
        if not password_attempt:  
            QMessageBox.warning(self, "Error", "Please enter the password to decrypt Message!")
            return  # Exiting function if no password is entered

        img = cv2.imread(Image_path)  # Reading the encrypted image
        if img is None:  # Checking if the image was loadeding successfully
            QMessageBox.warning(self, "Error", "Encrypted image not found.")  # Display error if image not found
            return

        extracted_password, message = self.extract_hidden_data(img)  
        print(f"Extracted Password: {extracted_password}")  
        if extracted_password != password_attempt:  
            QMessageBox.warning(self, "Error", "Incorrect password! Access denied.")  # It will Display error for wrong password
            return
        
        # Displaying the decrypted message if the password is correct
        QMessageBox.information(self, "Decryption Successful", f"Secret Message: {message}")

# Running the GUI application
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Creating an instance of the PyQt application
    window = DecryptGUI()  # To Creating an instance of the GUI window
    window.show()  # To  Displaying the window 
    sys.exit(app.exec())  #  To running the application 
