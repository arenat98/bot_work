import datetime
from google.oauth2 import service_account
from googleapiclient import discovery

def check_calendar(bot, message):
    try:
        credentials = service_account.Credentials.from_service_account_file('credentials.json')
        service = discovery.build('calendar', 'v3', credentials=credentials)

        now = datetime.datetime.utcnow().isoformat() + '+07:00'  # 'Z' indicates UTC time
        end_of_week = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + '+07:00'  # События за 7 дней
        print('Checking events from', now, 'to', end_of_week)

        eventsResult = service.events().list(
            calendarId='7cf44d58482818e043c1b95b293016277bc379c15b68102f322f276ab657f8e3@group.calendar.google.com',
            timeMin=now,
            timeMax=end_of_week,
            maxResults=100,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = eventsResult.get('items', [])

        if not events:
            bot.send_message(message.chat.id, 'На этой неделе нет событий в календаре.')
        else:
            # Сортируем события по датам
            events.sort(key=lambda x: x['start'].get('dateTime', x['start'].get('date')))
            current_date = None

            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event['summary']
                event_date = start.split("T")[0]

                # Если дата события изменилась, выводим новую дату
                if event_date != current_date:
                    current_date = event_date
                    bot.send_message(message.chat.id, f"<b>События на {event_date}:</b>", parse_mode='HTML')

                # Выводим событие
                msg = f"<i>{summary}</i>"
                bot.send_message(message.chat.id, msg, parse_mode='HTML')

    except Exception as e:
        print("Произошла ошибка: ", e)
        bot.send_message(message.chat.id, "Сейчас есть проблемы с сетью. Пожалуйста, попробуйте снова через 20 минут.")
