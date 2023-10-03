import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import List, Any
from google.auth.transport.requests import Request
from .chatgpt import generate_response  # make sure to import generate_response from chatgpt.py
from datetime import datetime



# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of the spreadsheet.
SAMPLE_SPREADSHEET_ID = '1O4fKy9WYVEljNWQjC73mf3WBcIBnC_sOOZNnQhLg_pc'
SAMPLE_RANGE_NAME = 'Sheet1!A1:C500'  # Adjust according to your sheet's range.

# Path to credentials.json
CREDENTIALS_FILE_PATH = 'C:/Users/ferna/OneDrive/Escritorio/MyTelegramBot/resources/credentials.json'


def service_gsheets():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first time.
    token_path = 'C:/Users/ferna/OneDrive/Escritorio/MyTelegramBot/resources/token.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    return sheet


def read_sheet(sheet, range_name=SAMPLE_RANGE_NAME):
    """Reads values from a specific range in the sheet"""
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=range_name).execute()
    values = result.get('values', [])
    return values


def write_to_sheet(spreadsheet_id: str, column: str, values: List[List[Any]]):
    service = service_gsheets()
    sheet_name = 'Sheet1'

    range_name = 'A'
    result = service.values().get(spreadsheetId=spreadsheet_id,
                                  range=f'{sheet_name}!{range_name}1:{range_name}').execute()

    values_in_column = result.get('values', [])
    first_empty_row = len(values_in_column) + 1

    if column == 'A':
        # Handling for column A
        new_range = f'{range_name}{first_empty_row}'
        body = {'values': values}
        service.values().update(spreadsheetId=spreadsheet_id, range=new_range, body=body,
                                valueInputOption='RAW').execute()

        # ChatGPT prompt for column B
        user_message = values[0][0]
        chatgpt_prompt_b = f"Escribe unicamente y, sin incluir comillas, la categoria del siguiente texto bajo las siguientes opciones: 'Agua' 'Luz' 'Gas' 'Impuestos Municipales' 'Impuestos Provinciales' 'Internet' 'Expensas' 'Nafta' 'Salidas' 'Verduleria' 'Carniceria' 'Supermercado' 'Alarma 'Jardineria' 'Otros': {user_message} (antes de enviar el resultado, asegurarse que sea sin comillas)"
        chatgpt_response_b = generate_response(chatgpt_prompt_b)

        # Writing response to column B
        service.values().update(spreadsheetId=spreadsheet_id, range=f'B{first_empty_row}',
                                body={'values': [[chatgpt_response_b]]}, valueInputOption='RAW').execute()

        # ChatGPT prompt for column C
        chatgpt_prompt_c = f"Escribe unicamente el numero que esta asociado al siguiente texto: {user_message}"
        chatgpt_response_c = generate_response(chatgpt_prompt_c)

        # Convert response to number
        try:
            chatgpt_response_c = float(chatgpt_response_c)  # convert to float; or use int() if you know it's an integer
        except ValueError:
            # Handle the case where the response is not a valid number.
            pass  # or log an error message or handle differently as per your needs


        # Writing response to column C
        service.values().update(spreadsheetId=spreadsheet_id, range=f'C{first_empty_row}',
                                body={'values': [[chatgpt_response_c]]}, valueInputOption='RAW').execute()

        # ...

        # ChatGPT prompt for column D
        chatgpt_prompt_d = f"Escribe unicamente el segundo numero que hace referencia el siguiente mensaje (en caso de no haber segundo numero, colocar 1): {user_message}"
        chatgpt_response_d = generate_response(chatgpt_prompt_d)

        # Convert response to number
        try:
            chatgpt_response_d = int(chatgpt_response_d)  # convert to int
        except ValueError:
            # Handle the case where the response is not a valid number.
            pass  # or log an error message or handle differently as per your needs

        # Writing response to column D
        service.values().update(spreadsheetId=spreadsheet_id, range=f'D{first_empty_row}',
                                body={'values': [[chatgpt_response_d]]}, valueInputOption='RAW').execute()

        # ...

        # Getting current date and time and formatting it correctly
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Writing formatted date and time to column E
        service.values().update(spreadsheetId=spreadsheet_id, range=f'E{first_empty_row}',
                                body={'values': [[current_datetime]]}, valueInputOption='USER_ENTERED').execute()
        # Get the response from column D
        divide_by = chatgpt_response_d

        # Parse the date from column E
        current_datetime = datetime.now()

        for i in range(divide_by):
            # Calculate the amount for each month
            divided_amount = chatgpt_response_c / divide_by

            # Write to the sheet
            new_row_index = first_empty_row + i  # Increment row index for each iteration

            # Repeat the value in columns A and B
            service.values().update(spreadsheetId=spreadsheet_id, range=f'A{new_row_index}',
                                    body={'values': [[values[0][0]]]}, valueInputOption='RAW').execute()
            service.values().update(spreadsheetId=spreadsheet_id, range=f'B{new_row_index}',
                                    body={'values': [[chatgpt_response_b]]}, valueInputOption='RAW').execute()

            # Writing response to column C with divided amount
            service.values().update(spreadsheetId=spreadsheet_id, range=f'C{new_row_index}',
                                    body={'values': [[divided_amount]]}, valueInputOption='RAW').execute()

            # Format and write date to column E with incremented month
            incremented_month_datetime = current_datetime.replace(month=((current_datetime.month - 1 + i) % 12) + 1)
            if i > 0 and incremented_month_datetime.month == 1:  # Handle year increment
                incremented_month_datetime = incremented_month_datetime.replace(
                    year=incremented_month_datetime.year + 1)

            # Format the date string
            incremented_month_str = incremented_month_datetime.strftime('%Y-%m-%d %H:%M:%S')

            # Repeat the value in column D
            service.values().update(spreadsheetId=spreadsheet_id, range=f'D{new_row_index}',
                                    body={'values': [[chatgpt_response_d]]}, valueInputOption='RAW').execute()

            # Writing incremented date to column E
            service.values().update(spreadsheetId=spreadsheet_id, range=f'E{new_row_index}',
                                    body={'values': [[incremented_month_str]]},
                                    valueInputOption='USER_ENTERED').execute()

        return chatgpt_response_b, chatgpt_response_c

    else:
        # Handling for column != 'A'
        new_range = f'{column}{first_empty_row}'
        body = {'values': values}
        service.values().update(spreadsheetId=spreadsheet_id, range=new_range, body=body,
                                valueInputOption='RAW').execute()

        return None





