from cryptography.fernet import Fernet
from django.conf import settings
import os

class EncryptionManager:
    @staticmethod
    def encrypt_file(*, input_file: str):
        encryption_key = Fernet.generate_key()
        f = Fernet(encryption_key)
        encrypted_data = f.encrypt(input_file.read())

        input_file.seek(0)
        input_file.write(encrypted_data)

        return input_file, encryption_key.decode()


    @staticmethod
    def decrypt_file(*,
            input_file: str,
            encryption_key: str,
            http_origin: str):
        f = Fernet(encryption_key)
        decrypted_data = f.decrypt(input_file.read())
        input_file.close()

        curr_path = 'media/'
        # Create the necessary directories in the input file's name attribute.
        for folder_name in ['decrypted'] + input_file.name.split('/')[:-1]:
            curr_path += folder_name + '/'
            if not os.path.exists(settings.BASE_DIR / curr_path):
                os.mkdir(settings.BASE_DIR / curr_path)

        decrypted_file_path = settings.BASE_DIR / f'media/decrypted/{input_file.name}'
        decrypted_file_url = http_origin + os.path.join(settings.MEDIA_URL, f'decrypted/{input_file.name}')

        file = open(decrypted_file_path, 'wb+')
        file.write(decrypted_data)
        file.close()

        return decrypted_file_url, decrypted_file_path, decrypted_data