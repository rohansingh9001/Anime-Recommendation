from html.parser import HTMLParser


anime = []


class ParseAnimeXML(HTMLParser):
    def handle_data(self, data):
        if data[:30] == "https://myanimelist.net/anime/":
            parts = data.split("/")
            ID, NAME = parts[4], parts[5]
            anime.append(f"{ID},{NAME}\n")


with open("anime.xml", "r", encoding="utf-8") as file:
    xml = file.read()
    parser = ParseAnimeXML()
    parser.feed(xml)

with open("anime.csv", "w", encoding="utf-8") as file:
    file.writelines(anime)
