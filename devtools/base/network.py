from common.id_generator import next_id


async def network_enable(session):
    id = next_id()
    message = {
        "id": id,
        "method": "Network.enable",
        "params": {}
    }
    if not session.is_connected():
        await session.connect()
    await session.send_message(message)


async def network_disable(session):
    id = next_id()
    message = {
        "id": id,
        "method": "Network.disable",
        "params": {}
    }
    if not session.is_connected():
        await session.connect()
    await session.send_message(message)
