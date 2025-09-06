from funcs.CalendarManager import CalendarManager

mng = CalendarManager()
mng.add_event('yoana', 'My Birthday', 'Birthday', '28/04')
mng.start_tracking_period('yoana', 30)
print(mng.display_calendar_on_terminal('yoana'))
