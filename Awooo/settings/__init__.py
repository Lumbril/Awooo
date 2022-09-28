import os


if os.getenv("LEVEL") == "PROD":
    print('RUN PROD MODE')
    from .prod import *

else:
    print('RUN LOCAL MODE')
    from .local import *

from .base import *
