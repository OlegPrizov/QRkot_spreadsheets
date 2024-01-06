from typing import Dict

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException

from app.core import db, user
from app.core.google_client import get_service
from app.crud.charity_project import charity_project_crud
from app.google_api import (
    GET_REPORT_TO_GOOGLE,
    get_spreadsheet_id,
    spreadsheet_update_value
)

router = APIRouter()


@router.get(
    path='/',
    summary=GET_REPORT_TO_GOOGLE,
    dependencies=[Depends(user.current_superuser)]
)
async def get_report(
    session: db.AsyncSession = Depends(db.get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
) -> Dict[str, str]:
    closed_projects = await charity_project_crud.get_projects_by_completion_rate(
        session=session
    )
    spreadsheet_id, url = await get_spreadsheet_id(
        wrapper_service=wrapper_service
    )
    try:
        await spreadsheet_update_value(
            spreadsheet_id=spreadsheet_id,
            projects=closed_projects,
            wrapper_service=wrapper_service
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    return {'url': url}
