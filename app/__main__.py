import os.path
from typing import Any, List


from google.auth.external_account_authorized_user import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# При изменении удалить файл token.json.
SCOPES: List[str] = ["https://mail.google.com/"]


def init_mailing() -> None:
    """
    Инициализирует credentials.json и token.json.
    """
    gmail_authenticate()


def gmail_authenticate() -> Any:
    """
    Авторизирует пользователя по OAuth 2.0.

    Returns:
      Service: Авторизированный сервис Gmail API.

    Raises:
      HttpError: Если произошла ошибка при подключении к сервису Gmail API.
    """
    creds = None
    # Файл token.json содержит доступные ключи доступа и обновления,
    # и создается автоматически при первом запуске авторизационного цикла.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # Если нет доступных учетных данных, попросите пользователя войти.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(request=Request())
        else:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file="credentials.json", scopes=SCOPES
            )
            creds: Credentials = flow.run_local_server(port=0)
        # Сохраняем данные для следующего запуска
        with open(file="token.json", mode="w") as token:
            token.write(creds.to_json())

    # Подключаемся к Gmail API
    try:
        # Получаем клиент Gmail API
        service = build(serviceName="gmail", version="v1", credentials=creds)
        return service

    except HttpError as e:
        print(e)
        print("Не получилось авторизовать GMAIL API клиент")
        exit(code=403)


if __name__ == "__main__":
    init_mailing()
    print("GMAIL API клиент инициализирован")
