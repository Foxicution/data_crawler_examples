from requests import get

headers = {
    "authority": "api.oneweb.mercedes-benz.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.mercedes-benz.lt",
    "referer": "https://www.mercedes-benz.lt/passengercars.html?group=all&subgroup=all.saloon&view=BODYTYPE",
    "sec-ch-ua": '"Chromium";v="119", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}


if __name__ == "__main__":
    response = get(
        "https://api.oneweb.mercedes-benz.com/vmos-api/v1/data/LT/lt/OWF/live",
        headers=headers,
    )
    print(response.json())
