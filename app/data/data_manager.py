from pathlib import Path
import pandas as pd
from datatable import dt

class DataManager:
    folder = Path.cwd().joinpath('data')
    files = list(folder.glob('*.csv'))
    total_data = list(dt.iread(files,encoding='utf-8'))

