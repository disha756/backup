from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# -----------------------------------
# CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Fake User
# -----------------------------------

FAKE_USER = {
    "email": "jack@example.com",
    "password": "qwerty",
    "name": "Jack",
    "avtar": "https://i.pravatar.cc/100?u=zz",
}

FAKE_TOKEN = "mysecrettoken123"

# -----------------------------------
# Models
# -----------------------------------


class LoginData(BaseModel):
    email: str
    password: str


class Position(BaseModel):
    lat: float
    lng: float


class City(BaseModel):
    cityName: str
    country: str
    emoji: str
    date: str
    notes: str
    position: Position
    id: int | None = None


# -----------------------------------
# Fake Database
# -----------------------------------

cities = [
    {
        "cityName": "Lisbon",
        "country": "Portugal",
        "emoji": "🇵🇹",
        "date": "2027-10-31T15:59:59.138Z",
        "notes": "My favorite city so far!",
        "position": {"lat": 38.727881642324164, "lng": -9.140900099907554},
        "id": 73930385,
    },
    {
        "cityName": "Madrid",
        "country": "Spain",
        "emoji": "🇪🇸",
        "date": "2027-07-15T08:22:53.976Z",
        "notes": "",
        "position": {"lat": 40.46635901755316, "lng": -3.7133789062500004},
        "id": 17806751,
    },
    {
        "cityName": "Berlin",
        "country": "Germany",
        "emoji": "🇩🇪",
        "date": "2027-02-12T09:24:11.863Z",
        "notes": "Amazing 😃",
        "position": {"lat": 52.53586782505711, "lng": 13.376933665713324},
        "id": 98443197,
    },
]

# -----------------------------------
# Auth Dependency
# -----------------------------------


def verify_token(authorization: str = Header(None)):
    if authorization != f"Bearer {FAKE_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


# -----------------------------------
# Login Route
# -----------------------------------


@app.post("/login")
def login(data: LoginData):

    if data.email == FAKE_USER["email"] and data.password == FAKE_USER["password"]:
        return {"token": FAKE_TOKEN, "user": FAKE_USER}

    raise HTTPException(status_code=401, detail="Invalid credentials")


# -----------------------------------
# Protected Routes
# -----------------------------------


@app.get("/cities")
def get_cities():#user=Depends(verify_token)):
    return cities


@app.get("/cities/{city_id}")
def get_city(city_id: int):#, user=Depends(verify_token)):
    city = next((c for c in cities if c["id"] == city_id), None)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@app.post("/cities")
def create_city(city: City):#, user=Depends(verify_token)):
    new_city = city.dict()

    new_city["id"] = random.randint(10000000, 99999999)

    cities.append(new_city)

    return new_city


@app.delete("/cities/{city_id}")
def delete_city(city_id: int):#, user=Depends(verify_token)):
    city = next((c for c in cities if c["id"] == city_id), None)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    cities.remove(city)

    return {"message": "City deleted"}
