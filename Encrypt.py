import sys  # Importing system-specific functions and parameters
import cv2  # Importing OpenCV for image processing
import numpy as np  # Importing NumPy for numerical operations
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,QLineEdit, QMessageBox)  # Importing GUI components from PyQt6

# Default input and output paths for the image
image_path = r"C:\Users\vamsh\Downloads\encryptedImage.png"  # Path to the image to be encrypted
output_path = r"C:\Users\vamsh\Downloads\AICTE_Encryption_Decryption_Project-main\AICTE_Encryption_Decryption_Project-main\encryptedImage.png"  # Path to save the encrypted image

# Creating a GUI class for the encryption application
class EncryptGUI(QWidget):
    def __init__(self):
        super().__init__()  # Calling the constructor of QWidget

        self.setWindowTitle("Image Encryption")  # Setting the window title
        self.setGeometry(100, 100, 400, 300)  # Setting the window size and 
 
        layout = QVBoxLayout()  # Creating a vertical layout for widgets

        self.label = QLabel("Enter secret message:")  # Label for the secret message input field
        layout.addWidget(self.label)  # Adding label to the layout

        self.message_input = QLineEdit(self)  # Creating an input field for the secret message
        layout.addWidget(self.message_input)  # Adding the input field to the layout

        self.label2 = QLabel("Enter passcode:")  # Label for the password input field
        layout.addWidget(self.label2)  # Adding the label to the layout

        self.password_input = QLineEdit(self)  # Creating an input field for the password
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hiding password input for security
        layout.addWidget(self.password_input)  # Adding the input field to the layout

        self.encrypt_button = QPushButton("Encrypt Image", self)  # Creating an encryption button
        self.encrypt_button.clicked.connect(self.encrypt_image)  # Connecting button click to encryption function
        layout.addWidget(self.encrypt_button)  # Adding the button to the layout

        self.setLayout(layout)  # Setting the layout for the window

    def encrypt_image(self):
        """
        This function encrypts the given message and password into an image.
        """
        message = self.message_input.text()  # Getting the user-inputted message
        password = self.password_input.text()  # Getting the user-inputted password

        # Checking if the message or password is empty
        if not message or not password:
            QMessageBox.warning(self, "Error", "Message and password cannot be empty!")  # Display error message
            return  # Exit the function

        img = cv2.imread(image_path)  # Reading the image from the specified path
        if img is None:  # Checking if the image was successfully loaded
            QMessageBox.warning(self, "Error", "Image not found or cannot be read.")  # Display error if image is missing
            return  # Exit the function

        n, m, z = 0, 0, 0  # Initial pixel positions (row, column, color channel)

        # Storing password and message length in the image pixels
        img[n, m, z] = np.uint8(len(password))  # Storing password length in the first pixel
        img[n + 1, m + 1, (z + 1) % 3] = np.uint8(len(message))  # Storing message length in the second pixel
        n += 2  # Moving to the next pixel for data storage
        m += 2
        z = (z + 2) % 3  # Switching to another color channel

        # Encrypting password and message into the image pixel values
        for char in password + message:  
            img[n, m, z] = np.uint8(ord(char))  
            n += 1  
            m += 1  
            z = (z + 1) % 3  

        cv2.imwrite(output_path, img)  # Saving the modified image 
        QMessageBox.information(self, "Success", f"Message encrypted successfully!\nSaved at: {output_path}")  # To the display success message

# Running the GUI application
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Creating an instance of the PyQt application
    window = EncryptGUI()  # Creating an instance of the GUI window
    window.show()  # To Displaying the window
    sys.exit(app.exec())  # To running the application event loop
