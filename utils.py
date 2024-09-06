import os
import platform
import subprocess
import sys
import importlib.util

def is_package_installed(package_name):
    """Verifica se um pacote está instalado."""
    package_spec = importlib.util.find_spec(package_name)
    return package_spec is not None

def check_and_install_packages():
    # Lê o arquivo requirements.txt
    with open("requirements.txt", "r") as file:
        required = file.read().splitlines()

    # Lista pacotes que não estão instalados
    missing = []
    for package in required:
        package_name = package.split('==')[0]  # Para pegar apenas o nome do pacote, ignorando a versão
        if not is_package_installed(package_name):
            missing.append(package_name)

    if missing:
        print(f"Os seguintes pacotes estão ausentes e serão instalados: {missing}")
        try:
            # Executa o comando pip install para instalar os pacotes ausentes
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("\nPacotes instalados com sucesso!")
            input("Pressione ENTER para continuar...")
        except subprocess.CalledProcessError as e:
            print(f"Ocorreu um erro durante a instalação dos pacotes: {e}")
            input("Pressione ENTER para continuar...")
            sys.exit(1)  # Encerra o programa em caso de erro
    else:
        print("Todos os pacotes já estão instalados.")

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Para Linux e macOS
        os.system('clear')

def print_art():
       print("""
       _                               _                    _           _     _ 
      | |                             | |                  | |         | |   | |
   ___| |__   __ _ _ __ ___   __ _  __| | ___  ___     __ _| | ___ _ __| |_  | |
  / __| '_ \ / _` | '_ ` _ \ / _` |/ _` |/ _ \/ __|   / _` | |/ _ \ '__| __| | |
 | (__| | | | (_| | | | | | | (_| | (_| | (_) \__ \  | (_| | |  __/ |  | |_  |_|
  \___|_| |_|\__,_|_| |_| |_|\__,_|\__,_|\___/|___/   \__,_|_|\___|_|   \__| (_)
                                                                                                                                                                                                                                        
    """)