import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token, url):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": url}
    
    response = requests.post("https://api-ssl.bitly.com/v4/bitlinks", json=payload, headers=headers)
    response.raise_for_status()
    
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, url):
    parsed = urlparse(url)
    bitlink = parsed.netloc + parsed.path
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary", headers=headers)
    response.raise_for_status()
    
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, url):
    parsed = urlparse(url)
    # bitlink = parsed[1] + parsed[2]
    bitlink = parsed.netloc + parsed.path
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}", headers=headers)
    return response.ok


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='Введите ссылку')
    args = parser.parse_args()
    user_input = args.link

    bitly_token = os.getenv("BITLY_TOKEN")

    requests.get(user_input).raise_for_status()

    if is_bitlink(bitly_token, user_input):
        print(f"Количество переходов по ссылке битли: {count_clicks(bitly_token, user_input)}")
    else:
        print(shorten_link(bitly_token, user_input))
