import requests
import random
import json
from parsel import Selector

class OlxScraper:
    def __init__(self, max_data=1000):
        self.base_url = "https://www.olx.in"
        self.start_url = f"{self.base_url}/kozhikode_g4058877/for-rent-houses-apartments_c1723"
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36"
        ]
        self.headers = {
            "User-Agent": random.choice(self.user_agents)
        }
        self.results = []
        self.max_data = max_data

    def fetch_page(self, url):
        """Fetches a page and returns the HTML content."""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def parse_listing_page(self, html):
        """Parses the listing page for individual property URLs and the next page."""
        selector = Selector(html)
        property_urls = [
            self.base_url + href
            for href in selector.css("li._1DNjI a::attr(href)").getall()
        ]
        next_page = selector.css("a._30kbx.da3cR::attr(href)").get()
        return property_urls, next_page

    def parse_property_page(self, html):
        """Parses the property page and extracts details."""
        selector = Selector(html)
        return {
            "property_name": selector.css('h1[data-aut-id="itemTitle"]::text').get(default='N/A'),
            "property_id": (selector.xpath("//div[@class='_1-oS0']//strong/text()").get(default='N/A').split()[-1]
                            if selector.xpath("//div[@class='_1-oS0']//strong/text()") else 'N/A'),
            "breadcrumbs": selector.xpath("//ol[@class='rui-2Pidb']/li/a[@class='_26_tZ']/text()").getall() or ['N/A'],
            "price": selector.css('span[data-aut-id="itemPrice"]::text').get() or 'N/A',
            "image_url": selector.css('img[data-aut-id="defaultImg"]::attr(src)').get() or 'N/A',
            "description": selector.css('div[data-aut-id="itemDescriptionContent"] p::text').getall() or ['N/A'],
            "seller_name": selector.xpath('//div[@class="eHFQs"]/text()[normalize-space()]').get(default='N/A'),
            "location": selector.xpath('//span[@class="_1RkZP"]/text()').get(default='N/A'),
            "property_type": selector.xpath('//span[@class="B6X7c"]/text()').get(default='N/A'),
            "bathrooms": selector.xpath('//span[@data-aut-id="value_bathrooms"]/text()').get(default='N/A'),
            "bedrooms": selector.xpath('//span[@data-aut-id="value_rooms"]/text()').get(default='N/A'),
        }

    def save_to_json(self, filename):
        """Saves the scraped data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)

    def run(self):
        """Executes the scraper."""
        current_url = self.start_url
        while current_url and len(self.results) < self.max_data:
            print(f"Fetching: {current_url}")
            html = self.fetch_page(current_url)
            property_urls, next_page = self.parse_listing_page(html)

            for property_url in property_urls:
                if len(self.results) >= self.max_data:
                    break
                print(f"Fetching property: {property_url}")
                property_html = self.fetch_page(property_url)
                property_data = self.parse_property_page(property_html)
                self.results.append(property_data)

            if next_page:
                current_url = self.base_url + next_page
            else:
                current_url = None

        # Save and print JSON
        print(json.dumps(self.results, ensure_ascii=False, indent=4))
        self.save_to_json("olx_properties.json")
        print("Scraping complete. Data saved to 'olx_properties.json'.")

# Run the scraper
if __name__ == "__main__":
    scraper = OlxScraper(max_data=1000)
    scraper.run()