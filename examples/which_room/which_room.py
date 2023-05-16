from hldmodding import on, controller

@on.change.room.sub
def print_room_id():
    print(f'i am now in {controller.room_id.new} and was in {controller.room_id.old}')