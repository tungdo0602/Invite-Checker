import requests
import random
import string
import colorama
from colorama import *
import os
import console
from console.utils import set_title
import time

s = requests.Session()
proxylist = set()
with open("proxies.txt", "r") as f:
  f_line = f.readlines()
  for line in f_line:
    proxylist.add(line.strip())

errmessage = "Unknown Invite"

vaildcode = []

vaild = 0
invaild = 0
checked = 0
rl = 0
badproxy = 0

while True:
  proxy = random.choice(list(proxylist))
  proxy_form = {'http': f"socks4://{proxy}", 'https': f"socks4://{proxy}"}
  set_title(f"Invite Cracker - Vaild: {vaild} | Invaild: {invaild} | Checked: {checked} | Rate Limied: {rl} | Bad Proxy: {badproxy}")
  ic = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
  try:
    respond = s.get(f'https://discordapp.com/api/invite/{ic}', proxies=proxy_form, timeout=3000)
    if respond.status_code != 429:
      check = respond.json()
      ct = respond.status_code
      try:
        if check.get('message') == errmessage:
          print(f"{Fore.RED} [-] {ct} | Invaild Invite Code: {ic}")
          invaild += 1
          checked += 1
      except:
        try:
          if check.get("code") == ic:
            print(f"{Fore.GREEN} [+] {ct} | Vaild Code: {ic}")
            f = open("Result.txt", "a+")
            f.write(f"""
Server Name: {check.get("guild").get("name")}
Server ID: {check.get("guild").get("id")}
Invite code expires_at: {check.get("expires_at")}
Vanity url code: {check.get("guild").get("vanity_url_code")}
Verification level: {check.get("guild").get("verification_level")}

Invite to Channel: 
+ Name: {check.get("guild").get("channel").get("name")}
+ ID: {check.get("guild").get("channel").get("id")}
+ Type: {check.get("guild").get("channel").get("type")}

Inviter:
+ Name: {check.get("guild").get("inviter").get("username")}
+ Discriminator: {check.get("guild").get("inviter").get("discriminator")}
+ Id: {check.get("guild").get("inviter").get("id")}\n
""")
            vaild += 1
            checked += 1
            vaildcode.append(ic)
        except:
          print("Lmao! get error lol")
    else:
      print(f"{Fore.YELLOW} Rate Limited!")
      rl += 1
  except:
    list(proxylist).remove(proxy)
    badproxy += 1