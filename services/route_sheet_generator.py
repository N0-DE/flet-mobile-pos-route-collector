"""
Route Sheet Generator Service
Reads daily delivery route dispatch data, computes cumulative balances,
and outputs styled, print-ready Excel spreadsheets with custom borders,
fonts, and dynamic column formatting using openpyxl.
"""
from datetime import date
from pathlib import Path
import pandas as pd
import openpyxl
from openpyxl.styles import Font, Border, Side, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import config

def generate_styled_route_sheet(output_dir: Path = None) -> Path:
    target_dir = output_dir or config.BASE_DIR
    today_str = date.today().strftime("%d-%m-%Y")
    output_file = target_dir / f"Route_Dispatch_{today_str}.xlsx"

    # Ingest data
    if config.SAMPLE_DATA_PATH.exists():
        df = pd.read_csv(config.SAMPLE_DATA_PATH)
    else:
        df = pd.DataFrame([
            {"Sequence": 1, "CustomerName": "Customer A", "OutstandingBalance": 1000, "TodayBill": 200},
            {"Sequence": 2, "CustomerName": "Customer B", "OutstandingBalance": 500, "TodayBill": 150}
        ])

    df.to_excel(output_file, sheet_name="DispatchRoute", index=False)

    # Style Excel Workbook with openpyxl
    wb = openpyxl.load_workbook(output_file)
    ws = wb.active

    header_font = Font(name="Arial", size=12, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    data_font = Font(name="Arial", size=11)
    
    thin_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC")
    )

    # Format Headers
    for col in range(1, len(df.columns) + 1):
        cell = ws.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Format Data Rows
    for row in range(2, len(df) + 2):
        for col in range(1, len(df.columns) + 1):
            cell = ws.cell(row=row, column=col)
            cell.font = data_font
            cell.border = thin_border
            if col == 1:
                cell.alignment = Alignment(horizontal="center")

    # Dynamic Column Widths
    for column in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in column)
        col_letter = get_column_letter(column[0].column)
        ws.column_dimensions[col_letter].width = max(max_length + 4, 12)

    wb.save(output_file)
    print(f"[+] Styled route sheet generated: {output_file}")
    return output_file

if __name__ == "__main__":
    generate_styled_route_sheet()
