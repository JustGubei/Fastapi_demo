from api.log.models import Logs


async def write_to_database(record):
    await Logs.create(**record)
