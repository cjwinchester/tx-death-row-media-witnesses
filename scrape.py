import csv
from datetime import datetime
from urllib.parse import urljoin

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

from fixes import journo_fixes


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


URL = 'http://www.tdcj.state.tx.us/death_row/dr_media_witness_list.html'

CSV_FILE = 'tx-death-row-media-list.csv'

CSV_HEADERS = [
    'execution_number',
    'execution_date',
    'journalist_name_last',
    'journalist_name_rest',
    'journalist_affiliation',
    'inmate_number',
    'inmate_name_last',
    'inmate_name_rest',
    'url'
]

r = requests.get(URL, verify=False)
r.raise_for_status()

table = BeautifulSoup(r.text, 'html.parser').find('table')

with open(CSV_FILE, 'w', newline='', encoding='utf-8') as outfile:

    writer = csv.DictWriter(outfile, fieldnames=CSV_HEADERS)

    writer.writeheader()

    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')

        execution_no = cells[0].text.strip()

        link = cells[1].a.get('href')

        url = "" if not link else urljoin(URL, link)

        inmate_last = cells[2].text.strip()
        inmate_rest = cells[3].text.strip()
        inmate_no = cells[4].text.strip()

        execution_date = datetime.strptime(
            cells[5].text.strip(),
            '%m/%d/%Y'
        ).date().isoformat()

        media_list = [x.strip() for x in cells[6].string.split(';') if x.strip()]  # noqa

        for journo in media_list:

            journo = journo_fixes.get(journo, journo)

            try:
                journo_affiliation = journo.rsplit(',', 1)[1].strip()

                journo_name = journo.split(',')[0].strip()
                journo_rest, journo_last = journo_name.rsplit(' ', 1)

            except IndexError:
                journo_last = journo
                journo_rest = None
                journo_affiliation = None

            writer.writerow({
                'execution_number': execution_no,
                'execution_date': execution_date,
                'journalist_name_last': journo_last,
                'journalist_name_rest': journo_rest,
                'journalist_affiliation': journo_affiliation,
                'inmate_number': inmate_no,
                'inmate_name_last': inmate_last,
                'inmate_name_rest': inmate_rest,
                'url': url
            })

    print(f'Wrote {CSV_FILE}')
