import os

from dotenv import load_dotenv

load_dotenv()

if os.getenv("LEVEL") == "PROD":
    print('RUN PROD MODE')
    from .prod import *

else:
    print('RUN LOCAL MODE')
    from .local import *

from .base import *
