# Automation Prj: This project will allow you to connect to two virtual machines using SSH, generate a new SSH key pair for the first virtual machine, save the SSH key pair for the first virtual machine to a file, connect to the first virtual machine using SSH, upload the SSH public key for the first virtual machine to the second virtual machine, disconnect from the first virtual machine, connect to the second virtual machine using SSH, and run a script on the second virtual machine.

import paramiko
import OpenSSL


def connect_to_server(hostname, username, password):
    # Connects to a remote server using SSH.
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client


def generate_key_pair():
    # Generates a new SSH key pair.
    private_key = OpenSSL.crypto.PKey()
    private_key.generate_key(2048)
    public_key = private_key.public_key()
    return private_key, public_key


def save_key_pair(private_key, public_key, filename):
    # Saves the SSH key pair to a file.
    with open(filename, "wb") as f:
        f.write(private_key.save_pkcs1())
        f.write(public_key.save_pem())


def main():
    # The main function.
    hostname1 = input("Enter the hostname: ")
    username1 = input("Enter the username: ")
    password1 = input("Enter the password: ")

    hostname2 = "localhost"
    username2 = "username2"
    password2 = "password2"

    # Generate a new SSH key pair for the first virtual machine.
    private_key1, public_key1 = generate_key_pair()

    # Save the SSH key pair for the first virtual machine to a file.
    save_key_pair(private_key1, public_key1, "id_rsa1")

    # Connect to the first virtual machine using SSH.
    client1 = connect_to_server(hostname1, username1, password1)

    # Upload the SSH public key for the first virtual machine to the second virtual machine.
    client1.exec_command("cat id_rsa1.pub >> .ssh/authorized_keys")

    # Disconnect from the first virtual machine.
    client1.close()

    # Connect to the second virtual machine using SSH.
    client2 = connect_to_server(hostname2, username2, password2)

    # Run a script on the second virtual machine.
    client2.exec_command("python script.py")

    # Disconnect from the second virtual machine.
    client2.close()


if __name__ == "__main__":
    main()
