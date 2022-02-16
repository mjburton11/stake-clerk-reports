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

def set_apart_parse(callings, **kwargs):
    dateAndSetApart = sustained_parse(callings)
    return dateAndSetApart.split('/')[1]

COLUMN_FUNCTIONS = {'CALLINGS': callings_parse,
                    'CALLINGS_WITH_DATE_SUSTAINED': sustained_parse,
                    'CALLINGS_WITH_DATE_SUSTAINED_AND_SET_APART': set_apart_parse}

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

def read_all_quarterly_reports():
    files = os.listdir('quarterly_reports')

    data = {'ministering.brothers': [], 'ministering.sisters': []}

    for file in files:
      if ('ministering-sisters.csv' == file):
        continue
      read_quarterly_report('quarterly_reports' + os.sep + file, data)

    df = pd.DataFrame(data['ministering.sisters'])
    df.to_csv("quarterly_reports/ministering-sisters.csv")


UNIT_MAP = {
  174831: "ARL",
  174858: "BEL1",
  365750: "BEL2",
  44598: "CAM1",
  101621: "CAM2",
  145971: "CAM3",
  211699: "CAM4",
  1061666: "CRW",
  2064774: "KSW",
  378445: "LFP",
  75892: "MAW",
}


def read_quarterly_report(filename, totalData):

    f = open(filename)
    data = json.load(f)
    f.close()

    quarterName = filename.split('/')[-1].split('.json')[0]

    for section in data['sections']:
      if (section["nameResourceId"] == 'members.families'):
        for subsection in section['rows']:
          for dataKey in totalData.keys():
            if (subsection["nameResourceId"] == dataKey):
              for unit in subsection['childUnitRows']:
                unitData = {
                  "Date": quarterName,
                  "Unit": UNIT_MAP[unit["childUnitNumber"]],
                  "Interviewed": unit["actualValue"],
                  "Companionships": unit["potentialValue"]
                }
                totalData[dataKey].append(unitData)


if __name__ == '__main__':
    # read_lcr_report('recent_converts_24_months/20210706.json')
    # read_lcr_report('all_baptisms_24_months/20210706.json')
    # read_lcr_report('recent_stake_callings/20210714.json', list='one')
    # read_lcr_report('elders_quorum_presidencies/20211211.json', list='one')
    # read_lcr_report('all_baptisms_24_months/20211211.json')
    # read_lcr_report('ym_by_unit/20210906.json')
    # read_lcr_report('yw_by_unit/20210906.json')
    # read_lcr_report('all_sisters_by_birth_country/20210912.json')
    # read_lcr_report('ordinations_to_ratify/20210916.json')
    # read_lcr_report('all_members_by_birth_country/20210926.json')
    # read_lcr_report('stake_young_women/20220106.json')
    # read_lcr_report('stake_young_men/20220111.json')
    # read_lcr_report('expired_last_month/20220208.json')
    # read_lcr_report('exec_secretaries/20220111.json')
    # read_lcr_report('mission_languages/20220117.json')
    # read_lcr_report('spanish_speaking_rms/20220205.json')
    read_all_quarterly_reports()