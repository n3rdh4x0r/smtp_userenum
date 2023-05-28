#!/usr/bin/python3

import socket
import sys
import time

ascii_art = 
'''                                                                                          '''
'''                    __                                                                    '''
'''    _________ ___  / /_____      __  __________  ________  ____  __  ______ ___           '''
'''   / ___/ __ `__ \/ __/ __ \    / / / / ___/ _ \/ ___/ _ \/ __ \/ / / / __ `__ \          ''' 
'''  (__  ) / / / / / /_/ /_/ /   / /_/ (__  )  __/ /  /  __/ / / / /_/ / / / / / /          '''
''' /____/_/ /_/ /_/\__/ .___/____\__,_/____/\___/_/   \___/_/ /_/\__,_/_/ /_/ /_/           '''
'''                   /_/   /_____/                                                          '''
'''                                                                                          ''' 
'''                                                                                          '''

def print_welcome():
    print(ascii_art)
    print("\r\nWelcome to the SMTP user enumeration super scan\r\n")
    print("============***c1ph3rm4st3r***=========================")


def enumerate_smtp(ip_address):
    # Path to the users dictionary file
    users_file_path = "/usr/share/metasploit-framework/data/wordlists/unix_users.txt"

    # Open the text file in Read mode and start enumerating
    try:
        with open(users_file_path, 'r') as users_file:
            for user in users_file:
                # Clean up the user value
                user = user.strip()

                # Do not process an empty user value
                if not user:
                    continue

                try:
                    # Create a Socket object
                    sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # Connect to the SMTP Server
                    sok.connect((ip_address, 25))
                    # Receive the banner from the server first
                    sok.recv(1024)
                    # Verify if the user exists on the server using the VRFY command
                    sok.send(b'VRFY ' + user.encode() + b'\r\n')
                    # Sleep for 1 second to avoid flooding the server
                    time.sleep(1)
                    # Get the response from the server
                    results = sok.recv(1024)
                    if b"rejected" not in results:
                        print("%s : Found" % user)
                except Exception as e:
                    print("An error occurred:", str(e))
                finally:
                    # Close the connection socket
                    sok.close()
    except Exception as e:
        print("An error occurred while reading the users file:", str(e))

    # Let the user know that we finished
    print("\r\nThe program has finished enumerating users.\r\n")


def print_usage():
    print("Usage: python script_name.py <IP_ADDRESS>")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_usage()
        sys.exit(0)
    print_welcome()
    enumerate_smtp(sys.argv[1])


if __name__ == '__main__':
    main()
