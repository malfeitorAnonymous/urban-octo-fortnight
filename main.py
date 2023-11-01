import os
import zipfile
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def encrypt_file(key, file_path, encrypted_path):
    cipher = AES.new(key, AES.MODE_EAX)
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    with open(encrypted_path, 'wb') as file_encrypted:
        for x in (cipher.nonce, ciphertext, tag):
            file_encrypted.write(x)

def main():
    folder_path = input("Digite o caminho da pasta que deseja criptografar: ")
    zip_path = folder_path + ".zip"
    encrypted_path = folder_path + ".enc"

    # Passo 1: Compactar a pasta
    zip_folder(folder_path, zip_path)
    
    # Passo 2: Criptografar o arquivo ZIP asd
    key = get_random_bytes(16)  # AES key, 16 bytes for AES-128
    encrypt_file(key, zip_path, encrypted_path)
    
    # Limpando (removendo o arquivo ZIP original após criptografá-lo)
    os.remove(zip_path)
    
    print(f"Pasta {folder_path} criptografada com sucesso em {encrypted_path}")
    print(f"Chave de criptografia (guarde-a com segurança!): {key.hex()}")

if __name__ == "__main__":
    main()



