import csv
from datetime import date

import requests
from bs4 import BeautifulSoup

from clean_journo import fixes


URL = 'https://www.tdcj.state.tx.us/death_row/dr_media_witness_list.html'

r = requests.get(URL)
try:
    r.raise_for_status()
except Exception as e:
    print('There was a problem: {}'.format(e))

table = BeautifulSoup(r.text, 'html.parser').find('table')

with open('tx-death-row-media-list.csv', 'w') as outfile:
    fields = ['execution_no', 'execution_date', 'journo_last',
              'journo_rest', 'journo_affiliation', 'inmate_no',
              'inmate_last', 'inmate_rest', 'url']

    writer = csv.DictWriter(outfile, fieldnames=fields)

    writer.writeheader()

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        execution_no = cells[0].string
        url = 'https://www.tdcj.state.tx.us/death_row/' + cells[1].a['href']
        inmate_last = cells[2].string
        inmate_rest = cells[3].string
        inmate_no = cells[4].string
        month, day, year = [int(x) for x in cells[5].string.split('/')]
        execution_date = date(year, month, day)
        media_list = [x.strip() for x in cells[6].string.split(';')
                      if x.strip()]
        for journo in media_list:
            for x in fixes:
                journo = journo.replace(x, fixes[x])
            journo_affiliation = journo.split(',')[1].strip()
            journo_name = journo.split(',')[0].strip()
            journo_rest, journo_last = journo_name.rsplit(' ', 1)
            writer.writerow({
                'execution_no': execution_no,
                'execution_date': execution_date,
                'journo_rest': journo_rest,
                'journo_last': journo_last,
                'journo_affiliation': journo_affiliation,
                'inmate_no': inmate_no,
                'inmate_rest': inmate_rest,
                'inmate_last': inmate_last,
                'url': url
            })
