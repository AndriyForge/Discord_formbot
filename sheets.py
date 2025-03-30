from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Подключение через Google API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'discordmemberidroles-9d911218061b.json'  # Файл с ключами

# ID Google Таблицы (скопируйте из URL)
SPREADSHEET_ID = '1rWwZUFB68ODrGXQTiIpbgmtssBSVbtq03DWzq_j7tkQ'
RANGE_NAME = 'Аркуш3!A2:B9'  # Диапазон данных (имя пользователя и роль)

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

def get_data():
    print(f"⏳ Запрашиваю диапазон: {RANGE_NAME} в таблице {SPREADSHEET_ID}")

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print("❌ Данные не найдены! Проверьте таблицу и доступ.")
        return []
    
    print("✅ Получены данные:")
    for row in values:
        print(row)
    
    return values

if __name__ == "__main__":
    data = get_data()
    for row in data:
        print(f"{row[0]} → {row[1]}")  # Например, "andri → Admin"
