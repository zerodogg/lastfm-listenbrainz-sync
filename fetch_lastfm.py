#!.venv/bin/python

import datetime
import itertools
import os
import re
import tqdm
from constants import LASTFM_DATA_ROOT
from config import lastfm_first_scrobble_date
from utils import (
    create_lastfm_data_root,
    get_db_con,
    fetch_lastfm_date
)


create_lastfm_data_root()

today = datetime.date.today()

last_fetched_date = max(
    itertools.chain(
        map(
            lambda x: datetime.date.fromisoformat(re.sub(r'\.json$', '', x)),
            os.listdir(LASTFM_DATA_ROOT)
        ),
        [datetime.date.fromisoformat(lastfm_first_scrobble_date)]
    )
)

db_con = get_db_con()

total_days = (today - last_fetched_date).days + 1

progress_bar = tqdm.tqdm(total=total_days)

while last_fetched_date <= today:
    fetch_lastfm_date(db_con, last_fetched_date)
    last_fetched_date += datetime.timedelta(days=1)
    progress_bar.update(n=1)

progress_bar.close()