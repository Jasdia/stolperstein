from asyncio import get_event_loop
from api.action_play import *

get_event_loop().run_until_complete(start_ws())
