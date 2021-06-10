import requests
from fastapi import APIRouter, Depends, HTTPException, status
from models import Event, EventUser
from typing import List
from . schemas import EventPydantic
from dependencies import oauth2_scheme, SECRET_KEY, ALGORITHM
from producer import publish
import jwt


router = APIRouter(tags=["events"])


@router.get('/api/events', response_model=List[EventPydantic])
async def index(token: str=Depends(oauth2_scheme)):
    events_list = await Event.all()
    response = [EventPydantic.from_orm(obj) for obj in events_list]
    return events_list
    
@router.post('/api/events/{event_id}/attend')
async def attend_event(event_id: int, token: str=Depends(oauth2_scheme)):
    ''''
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    req = requests.get("http://127.0.0.1:8001/api/events/", headers=headers)
    #print(req.json())
    '''

    user_id = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload["user_id"]
        #print(payload)
    except:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="Invalid Token",
        )
        
    already_attending = await EventUser.get_or_none(event_id=event_id, user_id=user_id)
    if already_attending:
        return {
            "message": "Already signed up",
            "status": status.HTTP_400_BAD_REQUEST
        }
        
    create_attendance = await EventUser.create(user_id=user_id, event_id=event_id)
    
    await publish('event attendee', event_id)
    
    return {
        "messaged": "Signed up",
        "status": status.HTTP_200_OK
    }