from functions import get_credentials, start_browser, access_colaborador, search_tickets, display_results, get_search_interval, check_and_install_packages, print_art
from utils import clear_console
import time

def main():

    clear_console()
    print_art()
    check_and_install_packages()

    clear_console()
    print_art()
    username, password = get_credentials()
    
    search_interval_min, search_interval_sec = get_search_interval()
    
    clear_console()
    print_art()
    systems_to_search = ["TRAMITE 5.00", "ALMOX 5.00", "SCF 5.00", "STP 5.00", "SCP 5.00"]
    print("Buscando pelos sistemas: ", ' - '.join(systems_to_search))

    try:
        while True:
            browser = start_browser()
            access_colaborador(browser, username, password)
            found_contents = search_tickets(browser, systems_to_search)
            display_results(found_contents)
            print(f"Aguardando {search_interval_min} minutos para a próxima busca...")
            print(f"Pressione 'Ctrl + C' para finalizar o programa ")
            time.sleep(search_interval_sec)

            # Limpa o vetor para sempre aparecer os mesmos dados
            found_contents.clear()
    except KeyboardInterrupt:
        print("Parando o programa.")
    finally:
        browser.quit()

main()