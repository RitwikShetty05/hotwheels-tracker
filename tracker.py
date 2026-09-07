import requests
from bs4 import BeautifulSoup

products = [
    {"name": "Charger", "url": "https://www.amazon.in/dp/B0GX5DG4N6/"},
    {"name": "Mazda", "url": "https://www.amazon.in/dp/B0GX52J7QH/"},
    {"name": "Civic", "url": "https://www.amazon.in/dp/B0GXDYV59X/"},
    {"name": "Supra", "url": "https://www.amazon.in/dp/B0HFNCLR8C/"},
]

price_limit = 400
ntfy_topic = "ritwik-hotwheels-alert"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
})

def get_price(soup):
    selectors = [
        "span.a-price-whole",
        "span.a-price.aok-align-center span.a-offscreen",
        "span#priceblock_ourprice",
        "span#priceblock_dealprice"
    ]
    for selector in selectors:
        price_tag = soup.select_one(selector)
        if price_tag is not None:
            price_text = price_tag.get_text()
            price_text = price_text.replace("₹", "").replace(",", "").split(".")[0].strip()
            if price_text.isdigit():
                return int(price_text)
    return None

def send_phone_alert(message):
    requests.post(
        "https://ntfy.sh/" + ntfy_topic,
        data=message.encode("utf-8"),
        headers={"Priority": "urgent", "Title": "Hot Wheels Price Alert"}
    )

for product in products:
    response = session.get(product["url"])
    soup = BeautifulSoup(response.text, "html.parser")
    price = get_price(soup)

    if price is None:
        print("Could not read price for " + product["name"])
    else:
        print(product["name"] + " is currently at Rs " + str(price))

        if price < price_limit:
            alert_message = product["name"] + " dropped to Rs " + str(price) + "! " + product["url"]
            send_phone_alert(alert_message)
            print("ALERT SENT: " + alert_message)
