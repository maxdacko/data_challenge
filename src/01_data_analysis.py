from helpers.load_datasets import load_datasets
from helpers.convert_dates import convert_dates
from helpers.calculate_next_payment_day import calculate_next_payment_day
from helpers.calculate_next_payment_day_sum_week import calculate_next_payment_day_sum_week


def analyze_discrepancies(allowance_events, allowance_backend, payment_schedule):
    """
    Identifies discrepancies between calculated and expected payment details
    Args:
        allowance_events (DataFrame): Event data that we use as a SOT
        allowance_backend (DataFrame): Allowance Backend data which we suspect have discrepancies.
        payment_schedule (DataFrame): Payment Schedule data which we also suspect have discrepancies.
    Returns:
        backend_discrepancies (DataFrame): Rows where calculated next payment day 
                                           differs from the backend data for enabled status.
        schedule_discrepancies (DataFrame): Rows with mismatches in payment dates or 
                                            multiple active records for the same user.
        period_frequency_discrepancies (DataFrame): Rows with mismatches in scheduled 
                                                    frequency or day compared to backend data.
    """
    allowance_events['calculated_next_payment_day'] = allowance_events.apply(calculate_next_payment_day, axis=1)

    merged_backend = allowance_backend.merge(
        allowance_events, 
        left_on='uuid', 
        right_on='user.id', 
        how='left', 
        suffixes=('_backend', '_events')
    )

    backend_discrepancies = merged_backend[  
        (merged_backend['next_payment_day'] != merged_backend['calculated_next_payment_day']) &
        (merged_backend['status'] == 'enabled')
    ] 

    # as there are multiple rows for each user.id, i sorted the rows by event.timestamp in descending order and dropped the duplicates, keeping only the newest row for each user.id
    backend_discrepancies = backend_discrepancies.sort_values('event.timestamp', ascending=False).drop_duplicates(subset=['user.id'], keep='first')

    merged_schedule = payment_schedule.merge(
        allowance_backend, 
        left_on='user_id', 
        right_on='uuid', 
        how='left'
    )

    schedule_discrepancies = merged_schedule[
        ((merged_schedule['payment_date'] != merged_schedule['next_payment_day']) |
        (merged_schedule.duplicated(subset=['user_id'], keep=False))) &
        ((merged_schedule['status'] == 'enabled'))
    ]

    period_frequency_discrepancies = merged_backend[
        ((merged_backend['allowance.scheduled.frequency'] != merged_backend['frequency']) |
        (merged_backend['allowance.scheduled.day'] != merged_backend['day'])) &
        ((merged_backend['status'] == 'enabled'))
    ]

    period_frequency_discrepancies = period_frequency_discrepancies.sort_values('event.timestamp', ascending=False).drop_duplicates(subset=['user.id'], keep='first')

    return backend_discrepancies, schedule_discrepancies, period_frequency_discrepancies

def analyze_discrepancies_sum_week(allowance_events, allowance_backend):
    """
    Same as before but adding a week, this because there are cases when if you add a week, 
    the next payment day is correct, so im not sure the logic behind payments.
    Args:
        allowance_events (DataFrame): Event data that we use as a SOT
        allowance_backend (DataFrame): Allowance Backend data which we suspect have discrepancies.
        payment_schedule (DataFrame): Payment Schedule data which we also suspect have discrepancies.
    Returns:
        backend_discrepancies_sum_week (DataFrame): Rows where calculated next payment day 
                                           differs from the backend data for enabled status.
    """

    allowance_events['calculated_next_payment_day'] = allowance_events.apply(calculate_next_payment_day_sum_week, axis=1)

    merged_backend = allowance_backend.merge(
        allowance_events, 
        left_on='uuid', 
        right_on='user.id', 
        how='left', 
        suffixes=('_backend', '_events')
    )

    backend_discrepancies = merged_backend[
        (merged_backend['next_payment_day'] != merged_backend['calculated_next_payment_day']) &
        (merged_backend['status'] == 'enabled')
    ]

    backend_discrepancies_sum_week = backend_discrepancies.sort_values('event.timestamp', ascending=False).drop_duplicates(subset=['user.id'], keep='first')

    return backend_discrepancies_sum_week

def save_discrepancies_to_csv(backend_discrepancies_sum_week, backend_discrepancies, schedule_discrepancies, period_frequency_discrepancies):
    """
    Saves identified discrepancies into separate CSV files for further analysis.
    Args:
        backend_discrepancies_sum_week (DataFrame): Discrepancies when adding a week.
        backend_discrepancies (DataFrame): General discrepancies.
        schedule_discrepancies (DataFrame): Discrepancies between schedule next payment and allwance backend next payment.
        period_frequency_discrepancies (DataFrame): Frequency or day-related mismatches.
    """
    backend_discrepancies_sum_week.to_csv("data/output/backend_discrepancies_sum_week.csv", index=False)
    backend_discrepancies.to_csv("data/output/backend_discrepancies.csv", index=False)
    schedule_discrepancies.to_csv("data/output/schedule_discrepancies.csv", index=False)
    period_frequency_discrepancies.to_csv("data/output/period_frequency_discrepancies.csv", index=False)

if __name__ == "__main__":
    """
    Main execution flow:
    - Loads datasets.
    - Converts date fields into standard formats.
    - Analyzes discrepancies in backend data and payment schedules.
    - Saves the results to CSV files for review.
    """
    allowance_events, allowance_backend, payment_schedule = load_datasets()

    allowance_backend, allowance_events = convert_dates(allowance_backend, allowance_events)

    backend_discrepancies, schedule_discrepancies, period_frequency_discrepancies = analyze_discrepancies(
        allowance_events, allowance_backend, payment_schedule
    )

    backend_discrepancies_sum_week= analyze_discrepancies_sum_week(
        allowance_events, allowance_backend
    )

    save_discrepancies_to_csv(backend_discrepancies_sum_week, backend_discrepancies, schedule_discrepancies,  period_frequency_discrepancies)

    print("Discrepancy reports generated and saved as CSV files!")
