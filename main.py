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

@app.post("/webhook")
async def webhook(data: InputData):
    # Obsługa testu weryfikacyjnego
    if data.input.startswith("test"):
        return OutputData(output=data.input)
    # Obsługa pobierania osób
    if data.input.startswith("pobierz osoby z "):
        uczelnia = data.input.replace("pobierz osoby z ", "")
        try:
            response = requests.get(OSOBY_URL)
            response.raise_for_status()
            osoby = response.json()
            team_members = [
                {"imie": osoba["imie"], "nazwisko": osoba["nazwisko"]}
                for osoba in osoby
                if osoba["uczelnia"].lower() == uczelnia.lower()
            ]
            return OutputData(output=json.dumps(team_members))
        except requests.RequestException as e:
            return OutputData(output=f"Błąd: {str(e)}")
    return OutputData(output="Nieprawidłowe zapytanie")
