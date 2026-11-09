# search.py - Google bhali search ra budhi

# Amara chhota database - 5 ta website
websites = [
    {"title": "Python Tutorial", "link": "python.org", "text": "python learn coding"},
    {"title": "Google Jobs", "link": "google.com/jobs", "text": "google job interview"},
    {"title": "Learn Odia Coding", "link": "coding.com", "text": "learn python coding"},
]

def search_data(query):
    query = query.lower()
    result = []
    for site in websites:
        if query in site["text"]:
            result.append(site)
    return result