import os
import platform

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Para Linux e macOS
        os.system('clear')