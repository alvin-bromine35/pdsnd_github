import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to explore? Chicago, New York City or Washington?\n')
        city = city.lower()

        if city not in ('chicago','new york city', 'washington'):
            print('Invalid input. Please enter a valid input!')
        else:
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("Please type in the desired month from January-June. If you want to explore the data of the the first six months, please type ALL.\n")
        month = month.lower()

        if month not in ('january', 'february','march','april','may','june','all'):
            print('Invalid input. Please enter a valid input!')
        else:
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please type in the desired day. If you want to explore the data of the whole week, please type ALL.\n")
        day = day.lower()

        if day not in ('sunday', 'monday','tuesday','wednesday','friday','saturday','all'):
            print('Invalid input. Please enter a valid input!')
        else:
            break
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

     # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays time related statistics."""

    print('\nTIME RELATED STATISTICS:\n')

    df['month'] = df['Start Time'].dt.month_name()

    print("The most common month is {}.\n".format(df['month'].mode()[0]))

    # display the most common day of week
    print("The most common day of week is {}.\n".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.strftime('%H').add(':00')

    print("The most common start hour is {} hh:mm.\n".format(df['hour'].mode()[0]))

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nSTATION RELATED STATISTICS:\n')

    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]
    number_of_times_start = df['Start Station'].value_counts().max()
    print("The most commonly used start station is {}.\n".format(most_commonly_used_start_station))
    print("Number of times {} has been used as start station is {}.\n".format(most_commonly_used_start_station,number_of_times_start))

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]
    number_of_times_end = df['End Station'].value_counts().max()
    print("The most commonly used end station is {}.\n".format(most_commonly_used_end_station))
    print("Number of times {} has been used as end station is {}.\n".format(most_commonly_used_end_station,number_of_times_end))

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station trip is: ", df['combination'].mode()[0])

    #display the top 10 start and end station
    top10_start_station = df['Start Station'].value_counts().head(10)
    top10_end_station = df['End Station'].value_counts().head(10)
    print('\nTop 10 Start Station:\n')
    print(top10_start_station)
    print('\nTop 10 End Station:\n')
    print(top10_end_station,'\n')
    print('-'*40)

def readable_timedelta(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "{} hours : {} minutes : {} seconds".format(hour,minutes,seconds)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTRIP DURATION STATISTICS:\n')

    # total travel hours
    seconds = int(df['Trip Duration'].sum())
    print("Total trip duration:")
    print(readable_timedelta(seconds),"\n")

    # Average trip duration
    seconds = int(df['Trip Duration'].mean())
    print("Average trip duration:")
    print(readable_timedelta(seconds),'\n')
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nUSER RELATED STATISTICS:\n')

    # Display counts of user types
    print('User Type Distribution:\n')
    user_type = df['User Type'].value_counts()
    print(user_type, "\n")

    if city != 'washington':
        # Display counts of gender
        print('Gender Distribution:\n')
        gender = df['Gender'].value_counts()
        print(gender)

        # Display earliest, most recent, and most common year of birth
        most_recent = int(df['Birth Year'].max())
        earliest_year = int(df['Birth Year'].min())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth is {}.\n".format(earliest_year))
        print("The most recent year of birth is {}.\n".format(most_recent))
        print("The most common year of birth is {}.\n".format(most_common_year))

def rawdata(df):
    x = 0
    while True:
        raw_data = input('\nDo you like to view the data? Enter yes or no.\n')
        if raw_data.lower() == 'yes':
            pd.set_option('display.max_columns',200)
            print('\n')
            print(df[x:x + 5])
            x +=5
        elif raw_data.lower() == 'no':
            break
        else:
            print('Invalid input. Please enter a valid input!')
    return raw_data

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data = rawdata(df)

        restart = input('Would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
