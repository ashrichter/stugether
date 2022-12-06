def get_weekly_health_averages(health_data):
    """ Calculates weekly averages of health, steps and sleep for given data from a week.

    :param health_data: queryset of health data for a week
    :return: dictionary of averages containing sleep, steps and water
    """
    total_sleep_for_week = 0
    total_steps_for_week = 0
    total_water_for_week = 0

    for i in health_data:
        total_sleep_for_week += i.sleep
        total_steps_for_week += i.steps
        total_water_for_week += i.water

    if len(health_data) != 0:
        sleep_in_format = seconds_to_day_hrs_min_sec(total_sleep_for_week / len(health_data))

        weekly_averages = {'sleep': sleep_in_format,  # list in format hours, min, sec
                           'steps': int(total_steps_for_week / len(health_data)),
                           'water': int(total_water_for_week / len(health_data)),
                           }
    else:
        weekly_averages = {'sleep': 'No data found',
                           'steps': 'No data found',
                           'water': 'No data found',
                           }

    return weekly_averages


def get_weekly_health_totals(health_data):
    """ Calculates weekly totals of health, steps and sleep for given data from a week.

    :param health_data: queryset of health data for a week
    :return: dictionary of totals containing sleep, steps and water
    """
    total_sleep_for_week = 0
    total_steps_for_week = 0
    total_water_for_week = 0

    for i in health_data:
        total_sleep_for_week += i.sleep
        total_steps_for_week += i.steps
        total_water_for_week += i.water

    weekly_totals = {'sleep': total_sleep_for_week,
                     'steps': total_steps_for_week,
                     'water': total_water_for_week,
                     }

    return weekly_totals


def date_diff_in_seconds(date_two, date_one):
    """ Calculate the amount of seconds between two dates.

    :param date_two: datetime end
    :param date_one: datetime start
    :return: difference between the two dates in seconds
    """
    timedelta = date_two - date_one
    return timedelta.days * 24 * 60 * 60 + timedelta.seconds


def seconds_to_day_hrs_min_sec(time):
    seconds_to_minute = 60
    seconds_to_hour = 60 * seconds_to_minute
    seconds_to_day = 24 * seconds_to_hour

    days = time // seconds_to_day
    time %= seconds_to_day

    hours = time // seconds_to_hour
    time %= seconds_to_hour

    minutes = time // seconds_to_minute
    time %= seconds_to_minute

    seconds = time

    # print("%d days, %d hours, %d minutes, %d seconds" % (days, hours, minutes, seconds))
    return [int(hours), int(minutes), int(seconds)]