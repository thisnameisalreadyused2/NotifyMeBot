from utils.weather import get_forecast_for_today
from utils.news import get_news_for_country


def summary_handler(update, context):
    weather = get_forecast_for_today("Cherkasy")
    news = get_news_for_country("ua")
    msg = f"{weather}\n\n{news}"
    try:
        context.bot.send_message(update.message.from_user.id, msg, parse_mode="Markdown")
    except Exception as ex:
        print(ex)

