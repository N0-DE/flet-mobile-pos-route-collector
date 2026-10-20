"""
Flet Mobile POS & Merchant Route Collection App
Cross-platform application built using Flet (Python with Flutter framework).
Features merchant overview, recent collection feed, route stop selector,
and transaction receipt entry with offline mock data support.
"""
import sys
from pathlib import Path
import pandas as pd
import flet as ft

# Add parent to path for config
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def load_route_customers():
    """Loads route customer list from database or sample CSV."""
    if config.USE_OFFLINE_MOCK or not config.DB_PASSWORD:
        if config.SAMPLE_DATA_PATH.exists():
            df = pd.read_csv(config.SAMPLE_DATA_PATH)
            return [f"{r['Sequence']}. {r['CustomerName']}" for _, r in df.iterrows()]
        return ["1. Customer Alpha", "2. Customer Beta", "3. Customer Gamma"]

    try:
        import pyodbc
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};SERVER={config.DB_HOST};DATABASE={config.DB_NAME};UID={config.DB_USER};PWD={config.DB_PASSWORD}"
        )
        cur = conn.cursor()
        cur.execute("SELECT slno, party_name FROM Route ORDER BY slno")
        rows = cur.fetchall()
        conn.close()
        return [f"{r[0]}. {r[1]}" for r in rows]
    except Exception as e:
        print(f"[-] DB connection failed ({e}). Loading fallback.")
        return ["1. Customer Alpha", "2. Customer Beta", "3. Customer Gamma"]

def main(page: ft.Page):
    page.title = "Route POS Merchant"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15

    customer_options = load_route_customers()

    # Form Controls
    customer_dropdown = ft.Dropdown(
        label="Select Customer / Route Stop",
        options=[ft.dropdown.Option(c) for c in customer_options],
        value=customer_options[0] if customer_options else None,
        autofocus=True
    )
    amount_field = ft.TextField(
        label="Collection Amount ($ / ₹)",
        keyboard_type=ft.KeyboardType.NUMBER
    )
    notes_field = ft.TextField(
        label="Payment Mode / Notes",
        hint_text="e.g. Cash, GPay, Cheque, Damage Credit",
        multiline=True
    )

    transactions_list = ft.Column(
        controls=[
            ft.ListTile(
                title=ft.Text("Grand Central Mart"),
                subtitle=ft.Text("Today • 11:45 AM • UPI"),
                trailing=ft.Text("+ $450.00", color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD)
            ),
            ft.ListTile(
                title=ft.Text("Sunshine Bakeries"),
                subtitle=ft.Text("Today • 10:15 AM • Cash"),
                trailing=ft.Text("+ $210.00", color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD)
            ),
            ft.ListTile(
                title=ft.Text("City Corner Store"),
                subtitle=ft.Text("Yesterday • 04:30 PM • Card"),
                trailing=ft.Text("+ $680.00", color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD)
            )
        ],
        height=240,
        scroll=ft.ScrollMode.AUTO
    )

    def go_back(e):
        page.views.pop()
        page.go("/")

    def record_transaction(e):
        cust = customer_dropdown.value or "Unknown"
        amt = amount_field.value.strip()
        note = notes_field.value.strip() or "Cash"

        if not amt:
            return

        transactions_list.controls.insert(
            0,
            ft.ListTile(
                title=ft.Text(cust.split(". ")[-1]),
                subtitle=ft.Text(f"Just now • {note}"),
                trailing=ft.Text(f"+ ${float(amt):,.2f}", color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD)
            )
        )
        amount_field.value = ""
        notes_field.value = ""
        go_back(None)

    def route_change(e):
        page.views.clear()

        # Route 1: Home View
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text("Route POS Merchant", weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.SURFACE_VARIANT,
                        actions=[
                            ft.IconButton(ft.Icons.PERSON)
                        ]
                    ),
                    # Merchant Header
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.STORE, size=32, color=ft.Colors.BLUE_400),
                            ft.Column([
                                ft.Text(config.MERCHANT_NAME, size=16, weight=ft.FontWeight.BOLD),
                                ft.Text("Route Delivery Terminal #01", size=12, color=ft.Colors.GREY_400)
                            ])
                        ]),
                        padding=10
                    ),
                    # Daily Summary Card
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Total Collected Today", size=13, color=ft.Colors.GREY_400),
                            ft.Text("$1,340.00", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                            ft.ElevatedButton(
                                "Record New Collection Receipt",
                                icon=ft.Icons.ADD_CARD,
                                on_click=lambda _: page.go("/new-receipt"),
                                style=ft.ButtonStyle(bgcolor=ft.Colors.PRIMARY, color=ft.Colors.ON_PRIMARY)
                            )
                        ]),
                        padding=15,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                        border_radius=12
                    ),
                    # Recent Transactions Section
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Recent Route Collections", size=15, weight=ft.FontWeight.BOLD),
                            transactions_list
                        ]),
                        padding=ft.padding.only(top=10)
                    )
                ]
            )
        )

        # Route 2: New Receipt Page
        if page.route == "/new-receipt":
            page.views.append(
                ft.View(
                    "/new-receipt",
                    [
                        ft.AppBar(
                            title=ft.Text("New Collection Receipt"),
                            leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back)
                        ),
                        ft.Container(
                            content=ft.Column([
                                customer_dropdown,
                                amount_field,
                                notes_field,
                                ft.ElevatedButton(
                                    "Save Collection Receipt",
                                    icon=ft.Icons.CHECK_CIRCLE,
                                    on_click=record_transaction,
                                    height=45
                                )
                            ], spacing=15),
                            padding=20
                        )
                    ]
                )
            )

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)
