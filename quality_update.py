from pychord import QualityManager
from pychord.constants.qualities import DEFAULT_QUALITIES
from data_util import SCALE_PALLETTE_VAL_DICT, MATCHES_DICT

# TO DO: Do this shit 
UPDATED_DEFAULT_QUALITIES = set()

for i in MATCHES_DICT.keys():
    if i not in DEFAULT_QUALITIES:
        UPDATED_DEFAULT_QUALITIES.add(i)

for i in UPDATED_DEFAULT_QUALITIES:
    print(i)