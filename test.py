from bs4 import BeautifulSoup
import pandas as pd
import requests

response = requests.get(
    "https://catalogue.uci.edu/previouseditions/2019-20/thehenrysamuelischoolofengineering/departmentofmechanicalandaerospaceengineering/#majorstext"
)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find_all("h4", string=lambda s: s and "Requirements for the" in s)

print(table)
print(type(table))
