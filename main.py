from utils import clear_console, print_art
from functions import start_browser, access_colaborador, search_tickets, display_results, config_menu, print_log_message, verify_first_credentials
import time 



def main():

    clear_console()
    print_art()

    username, password = verify_first_credentials()

    search_interval_min, search_interval_sec, print_log = config_menu()
    
    clear_console()
    print_art()
    print("Buscando chamados")
    print(f"Pressione 'Ctrl + C' para finalizar o programa a qualquer momento")

    try:
        while True:
            browser = start_browser(print_log)
            access_colaborador(browser, username, password, print_log)
            tickets_exist = search_tickets(browser, print_log)
            display_results(tickets_exist)
            message_next_search = f"[LOG] Aguardando {search_interval_min} minutos para a próxima busca..."
            print_log_message(print_log, message_next_search)
            time.sleep(search_interval_sec)

    except KeyboardInterrupt:
        print("Parando o programa.")
    finally:
        browser.quit()

main()