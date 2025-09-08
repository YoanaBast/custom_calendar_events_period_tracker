from funcs.CalendarManager import CalendarManager



def get_user_command(username, *args):
    mng = CalendarManager()

    user = username
    print("0. Exit\n"
          "1. Add Event\n"
          "2. Start tracking period\n"
          "3. Edit period dates\n"
          "4. Edit event date\n"
          "5. Delete event\n"
          "6. Show calendar\n")

    try:
        command = int(input("Please enter command #: "))
    except ValueError:
        print('Please enter an integer.')
        command = int(input("Please enter command #: "))

    if command == 0:
        return 'exit'

    elif command == 1:
        event_name = input('Event name: ')
        event_type = input('Event type: ')
        event_start_date = input('Event start date: ')
        event_end_date = input('Event end date: ')
        event_notes = input('Event notes: ')

        mng.add_event(user, event_name, event_type, event_start_date)


    elif command == 2:
        first_day_last_per = input('What was the first day of your last period? ')
        cycle_len = int(input('What is your cycle length? '))
        per_len = int(input('What is period length? '))

        mng.start_tracking_period(user, first_day_last_per)

    elif command == 6:
        print(mng.display_calendar_on_terminal(user))

    else:
        print('this is under implementation')


user = input('username: ')

while True:
    if get_user_command(user) == 'exit':
        print('Goodbye!')
        break

