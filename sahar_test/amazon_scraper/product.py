from bs4 import BeautifulSoup
from .css_selectors import css_selectors

class Product:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, 'lxml')
    
    async def extract_info(self):
        # Extracting information using CSS selectors
        title = self._extract_text(css_selectors["title"])
        price = self._extract_price(css_selectors["price"])
        reviews = self._extract_reviews(css_selectors["reviews"])
        description = self._extract_description(css_selectors["pre_descripton"])
        rating = self._extract_rating(css_selectors["rating"])

        return {
            "title": title,
            "price": price,
            "reviews": reviews,
            "description": description,
            "rating": rating
        }

    def _extract_text(self, selector):
        element = self.soup.select_one(selector)
        return element.get_text().strip() if element else "Not found"

    def _extract_price(self, selector):
        price = self._extract_text(selector)
        return price.split("&")[0] if price != "Not found" else price

    def _extract_reviews(self, selector):
        reviews = [review.get_text().strip() for review in self.soup.select(selector)]
        return reviews[:5]

    def _extract_description(self, selector):
        elements = self.soup.select(selector)
        return [elem.get_text().strip() for elem in elements] if elements else "Not found"

    def _extract_rating(self, selector):
        rating = self._extract_text(selector)
        return rating.split(" ")[0] if rating != "Not found" else rating