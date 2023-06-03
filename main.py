import threading
from icmplib import ping
from webbrowser import open as open_on_browser
from colorama import Fore
from instances import list_of_websites


def validate_input(user_input):
    try:
        website_index = int(user_input)
        if website_index >= 0 and website_index < len(list_of_websites):
            open_on_browser(list_of_websites[website_index])
        else:
            print(Fore.RED, f'input should be in range of 0-{len(list_of_websites)-1}')
    except ValueError:
        print(Fore.RED, 'input should be decimal number like 7')


class Ping:
    def __new__(cls):
        # singleton design pattern implemented.
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    minimum_ping = 1000

    def get_input(self):
        while True:
            user_input = input()
            validate_input(user_input)

    def get_ping(self):
        print(Fore.CYAN, 'Please Wait.... This will Take some time.')
        print(Fore.CYAN, 'Enter website index to launch on browser')
        input_thread = threading.Thread(target=self.get_input)
        input_thread.start()
        
        for i, website in enumerate(list_of_websites):
            host = ping(website, count=4, interval=1, timeout=2, privileged=True)

            if host.is_alive:
                if host.avg_rtt < self.minimum_ping:
                    self.minimum_ping = host.avg_rtt
                    print(Fore.GREEN, f'{i} {website} is alive! avg_rtt={host.avg_rtt} ms')
                else:
                    print(Fore.WHITE, f'{i} {website} is alive! avg_rtt={host.avg_rtt} ms')
            else:
                print(Fore.RED, f'{i} {website} {host.address} is dead')


if __name__ == '__main__':
    new_ping = Ping()
    new_ping.get_ping()
