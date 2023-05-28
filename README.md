# Financial data simple analize and backend api
___
## Installation
If you are using **linux** or **macOS**, you probably **already have** git and python
1. [Git](https://git-scm.com/)
2. [Python3.10+](https://www.python.org/downloads/)
___
### For linux and macOS:
Open **terminal** and run this command()
```
git clone https://github.com/GaganovAlexander/fin-stat-data-analize-backend &&
cd ./fin-stat-data-analize-backend &&
python3 -m venv venv &&
source ./venv/bin/activate &&
pip install -r requirements.txt
```
___
### For Windows:
Open **cmd** and run this commands one by one
```
git clone https://github.com/GaganovAlexander/fin-stat-data-analize-backend
cd ./fin-stat-data-analize-backend
python3 -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```
___
## Run
**Before running there and in test part you should always activate venv by running tis command in the project directory**
### For Windows
```
./venv/bin/activate.bat
```
### For linux and macOS
```
source ./venv/bin/activate
```
To run app use this command in project directory
```
gunicorn -b 127.0.0.1:8001 app:app
```
___
### To stop running
Make keyboard interrupt(press **ctrl+C** in the command line)
___
## Test
For tasting if everything is OK, you can run this from project directory while app is running
```
python3 ./test/test.py
```
On success you will create **test.json** file in the test/ directory and this file should be simmilar to correct_test.json file in the same directory

In there any other case, that means that you did something wrong from previous commands
___
## .json file from api structure
```
{
    "Years": [
        // It's a list of years as numbers, example: [2020, 2021]
        number,
    ],
    "Datasets": [
        // There will be one or multiple identically structured objects
        // in the order of the "Years" list
        {
            "Year": number,
            // here and below if you see a number with <, > or ~,
            // it represents usual amount
            "RealIncome": number, // >100k
            "TargetIncome": number, // >100k
            "AverageIncome": number, // ~100k
            "IncomePercent": number, // here and below percent(age) will be 0-100
            "ByMonths": {
                // contain all months incomes
                "monthName": number, // ~100k
            },
            "Items": [
                // There will be one or multiple identically structured objects
                {
                    "Name": string,
                    "QuantityPercentage": number,
                    "Quantity": number, // <100k
                    "Income": number, // ~100k 
                    "IncomePercentage": number, 
                    "IncomeBreakdowns": [
                        // There will be one or multiple identically structured objects
                        // if IncomeBreakdown name is identical to item name, there will be empty
                        {
                            "Name": string,
                            "Income": number, // ~10-100k
                            "IncomePercentage": number
                        },
                    ]
                },
            ],
            "OperatingProfits": {
                "Total": number, // >100k
                "ByMonths": {
                    "monthName": number, // ~10k
                }
            },
            "MarketingStrategies": {
                "B2B": [
                    number, // absolute value of income >100k
                    number // percentage value of income
                ],
                "B2C": [
                    // similar to B2B
                    number,
                    number
                ]
            }
        },
    ]
}
```