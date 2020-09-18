from sqlalchemy import extract

from app.models import *


def read_room_infos(name=None, kind_of_room_id=None, status=None, amount = None):
    room = Room.query.all()
    kind = str(kind_of_room_id)

    if name:
        room = filter(lambda tt: tt.name == name, room)

    if kind_of_room_id:
        room = list(filter(lambda tt: tt.KindOfRoom.name == kind, room))

    if status:
        room = filter(lambda tt: tt.status.value == status, room)

    return room

