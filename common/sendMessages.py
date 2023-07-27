from Database.databaseConfig import *
from Database.databaseConfig import websockets, test 

import asyncio



async def send_to_all(_from, toUser, message, toto,type,MessageData):
    
    if type == "message":
        data = {"Type": "Group", "from": _from, "to": toUser,
                "Message": message, "task": "onMessage","type_":type}
    else:
        data = {"Type": "Group", "from": _from, "to": toUser,
                "Message": message, "task": "onMessage","type_":type,"fileurl":MessageData['fileurl']}

    # history.append(data)
    # if len(history) > 2:
    #     del history[:1]

    tasks = set()

    for groupMember in toto:
        for ws in websockets:
            try:    
                if ws == test[_from]:
                    pass
                elif ws == test[groupMember]:
                    tasks.add(asyncio.create_task(ws.send_json(data)))
                    while tasks:
                        done, tasks = await asyncio.wait(tasks)
            except KeyError:
                pass


# Sending Private message to the User
async def send_to_user(_frm, to, user, message, type_, MessageData,date_time):
    if type_ == "message":
        data = {"Type": "Private", "from": _frm, "to": to,"Message": message, "task": "onMessage","type_":"message","time":date_time[0],"date":date_time[1]}
        txt = "message from" + _frm
        flash_message = {"task": "flash", "alertMessage": txt}
        # await user.send_str(data)
        await user.send_json(data)
        await test[to].send_json(flash_message)
    else:
        data = {"Type": "Private", "from": _frm, "to": to,"Message": message, "task": "onMessage","type_":"file","fileurl":MessageData['fileurl'],"time":date_time[0],"date":date_time[1]}
        txt = "message from" + _frm
        flash_message = {"task": "flash", "alertMessage": txt}
        # await user.send_str(data)=
        await user.send_json(data)
        await test[to].send_json(flash_message)