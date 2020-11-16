import asyncio
from asgiref.sync import async_to_sync
from api.action_play import *


asyncio.get_event_loop().run_until_complete(start_ws())
