from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Model dla danych wejściowych i wyjściowych
class InputData(BaseModel):
    input: str

class OutputData(BaseModel):
    output: str

# Załaduj dane z osoby.json (w praktyce pobierz z https://letsplay.ag3nts.org/data/osoby.json)
# Dla uproszczenia zakładam lokalny plik lub wczytanie w kodzie
with open("osoby.json", "r") as f:
    osoby = json.load(f)

@app.post("/webhook")
async def webhook(data: InputData):
    # Przykład: input = "pobierz zespół 1"
    if data.input.startswith("pobierz zespół"):
        team_id = int(data.input.split()[-1])
        # Filtruj osoby z danym zespołem
        team_members = [
            {"imie": osoba["imie"], "nazwisko": osoba["nazwisko"]}
            for osoba in osoby
            if osoba.get("zespół_id") == team_id
        ]
        return OutputData(output=json.dumps(team_members))
    return OutputData(output="Nieprawidłowe zapytanie")
