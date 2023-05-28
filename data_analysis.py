from json import dumps
from io import BufferedReader

import pandas as pd


def analyze_excel(excel_file: BufferedReader):
    excel = pd.read_excel(excel_file)

    # total_data is a list wich will contain identically structured dict for each year from excel file
    total_data = []

    # Therefore we will run all of the years from excel one by one
    for i, year in enumerate(excel.Year.unique()):
        # Selecting current year with DataFrame where-like construction
        current_year = excel[excel['Year'] == year]

        # Adding simple-to-calculate data(there and later we wil use round due to the fact that data was requested rounded)
        total_data.append({
            'Year': round(year),
            'RealIncome': round(current_year.Income.sum()),
            'TargetIncome': round(current_year['Target Income'].sum()),
            'AverageIncome': round(current_year.Income.sum() / 12),
        })
        total_data[i]['IncomePercent'] = round(total_data[i]['RealIncome'] / total_data[i]['TargetIncome'] * 100)

        # pandas sort months alphabetically, so we will need to reindex(~sort) them in the right order
        right_months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # There we calculating monthly income in 2 steps
        # Aggregate income sum by months groups
        total_data[i]['ByMonths'] = current_year.loc[:, ['Month', 'Income']].groupby('Month').sum().reindex(right_months_order, axis=0)
        # And restructure it into a dict with rounding
        total_data[i]['ByMonths'] = {month[0]: round(month[1]) for month in total_data[i]['ByMonths'].to_dict()['Income'].items()}

        # IncomeSources is a list of similar objects where each one represents one income source
        items = []
        # Fiestly we will create each object and calculate counts of operations right away
        for counts in current_year.loc[:, ['Income sources', 'Counts']].groupby('Income sources').sum('Counts').to_dict()['Counts'].items():
            items.append({'Name': counts[0], 'QuantityPercentage': round(counts[1]/current_year.Counts.sum() * 100), 'Quantity': round(counts[1])})

        # Then we will calculate income and its income percentage for each income source
        current_year_income = current_year.Income.sum()
        for j, income in enumerate(current_year.loc[:, ['Income sources', 'Income']].groupby('Income sources').sum('Income').to_dict()['Income'].items()):
            items[j]['Income'] = round(income[1])
            items[j]['IncomePercentage'] = round(income[1]/current_year_income * 100)
        total_data[i]['Items'] = items  

        # Lastly we will add "source's children", they have parent-similar structure but without counts calculating
        for j, income_source in enumerate(current_year.loc[:, ['Income sources', 'Income Breakdowns', 'Income']].groupby('Income sources')):
            income_breakdowns = list(income_source[1].groupby('Income Breakdowns').sum('Income').to_dict()['Income'].items())
            items[j]['IncomeBreakdowns'] = []
            if not items[j]['Name'] == income_breakdowns[0][0]:
                for l in income_breakdowns:
                    items[j]['IncomeBreakdowns'].append({'Name': l[0], 'Income': round(l[1]), 'IncomePercentage': round(l[1]/current_year.Income.sum() * 100)})
        
        # Now we will calculate operations profits for all year
        total_data[i]['OperatingProfits'] = {}
        total_data[i]['OperatingProfits']['Total'] = round(current_year['operating profit'].sum())

        # And each month separately, not forgeting reindexing
        total_data[i]['OperatingProfits']['ByMonths'] = current_year.loc[:, ['Month', 'operating profit']].groupby('Month').sum().reindex(right_months_order, axis=0)
        total_data[i]['OperatingProfits']['ByMonths'] = {month[0]: round(month[1]) for month in total_data[i]['OperatingProfits']['ByMonths'].to_dict()['operating profit'].items()}

        # And lastly calculate marketing strategies abcolute and procentage income values
        total_data[i]['MarketingStrategies'] = {}
        for j in current_year.loc[:, ['Income', 'Marketing Strategies']].groupby('Marketing Strategies').sum('Income').to_dict()['Income'].items():
            total_data[i]['MarketingStrategies'][j[0]] = [round(j[1]), round(j[1] / current_year.Income.sum() * 100)]

    # Before returning, adding list of all included year
    json_res = {'Years': excel.Year.unique().tolist(), 'Datasets': total_data}
    # return as json due to the frontender's request
    return dumps(json_res, indent=4)
