

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

def scrape_amazon_product(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8"
        }
        status_code = 503

        while status_code != 200:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                product_name = soup.find('span', class_='a-size-large product-title-word-break')
                price_element = soup.find('span', class_='a-price-whole')
                if price_element:
                    return product_name.get_text().strip()[:50], price_element.get_text().strip()

    except Exception as e:
        return None, str(e)

def scrape_snapdeal_product(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_name = soup.find('h1', {'class': 'pdp-e-i-head'}).text.strip()
        product_price = soup.find('span', {'class': 'payBlkBig'})
        if product_price:
            return product_name[:50], product_price.text.strip()
        else:
            return None, "Price not found"

    except Exception as e:
        return None, str(e)

# Get Amazon and Snapdeal URLs from the user
amazon_url = input("Enter the Amazon product URL: ")
snapdeal_url = input("Enter the Snapdeal product URL: ")

# Scrape data from both websites
amazon_product_name, amazon_product_price = scrape_amazon_product(amazon_url)
snapdeal_product_name, snapdeal_product_price = scrape_snapdeal_product(snapdeal_url)

# Calculate the lower price
if amazon_product_price and snapdeal_product_price:
    amazon_price = float(amazon_product_price.replace(',', ''))
    snapdeal_price = float(snapdeal_product_price.replace(',', ''))
    lower_price = "Amazon" if amazon_price < snapdeal_price else "Snapdeal"
else:
    lower_price = "N/A"

# Create a list of lists with the data
table_data = [
    ['Website', 'Product Name', 'Product Price'],
    ['Amazon', amazon_product_name, amazon_product_price],
    ['Snapdeal', snapdeal_product_name, snapdeal_product_price],
    ['Comparison', '', f'Lower Price: {lower_price}']
]

table = tabulate(table_data, headers='firstrow', tablefmt='grid')

# Display the table
print(table)


