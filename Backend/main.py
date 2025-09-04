from Backend.CalendarManager import CalendarManager

mng = CalendarManager()
mng.add_event('yoana', 'My Birthday',  'Birthday', '28/04')
print(mng.display_calendar_terminal('yoana'))
