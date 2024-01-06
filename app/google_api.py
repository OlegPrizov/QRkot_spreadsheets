from copy import deepcopy
from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

GET_REPORT_TO_GOOGLE = 'Добавить данные о проектах в гугл-таблицу'
TABLE_NAME = 'Отчет от {now_date_time}'
SHEET_NAME_RATING_SPEED_CLOSING = 'Рейтинг проектов по быстроте закрытия'
ROW_COUNT = 100
COLUMN_COUNT = 100
FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_BODY = dict(
    properties=dict(
        title=TABLE_NAME.format(now_date_time=datetime.now().strftime(FORMAT)),
        locale='ru_RU'
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title=SHEET_NAME_RATING_SPEED_CLOSING,
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT
        )
    ))]
)
TABLE_HEADER = [
    ['Отчет от', datetime.now().strftime(FORMAT)],
    ['Количество по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheet_create(
        wrapper_service: Aiogoogle,
        spreadsheet_body=None
) -> str:
    if spreadsheet_body is None:
        spreadsheet_body = deepcopy(SPREADSHEET_BODY)
        spreadsheet_body['properties']['title'] = TABLE_NAME.format(
            now_date_time=datetime.now().strftime(FORMAT)
        )
    service = await wrapper_service.discover('sheets', 'v4')
    response = await wrapper_service.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['url']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_service: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_service.discover('drive', 'v3')
    await wrapper_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def get_spreadsheet_id(wrapper_service: Aiogoogle) -> str:
    spreadsheet_id, url = spreadsheet_create(
        wrapper_service=wrapper_service
    )
    return spreadsheet_id, url


async def spreadsheet_update_value(
    spreadsheet_id: str,
    projects: List[CharityProject],
    wrapper_service: Aiogoogle
) -> None:
    service = await wrapper_service.discover('sheets', 'v4')
    await set_user_permissions(
        spreadsheet_id=spreadsheet_id,
        wrapper_service=wrapper_service
    )
    table_header = deepcopy(TABLE_HEADER)
    table_header[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *table_header,
        *[list(map(str, [
            attr.name, attr.close_date - attr.create_date, attr.description
        ])) for attr in projects],
    ]
    rows = len(table_values)
    columns = max(map(len, table_values))
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    if rows > ROW_COUNT or columns > COLUMN_COUNT:
        raise ValueError(
            f'Превышены размеры таблицы. '
            f'Количество строк – {rows}, а максимум – {ROW_COUNT}. '
            f'Количество столбцов – {columns}, а максимум – {COLUMN_COUNT}. '
        )
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
