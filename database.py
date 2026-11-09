# database.py - Data rakhhiba jagah

saved_links = {}

def save_link(short, long):
    saved_links[short] = long
    print("Save hei gala:", short)

def get_link(short):
    return saved_links.get(short, "Milila ni")