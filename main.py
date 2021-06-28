import json
import pandas as pd

def callings_parse(callings):
    return ', '.join(
        [c.replace('<span class="custom-report-position">', '')
         for c in callings.split('</span>')][:-1]
    )

COLUMN_FUNCTIONS = {'CALLINGS': callings_parse}

def read_lcr_report(filepath):

    f = open(filepath)
    data = json.load(f)
    f.close()

    columns = [c['key'] for c in data['columns']]
    dfData = []
    for member in data['members']:
        dfData.append([
            COLUMN_FUNCTIONS[c](member[c]) if c in
            COLUMN_FUNCTIONS.keys() else member[c] for c in columns
        ])

    df = pd.DataFrame(dfData, columns=columns)
    df.to_csv(filepath.replace('.json', '.csv'))

if __name__ == '__main__':
    read_lcr_report('recent_converts_24_months/20210627.json')

