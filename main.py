# main.py - Mini Google ra main engine

from search import search_data
from shortener import make_short

print("Mini Google Chalu Hei Gala!")

result = search_data("python")
print("Search Result:", result)

short = make_short("https://www.google.com/very-long-link")
print("Short Link:", short)