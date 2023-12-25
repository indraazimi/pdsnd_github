import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york, washington)
    while True:
        print('\nWould you like to see data for Chicago, New York, or Washington?')
        city = input().lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city.')

    # get user input for time filter (month, day, both, or none)
    while True:
        print('\nWould you like to filter the data by month, day, both, or not at all?')
        print('Type "none" for no time filter.')
        filter = input().lower()
        if filter == 'both':
            break
        elif filter == 'month':
            day = 'all'
            break
        elif filter == 'day':
            month = 'all'
            break
        elif filter == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            print('Invalid time filter.')

    # get user input for month (january, february, ... june)
    while filter == 'month' or filter == 'both':
        print('\nWhich month - January, February, March, April, May, or June?')
        month = input().lower()
        if month in VALID_MONTHS:
            break
        else:
            print('Invalid month.')

    # get user input for day of week (monday, tuesday, ... sunday)
    while filter == 'day' or filter == 'both':
        print('\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?')
        day = input().lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        month = VALID_MONTHS.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def show_stats_footer(timelapse):
    """
    Displays how long a statistic calculation took place and divider

    Args:
        (float) timelapse - how long a statistic calculation took place
    """
    print("\nThis took %.6f seconds." % timelapse)
    print('-'*40)


def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) month - name of the month filter, or "all" if no month filter
        (str) day - name of the day filter, or "all" if no day filter
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, if data not filtered by month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        month_name = VALID_MONTHS[popular_month-1].title()
        print('Most popular month:', month_name)

    # display the most common day of week, if data not filtered by day
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('Most popular day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_hour)

    show_stats_footer(time.time() - start_time)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' -> ' + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print('Most popular trip:', popular_trip)

    show_stats_footer(time.time() - start_time)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time: {:,} seconds'.format(total_time))

    # display mean travel time
    average_time = df['Trip Duration'].mean()
    print('Average travel time: {:.2f} seconds/trip'.format(average_time))

    show_stats_footer(time.time() - start_time)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        print()
        gender = df['Gender'].value_counts()
        print(gender.to_string())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest birth year:', int(df['Birth Year'].min()))
        print('Most recent birth year:', int(df['Birth Year'].max()))
        print('Most common birth year:', int(df['Birth Year'].mode()[0]))

    show_stats_footer(time.time() - start_time)


def revert_data(df):
    """
    Reverts DataFrame to original data by deleting previously added columns.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    # These columns added when data is loaded from CSV
    df.pop('month')
    df.pop('day_of_week')

    # This column added when time stats is calculated
    df.pop('hour')

    # This column added when station stats is calculated
    df.pop('trip')


def show_raw_data(df):
    """
    Shows raw data, 5 rows at a time, if user wants it.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    # Reverts DataFrame to original data by deleting previously added columns
    revert_data(df)

    # Asks user if he/she wants to see raw data
    index = 0
    while True:
        if index == 0:
            print('\nWould you like to see the raw data? Enter yes or no.')
        else:
            print('\nWould you like to see next raw data? Enter yes or no.')

        choice = input().lower()
        if choice == 'yes':
            nextIndex = min(index+5, df.shape[0])
            print('\nShowing {} to {} of {} entries.'.format(index+1, nextIndex, df.shape[0]))

            for i in range(index, nextIndex):
                print()
                print(df.iloc[i].to_string())
            
            print("\n" + '-'*40)

            if nextIndex < df.shape[0]-1:
                index = nextIndex
            else:
                break
        elif choice == 'no':
            break
        else:
            print('Invalid choice.')


def main():
    try:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df, month, day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            show_raw_data(df)

            print('\nWould you like to restart? Enter yes or no.')
            restart = input().lower()
            if restart == 'yes':
                print("\n" + '='*40 + "\n")
            elif restart == 'no':
                print('\nGood bye.')
                break
            else:
                print('\nSeems like you don\'t want to restart.. Bye.')
                break
    except (KeyboardInterrupt):
        print('\n\nBye.')


if __name__ == "__main__":
	main()
