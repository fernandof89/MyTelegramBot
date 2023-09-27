from src.services.google_sheets import service_gsheets, write_to_sheet

if __name__ == "__main__":
    sheet = service_gsheets()
    range_name = 'Sheet1!A1'
    write_to_sheet(sheet, range_name, [["Test Message"]])
