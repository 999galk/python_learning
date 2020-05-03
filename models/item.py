import re
import uuid
from typing import Dict
import requests
# type hinting - means we give params the expected var type,
# it wont break the program, only pops up warning
from bs4 import BeautifulSoup
from models.model import Model


class Item(Model):
    collection = 'items'  # mongo collection in which it will be kept

    def __init__(self, url: str, tag_name: str, query: Dict, _id: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = ""
        self.tag_name = tag_name
        self.query = query
        self.price = None
        self._id = _id or uuid.uuid4.hex

    def __repr__(self):
        return f"<Item {self.url}>"

    #type hinting for return value of function is with an arrow at the declaration
    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()
        pattern = re.compile(r"(\d+,?\d*\.\d*)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_comma = found_price.replace(",", "")
        self.price = float(without_comma)
        return self.price

    def json(self) -> Dict:
        return{
            "_id" : self._id,
            "url" : self.url,
            "tag_name" : self.tag_name,
            "query" : self.query
        }

