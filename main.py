from utils import clear_console, print_art
from functions import get_credentials, start_browser, access_colaborador, search_tickets, display_results, config_menu, print_log_message
from datetime import datetime
import time 


def main():

    clear_console()
    print_art()
    username, password = get_credentials()

    search_interval_min, search_interval_sec, systems_to_search, print_log = config_menu()
    
    clear_console()
    print_art()
    print("Buscando pelos sistemas: ", ' - '.join(systems_to_search))
    print(f"Pressione 'Ctrl + C' para finalizar o programa a qualquer momento")

    try:
        while True:
            browser = start_browser(print_log)
            access_colaborador(browser, username, password, print_log)
            found_contents = search_tickets(browser, systems_to_search, print_log)
            display_results(found_contents)
            
            message_next_search = f"[LOG] Aguardando {search_interval_min} minutos para a próxima busca..."
            print_log_message(print_log, message_next_search)
            time.sleep(search_interval_sec)

            # Limpa o vetor para sempre aparecer os mesmos dados
            found_contents.clear()
    except KeyboardInterrupt:
        print("Parando o programa.")
    finally:
        browser.quit()

main()