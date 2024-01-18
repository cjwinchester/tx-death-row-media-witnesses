# Texas death row media witnesses

[Some Python](scrape.py) to scrape and reshape [a table of data](https://www.tdcj.state.tx.us/death_row/dr_media_witness_list.html) on journalists who witness executions in Texas.

The script attempts some typo correction (`fixes.py`) and flattens the data into a tidy CSV in which each record is one journalist's witness of a single execution (e.g., five witnesses at an execution = five rows).