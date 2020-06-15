"""
Project Constants.
"""

import os

from pathlib import Path
from dotenv import find_dotenv, load_dotenv

# find .env.sample automagically by walking up directories until it's found, then
# load up the .env.sample entries as environment variables
_DOTENV_PATH = Path(find_dotenv())
load_dotenv(_DOTENV_PATH)

LOGGER_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_ENV_JSON_COMPRESS_LVL: str = 'JSON_COMPRESS_LVL'
_ENV_OVERWRITE_INTERIM_DATA: str = 'OVERWRITE_INTERIM_DATA'
_ENV_OVERWRITE_PROCESSED_DATA: str = 'OVERWRITE_PROCESSED_DATA'
_ENV_WORD_CLOUD_FONT_PATH: str = 'WORD_CLOUD_FONT_PATH'

PROJECT_DIR = _DOTENV_PATH.parents[0]
DATA_DIR = PROJECT_DIR / 'data'

EXTERNAL_DATA_DIR = DATA_DIR / 'external'
RAW_DATA_DIR = DATA_DIR / 'raw'
INTERIM_DATA_DIR = DATA_DIR / 'interim'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
MODEL_DIR = DATA_DIR / 'model'

REFERENCES_DIR = PROJECT_DIR / 'references'
REPORTS_DIR = PROJECT_DIR / 'reports'

RELATIONSHIP_CSV_FILENAME = 'character_relationships.csv'
TEXT_STATS_CSV_FILENAME = 'book_textstats.csv'
CENTRALITY_CSV_FILENAME = 'Centralities {}.csv'

FORCE_INTERIM_SAVE: bool = os.getenv(_ENV_OVERWRITE_INTERIM_DATA).lower() in ['true', '1', 'yes']
FORCE_PROCESSED_SAVE: bool = os.getenv(_ENV_OVERWRITE_PROCESSED_DATA).lower() in ['true', '1', 'yes']

JSON_COMPRESS_LVL: int = int(os.getenv(_ENV_JSON_COMPRESS_LVL)) if os.getenv('%s' % _ENV_JSON_COMPRESS_LVL) else 9

CSV_CHAR_MENT: str = 'mentions'
CSV_CHAR_HITS: str = 'hits'
CSV_CHAR_IMPR: str = 'importance'
CSV_CHAR_SRC: str = 'source'
CSV_CHAR_TRG: str = 'target'
CSV_CHAR_BOOK: str = 'book'

CENT_CSV_TR: str = 'text_rank'
CENT_CSV_OTR: str = 'own_text_rank'
CENT_CSV_EV: str = 'eigenvector'
CENT_CSV_OEV: str = 'own_eigenvector'
CENT_CSV_DEG: str = 'degree'
CENT_CSV_CLSNS: str = 'closeness'
CENT_CSV_HARM: str = 'harmonic'
CENT_CSV_BTWN: str = 'betweenness'
CENT_CSV_KATZ: str = 'katz'
CENT_CSV_OKATZ: str = 'own_katz'
CENT_CSV_HITS: str = 'hits'
CENT_CSV_ID: str = 'label'

# Golden ratio
PHI = (1 + 5 ** 0.5) / 2  # https://en.wikipedia.org/wiki/Golden_ratio
# mm to inch conversion factor
MM_TO_INCH = 1 / 25.4  # https://en.wikipedia.org/wiki/Inch

WORD_CLOUD_FONT_PATH: str = os.getenv(_ENV_WORD_CLOUD_FONT_PATH)
