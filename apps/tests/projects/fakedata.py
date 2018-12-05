from datetime import date, datetime, timedelta


date_1 = date.today()
date_2 = date_1 + timedelta(days=10)

test_project ={
    'prudent_number' : '103.411',
    'penndot_number' : 'E01994',
    'name' : 'Septa bridge over mars',
    'inspector' : None,
    'office' : 'King of Prussia',
    'start_date' : date_1,
    'end_date' : date_2,
    'st_hours' : 300,
    'ot_hours' : 25,
    'payroll_budget' : 132000,
    'other_cost_budget' : 10000,
}
