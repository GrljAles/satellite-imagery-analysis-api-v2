from datetime import datetime

def get_dates_between_two_dates(starting_date, ending_date, date_list):
    """
    Returns list of dates between timeserise endig and starting dates from available dates in provided list.
    Parameters:
        starting_date (str): YYYYMMDD date string of the first date.
        ending_date (str): YYYYMMDD date string of the last date.
        date_list (list): List of available dates to pick from. Dates are YYYYMMDD strings.
    
    """
    starting_dateobj = datetime.strptime(starting_date, "%Y%m%d")
    ending_dateobj = datetime.strptime(ending_date, "%Y%m%d")

    valid_dates_list = []
    for date_string in date_list:
        date_obj = datetime.strptime(date_string, "%Y%m%d")
        if starting_dateobj <= date_obj <= ending_dateobj:
            valid_dates_list.append(date_string)
    return valid_dates_list
    
if __name__ == "__main__":
    pass