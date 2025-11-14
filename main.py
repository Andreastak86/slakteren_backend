from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(
    title="Data Slakter Backend",
    description="Backend API for Data Slakter project",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("data/gigasvaer_sales.csv", sep=";", parse_dates=["order_datetime"])

df["revenue"] = df["unit_price"] * df["quantity"] * (1 - df["discount"])

df["year_month"] = df["order_datetime"].dt.to_period("M").astype(str)


@app.get("/health")
def health():
    """Liten sjekk om serveren lever."""
    return {"status": "ok"}


@app.get("/summary/month")
def summary_per_month():
    """
    Summerer omsetning per måned.
    Returnerer f.eks:
    [
      {"year_month": "2023-01", "revenue": 123456.78},
      ...
    ]
    """
    grouped = (
        df.groupby("year_month")["revenue"]
        .sum()
        .reset_index()
        .sort_values("year_month")
    )
    return grouped.to_dict(orient="records")


@app.get("/summary/country")
def summary_per_country():
    """
    Summerer omsetning per land.
    Sortert fra høyest til lavest.
    """
    grouped = (
        df.groupby("country")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    return grouped.to_dict(orient="records")


@app.get("/top-products")
def top_products(limit: int = 10):
    """
    Topp N produkter basert på omsetning.
    /top-products?limit=5
    """
    grouped = (
        df.groupby("product")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
        .head(limit)
    )
    return grouped.to_dict(orient="records")
