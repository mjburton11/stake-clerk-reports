import json
import os
import pandas as pd

def callings_parse(callings, list='all', **kwargs):
    callings = [c.replace('<span class="custom-report-position">', '')
         for c in callings.split('</span>')][:-1]
    if list == 'one':
        return callings[0]
    else:
        return ', '.join(callings)

def sustained_parse(callings, **kwargs):
    callings = callings_parse(callings, list='one')
    return callings.split('(')[-1].replace(')', '')

COLUMN_FUNCTIONS = {'CALLINGS': callings_parse,
                    'CALLINGS_WITH_DATE_SUSTAINED': sustained_parse}

def read_lcr_report(filepath, **kwargs):

    csv_filename = filepath.replace('.json', '.csv')

    if os.path.exists(csv_filename):
        os.remove(csv_filename)

    f = open(filepath)
    data = json.load(f)
    f.close()

    columns = [c['key'] for c in data['columns']]
    dfData = []
    for member in data['members']:
        dfData.append([
            COLUMN_FUNCTIONS[c](member[c], **kwargs) if c in
            COLUMN_FUNCTIONS.keys() else member[c] for c in columns
        ])

    df = pd.DataFrame(dfData, columns=columns)
    df.to_csv(csv_filename)

if __name__ == '__main__':
    # read_lcr_report('recent_converts_24_months/20210706.json')
    # read_lcr_report('all_baptisms_24_months/20210706.json')
    read_lcr_report('recent_stake_callings/20210714.json', list='one')

