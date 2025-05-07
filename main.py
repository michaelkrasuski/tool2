from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class InputData(BaseModel):
    input: str

class OutputData(BaseModel):
    output: str

OSOBY_URL = "https://letsplay.ag3nts.org/data/osoby.json?v=1743591162"

def get_uczelnia_code(nazwa):
    words = nazwa.split()
    if len(words) < 2:
        return "".join(word[:3].upper() for word in words)
    return words[0][:3].upper() + words[1][:3].upper()

@app.post("/webhook")
async def webhook(data: InputData):
    # Obsługa testu weryfikacyjnego
    if data.input.startswith("test"):
        return OutputData(output=data.input)
    # Obsługa pobierania osób
    if data.input.startswith("pobierz osoby z "):
        uczelnia_nazwa = data.input.replace("pobierz osoby z ", "")
        uczelnia_code = get_uczelnia_code(uczelnia_nazwa)
        try:
            response = requests.get(OSOBY_URL)
            response.raise_for_status()
            osoby = response.json()
            team_members = [
                {"imie": osoba["imie"], "nazwisko": osoba["nazwisko"]}
                for osoba in osoby
                if osoba["uczelnia"] == uczelnia_code
            ]
            return OutputData(output=json.dumps(team_members))
        except requests.RequestException as e:
            return OutputData(output=f"Błąd: {str(e)}")
    return OutputData(output="Nieprawidłowe zapytanie")
