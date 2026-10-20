"""
Configuration for Flet Mobile POS & Route Collector.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

USE_OFFLINE_MOCK = os.getenv("USE_OFFLINE_MOCK", "true").lower() == "true"
MERCHANT_NAME = os.getenv("MERCHANT_NAME", "Store Merchant Express")

DB_HOST = os.getenv("ROUTE_DB_HOST", "localhost")
DB_NAME = os.getenv("ROUTE_DB_NAME", "RouteSale")
DB_USER = os.getenv("ROUTE_DB_USER", "sa")
DB_PASSWORD = os.getenv("ROUTE_DB_PASSWORD", "")

SAMPLE_DATA_PATH = BASE_DIR / "sample_data" / "sample_route_customers.csv"
