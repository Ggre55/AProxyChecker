import requests
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor
import time
import os

console = Console()
proxies = []

def check_reliability(proxy, website):
    reliability = 0
    for i in range(5):
        try:
            r = requests.get(website, proxies={"http": proxy, "https": proxy}, timeout=5)
            if r.status_code == 200:
                reliability += 1
                
        except Exception as e:
            print(e)
            continue
    return reliability / 5

    
def check_proxy(site, proxy, alPr, file):
    try:
        
        start = time.time()
        r = requests.get(
                site,
                proxies={
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}",
                },
            )
        end = time.time()
        if r.status_code == 200:
            if proxy not in alPr:
                file.write(proxy + "\n")
            reliability = check_reliability(proxy, site)
            console.print(f"[bold green]-----------:[Success] Proxy {proxy} is working. Latency: {(end - start)}seconds. reliability: {reliability}/5[/bold green]")

        else:
            console.print(f"[bold ]-----------:[Error] Proxy {proxy}, is not working.[/bold]")
    except Exception as e:
        console.print(f"[bold ]-----------:[Error] Proxy {proxy} is not working.[/bold]")


def chk_proxy(site):
    alPr = []
    with open("valid.txt", "r+") as f:
        alPr = f.readlines()
    f.close()
    file_name = "proxies.txt"
    file_path = os.path.join(file_name)
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            proxies.extend([proxy.strip() for proxy in f.readlines()])
    else:
        print(f"Error: The file {file_path} does not exist.")
    console.print(f"[bold ]-----------:Found '{len(proxies)}' Proxies.[/bold]")
    console.print(f"[bold ]-----------:Cheking '{len(proxies)}' Proxies.[/bold]")
    file = open("valid.txt", "a+")
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = [executor.submit(check_proxy, site, proxy, alPr, file) for proxy in proxies]



it = input("Entre Valid URL :$")
chk_proxy(it)

