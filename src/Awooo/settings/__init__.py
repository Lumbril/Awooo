import os

from dotenv import load_dotenv

load_dotenv()

if os.getenv("LEVEL") == "PROD":
    print('RUN PROD MODE')
    from .prod import *
elif os.getenv("LEVEL") == "LOCAL_PROD":
    print('RUN LOCAL PROD MODE')
    from .local_prod import *
else:
    print('RUN LOCAL MODE')
    from .local import *

from .base import *
