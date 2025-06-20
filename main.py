import requests
import random
import string
import time
import threading
from datetime import datetime
import concurrent.futures

COLOR_MAIN = "\033[38;2;247;133;255m"   
COLOR_DIM = "\033[38;2;180;100;190m"  
COLOR_RESET = "\033[0m"

COLOR_RED = "\033[38;2;255;100;100m"
COLOR_GREEN = "\033[38;2;150;255;150m"
COLOR_YELLOW = "\033[38;2;255;255;150m"

banner = f"""{COLOR_MAIN}
╔╗╔╔═╗╦╔═╔═╗ ╔═╗╦═╗╔═╗
║║║║╣ ╠╩╗║ ║ ║╣ ╠╦╝╠═╣
╝╚╝╚═╝╩ ╩╚═╝o╚═╝╩╚═╩ ╩
{COLOR_RESET}"""


print(banner)
print("PAY TO WIN NIGGA")
time.sleep(3)

def get_now():
    return datetime.now().strftime("%H:%M:%S")

def random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def gen_threaded(count, length=8, filename="usernames.txt", max_threads=30):
    usernames = []

    def gen_partial(n):
        return [random_string(length) for _ in range(n)]

    counts = [count // max_threads] * max_threads
    for i in range(count % max_threads):
        counts[i] += 1

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = list(executor.map(gen_partial, counts))

    for result in results:
        usernames.extend(result)

    for name in usernames:
        print(f"{COLOR_DIM}{get_now()} | {COLOR_MAIN}[+]{COLOR_RESET} Generated | {COLOR_MAIN}{name}{COLOR_RESET}")

    with open(filename, "w") as f:
        f.write('\n'.join(usernames))

    print(f"{COLOR_DIM}{get_now()} | {COLOR_MAIN}Done! | {filename}{COLOR_RESET}")

def check_username(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            print(f"{COLOR_DIM}{get_now()} | {COLOR_RED}[-]{COLOR_RESET} TAKEN: {COLOR_MAIN}{username}{COLOR_RESET}")
        elif response.status_code in [204, 404]:
            print(f"{COLOR_DIM}{get_now()} | {COLOR_GREEN}[+]{COLOR_RESET} AVAILABLE: {COLOR_MAIN}{username}{COLOR_RESET}")
            with open("valid.txt", "a") as valid_file:
                valid_file.write(username + "\n")
    except requests.exceptions.RequestException:
        print(f"{COLOR_DIM}{get_now()} | {COLOR_YELLOW}[!]{COLOR_RESET} ERROR: {COLOR_MAIN}{username}{COLOR_RESET}")

    time.sleep(1)

def check_usernames_threaded(usernames, max_threads=3):
    threads = []

    for username in usernames:
        thread = threading.Thread(target=check_username, args=(username,))
        threads.append(thread)
        thread.start()

        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

def main():
    gen_threaded(count=100000, length=3, max_threads=100)

    try:
        with open("usernames.txt", "r") as file:
            usernames = file.read().splitlines()

        print(f"{COLOR_DIM}{get_now()} | {COLOR_GREEN}[+]{COLOR_RESET} Started Search | {COLOR_MAIN}GOOD LUCK :) {COLOR_RESET}")
        check_usernames_threaded(usernames, max_threads=30)
        print(f"{COLOR_DIM}{get_now()} | {COLOR_GREEN}[+]{COLOR_RESET} {COLOR_MAIN}GOOD LUCKS :D Check it valid.txt |{COLOR_RESET}")

    except FileNotFoundError:
        print(f"{COLOR_RED}ERROR: usernames.txt not found!{COLOR_RESET}")

if __name__ == "__main__":
    main()
