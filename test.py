from bs4 import BeautifulSoup
import pandas as pd
import requests

response = requests.get(
    "https://catalogue.uci.edu/previouseditions/2019-20/thehenrysamuelischoolofengineering/departmentofmechanicalandaerospaceengineering/#majorstext"
)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("h4", text=lambda t: "Mechanical Engineering" in t).find_next(
    "table", class_="sc_plangrid"
)

print(table)
print(type(table))
