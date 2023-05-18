from datetime import datetime
from dotenv import load_dotenv
import os

import pytz

load_dotenv()


timezone = os.environ.get('TIMEZONE')
class DateHelper:
    
    def get_date(self):
        sa_timezone = pytz.timezone(timezone)
        local_date = datetime.now().astimezone(sa_timezone)
        return local_date