# This Python code analyzes data from one of 3 files:
# 1. washington.csv
# 2. new_york_city.csv
# 3. chicago.csv
#
# The user is initially asked to filter the data by: city, month
# and day - then statistics such as most popular start station,
# gender usage ratios and average trip time are returned.
################################################################

import pandas as pd
import time
import numpy as np

# Define filters:

def get_filters():
    # City:
    city=input("What city would you prefer? ").lower()
    city_list=['chicago', 'washington', 'new york city']
    while city not in city_list:
        print("Incorrect - please choose again")
        city=input("What city are you interested in? ").lower()

    # Month:
    month=input("What month are you interested in? ").lower()
    month_list=['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    while month not in month_list:
        print("Not a month - choose again")
        month=input("What month are you interested in? ").lower()

    # Day:
    day=input("What day of the week are you interested in? ").lower()
    day_list=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while day not in day_list:
        print("Invalid - choose again")
        day=input("What day of the week are you interested in? ").lower()

    print("\n You have chosen to filter by: \n City: {}\n Month: {}\n Day: {}\n".format(city.title(), month.title(), day.title()))
    return city, month, day

# Load data according to the filters:
def load_data(city, month, day):
    filename=("{}.csv".format(city).replace(" ","_"))
    df=pd.read_csv(filename)

# Now that we have the data frame for the selected city,
# extract the month and day from the 'Start Time' column
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month_start'] = df['Start Time'].dt.month
    df['day_start'] = df['Start Time'].dt.weekday
    return df

# Display statistics on the most frequent times of travel
def time_stats(df):
    # Display the most common start hour
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['hour_start'] = df['Start Time'].dt.hour
    popular_hour = df['hour_start'].mode()[0]
    print("The most popular time in the day for bike\nrental is: {} hundred hours.".format(popular_hour))

# Display station statistics
def station_stats(df):
    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular start station is: {}".format(popular_start_station))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular end station is: {}".format(popular_end_station))

    # Display most frequent combination of start station and end station trip
    df['popular_combo']=df['Start Station']+" "+df['End Station']
    popular_combo=df['popular_combo'].mode()[0]
    print("The most frequent pair of stations is:\n {}".format(popular_combo))
    print()
# Display trip duration statistics
def trip_duration_stats(df):
    # Display total travel time
    total_travel_time=df['Trip Duration'].sum()/60/60/24
    days_travel_time=total_travel_time/24
    days_travel="%.2f"% days_travel_time
    print("The total time travel is: {} days".format(days_travel))

    # Display mean travel time
    mean_travel_time=df['Trip Duration'].mean()/60
    mean_travel_time="%.2f"% mean_travel_time
    print("The mean time travel is: {} minutes".format(mean_travel_time))

# Display statistics on bikeshare users
def user_stats(df,city):
    # Display counts of user types
    print("User Types are:")
    print()
    print(df['User Type'].value_counts())
    print()

    # Display counts of gender
    # NOTE: Washington has no gender or birth year data
    if city!='washington':
        print()
        print("Gender split for using the bikes was:")
        print()
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
        print()
        print("The earliest birth year was: {}".format(int(df['Birth Year'].min())))
        print("The most recent birth year was: {}".format(int(df['Birth Year'].max())))
        print("The most common birth year was: {}".format(int(df['Birth Year'].mean())))
    else:
        print("There is no available Gender or Birth Year data available for Washington")

def display_raw_data(df):
    print()
    raw_data=input("Would you like to see the raw data?")
    counter_rows1=0
    counter_rows2=5
    if raw_data=="Yes".lower():
        while counter_rows2<df.shape[0]-1:
            print()
            print(df.iloc[counter_rows1:counter_rows2,0:-1])
            counter_rows1+=5
            counter_rows2+=5
            more_raw_data=input("Would you like to see the next 5 rows?")
            if more_raw_data=="No".lower():
                break

#The 'main' function calls in all the functions above
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

#
if __name__ == "__main__":
    main()
