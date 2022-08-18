## Аналіз твітів з допомогою *Twint*

## USEFULL DISCUSSION https://github.com/twintproject/twint/issues/1111
## [рішення проблеми](https://github.com/twintproject/twint/issues/1253#issuecomment-913055717

from config_dir import my_dir # first, set paths to my directories
from twint_ops import twint_query_pars, twint_cli, twint_api, twint_read_csv

#### SET TWINT QUERY PARAMETERS

tw = twint_query_pars()

#### RUN QUERY VIA CLI

import os

tw_run_str = twint_cli(tw)
#os.system(tw_run_str) # uncomment if necessary

#### RUN QUERY VIA API

#twit_num = twint_api(tw) # uncomment if necessary

#### TWINT QUERY RESULT PROCESSING

twint_df = twint_read_csv(my_dir['data'] + tw['output_name'],encode=True,
                          del_empty_cols=True)
