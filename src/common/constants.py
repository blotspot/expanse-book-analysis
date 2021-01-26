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

_ENV_JSON_COMPRESS_LVL = 'JSON_COMPRESS_LVL'
_ENV_OVERWRITE_INTERIM_DATA = 'OVERWRITE_INTERIM_DATA'
_ENV_OVERWRITE_PROCESSED_DATA = 'OVERWRITE_PROCESSED_DATA'
_ENV_WORD_CLOUD_FONT_PATH = 'WORD_CLOUD_FONT_PATH'

PROJECT_DIR = _DOTENV_PATH.parents[0]
DATA_DIR = PROJECT_DIR / 'data'

EXTERNAL_DATA_DIR = DATA_DIR / 'external'
RAW_DATA_DIR = DATA_DIR / 'raw'
MODEL_DATA_DIR = DATA_DIR / 'model'
INTERIM_DATA_DIR = DATA_DIR / 'interim'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

MODEL_DIR = PROJECT_DIR / 'models'
REFERENCES_DIR = PROJECT_DIR / 'references'
REPORTS_DIR = PROJECT_DIR / 'reports'

RELATIONSHIP_CSV_FILENAME = 'character_relationships.csv'
TEXT_STATS_CSV_FILENAME = 'book_textstats.csv'
CENTRALITY_CSV_FILENAME = 'Centralities {}.csv'

FORCE_INTERIM_SAVE = os.getenv(_ENV_OVERWRITE_INTERIM_DATA).lower() in ['true', '1', 'yes']
FORCE_PROCESSED_SAVE = os.getenv(_ENV_OVERWRITE_PROCESSED_DATA).lower() in ['true', '1', 'yes']

JSON_COMPRESS_LVL = int(os.getenv(_ENV_JSON_COMPRESS_LVL)) if os.getenv('%s' % _ENV_JSON_COMPRESS_LVL) else 9

CSV_CHAR_MENT = 'mentions'
CSV_CHAR_HITS = 'hits'
CSV_CHAR_IMPR = 'importance'
CSV_CHAR_SRC = 'source'
CSV_CHAR_TRG = 'target'
CSV_CHAR_BOOK = 'book'

CENT_CSV_TR = 'text_rank'
CENT_CSV_OTR = 'own_text_rank'
CENT_CSV_EV = 'eigenvector'
CENT_CSV_OEV = 'own_eigenvector'
CENT_CSV_DEG = 'degree'
CENT_CSV_CLSNS = 'closeness'
CENT_CSV_HARM = 'harmonic'
CENT_CSV_BTWN = 'betweenness'
CENT_CSV_KATZ = 'katz'
CENT_CSV_OKATZ = 'own_katz'
CENT_CSV_HITS = 'hits'
CENT_CSV_ID = 'label'

# Golden ratio
PHI = (1 + 5 ** 0.5) / 2  # https://en.wikipedia.org/wiki/Golden_ratio
# mm to inch conversion factor
MM_TO_INCH = 1 / 25.4  # https://en.wikipedia.org/wiki/Inch

WORD_CLOUD_FONT_PATH = os.getenv(_ENV_WORD_CLOUD_FONT_PATH)
