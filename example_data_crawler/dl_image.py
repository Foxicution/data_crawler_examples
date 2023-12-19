import requests

headers = {
    "sec-ch-ua": '"Chromium";v="119", "Not?A_Brand";v="24"',
    "Referer": "https://www.lrytas.lt/",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": '"Linux"',
}

response = requests.get(
    "https://www.eurovaistine.lt/media/cache/ev_tablet/88/3e/357a506f7dea394c12f82a1018bd.png",
    headers=headers,
)

with open("image.png", "wb") as f:
    print(f.write(response.content))
