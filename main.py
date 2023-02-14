import requests
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
import time
import os


console = Console()
proxies = []
def check_proxy(site, proxy):
    try:
        
        start = time.time()
        r = requests.get(
                site,
                proxies={
                    "http": f"http://{proxy}",
                    "https": f"https://{proxy}",
                },
            )
        end = time.time()
        if r.status_code == 200:
            console.print(f"[bold green]-----------:[Success] Proxy {proxy} is working. Latency: {end - start}seconds[/bold green]")
            with open("valid.txt", "a+") as f:
                f.write(proxy + "\n")
        else:
            console.print(f"[bold ]-----------:[Error] Proxy {proxy}, is not working. Response code: {r.status_code}[/bold]")
    except Exception as e:
        console.print(f"[bold ]-----------:[Error] Proxy {proxy} is not working.[/bold]")


def chk_proxy(site):
    file_name = "proxies.txt"
    file_path = os.path.join(file_name)
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            proxies.extend([proxy.strip() for proxy in f.readlines()])
    else:
        print(f"Error: The file {file_path} does not exist.")
    console.print(f"[bold ]-----------:Found '{len(proxies)}' Proxies.[/bold]")
    console.print(f"[bold ]-----------:Cheking '{len(proxies)}' Proxies.[/bold]")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = [executor.submit(check_proxy, site, proxy) for proxy in proxies]



it = input("Entre Valid URL :$")
chk_proxy(it)
