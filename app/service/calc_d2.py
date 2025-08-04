from datetime import datetime, timedelta

def get_filtered_dates(reference_date=None):
    if reference_date and isinstance(reference_date, str):
        reference_date = datetime.fromisoformat(reference_date)

    today = reference_date or datetime.today()
    weekday = today.weekday() 
    filtered_dates = []

    if weekday == 0:  # Segunda
        target_date = today - timedelta(days=4)
        filtered_dates.append(target_date)
    elif weekday == 1:  # Terça
        for delta in [4, 3, 2]: 
            filtered_dates.append(today - timedelta(days=delta))
    elif weekday == 2:  # Quarta
        target_date = today - timedelta(days=2)
        filtered_dates.append(target_date)
    elif weekday == 3:  # Quinta
        target_date = today - timedelta(days=2)
        filtered_dates.append(target_date)
    elif weekday == 4:  # Sexta
        target_date = today - timedelta(days=2)
        filtered_dates.append(target_date)
    else:
        return
    return [date.strftime("%Y-%m-%d") for date in filtered_dates]

#get_filtered_dates("2025-08-05")