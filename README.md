# Texas death row media witnesses

A Python script, `scraper.py`, to scrape and reshape [a table of data](https://www.tdcj.state.tx.us/death_row/dr_media_witness_list.html) on journalists who witness executions in Texas. Dependencies (`requests`, `bs4`) are managed with [pipenv](https://docs.pipenv.org/).

The script attempts some typo correction (`clean_journo.py`) and flattens the data into a CSV where each record is one journalist's witness of a single execution (e.g., 5 witnesses at an execution = 5 records).