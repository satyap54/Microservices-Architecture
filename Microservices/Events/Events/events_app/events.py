from fastapi import APIRouter
from models import Event, EventUser
from typing import List
from . schemas import EventPydantic


router = APIRouter(tags=["events"])


@router.get('/api/events', response_model=List[EventPydantic])
async def index():
    events_list = await Event.all()
    response = [EventPydantic.from_orm(obj) for obj in events_list]
    return events_list