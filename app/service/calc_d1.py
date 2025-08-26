from datetime import datetime, timedelta

def get_filtered_dates(reference_date=None):
    if reference_date and isinstance(reference_date, str):
        reference_date = datetime.fromisoformat(reference_date)

    today = reference_date or datetime.today()
    target_date = today - timedelta(days=1)

    return [target_date.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]]
    #return ['2024-04-14 18:11:00.000']

def get_dates_reminder(day):
    dt_str = get_filtered_dates()[0]
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
    
    dt_new = dt + timedelta(days=day)
    
    return int(dt_new.timestamp())
#get_filtered_dates("2025-08-05")