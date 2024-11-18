import requests
from bs4 import BeautifulSoup

class Store:

    def search_package_store(self, query):
        url = f"https://pypi.org/search/?q={query}"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            results = soup.find_all('a', class_='package-snippet')

            packages = []
            for result in results:
                package_name = result.find('h3').text.strip()
                package_description = result.find('p').text.strip()
                package_url = result.get('href')
                packages.append({
                    "name": package_name,
                    "description": package_description,
                    "url": f"https://pypi.org{package_url}"
                })

            return packages
        
        else:
            print(f"Error fetching results from PyPI: {response.status_code}")
            return []
        

if __name__ == "__main__":
    store = Store()

    query = "numpy"

    results = store.search_package_store(query)

    print(results)

