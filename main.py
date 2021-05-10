from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler,Filters)
from db_helper import DBHelper
from conf import TOKEN, DB_NAME

BTN_TODAY, BTN_TOMORROW, BTN_CALENDAR, BTN_REGION, BTN_DUA, BTN_CHANNEL =("Bugun📆","Ertaga📅", "To'liq taqvim🗓","Mintaqa🔧","Duo🤲","Kanalimizga obuna bo'ling📎")

main_buttons = ReplyKeyboardMarkup([
[BTN_TODAY], [BTN_TOMORROW,BTN_CALENDAR ],[BTN_REGION],[BTN_DUA],[BTN_CHANNEL]
])

STATE_REGION = 1
STATE_CALENDAR = 2

user_region = dict()
db = DBHelper(DB_NAME)
def region_buttons():
    regions = db.get_regions()
    buttons = []
    tmp_b = []
    for region in regions:
        tmp_b.append(InlineKeyboardButton(region["name"], callback_data=region["id"]))
        if len(tmp_b) == 2:
            buttons.append(tmp_b)
            tmp_b = []
    return buttons
def start(update, context):
    user = update.message.from_user
    user_region[user.id]=None
    buttons = region_buttons()



    update.message.reply_html("Assolomu alaykum <b>{}!</b>\n \n <b>Ramazon oyingiz muborak bo'lsin!</b> \n \n Sizga qaysi mintaqa bo'yicha ma'lumot berayin?".
    format(user.first_name), reply_markup=InlineKeyboardMarkup(buttons))
    return STATE_REGION
def inline_callback(update,context):
    try:
        query= update.callback_query
        user_id =query.from_user.id
        user_region[user_id]=int(query.data)
        query.message.delete()
        query.message.reply_html(text='<b>Ramazon taqvimi</b>2️⃣0️⃣2️⃣1️⃣ \n \n Quyidagilardan birini tanlang👇👇👇',
        reply_markup=main_buttons)

        return STATE_CALENDAR
    except Exception as e:
        print("error", str(e))


def cr_today(update,context):
    try:
            user_id = update.message.from_user.id
            if not user_region[user_id]:
                return STATE_REGION
            region_id = user_region[user_id]
            region = db.get_region(region_id)

            today = str(datetime.now().date())
            calendar = db.get_calendar_by_region(region_id, today)
            photopath = "1.jpg"
            message ="<b>Ramazon</b> 2021 \n<b>{}</b> vaqti \n \n Saharlik: <b>{}</b>\n Iftorlik: <b>{}</b>".format(
            region['name'], calendar['fajr'], calendar['maghrib'][:5])

            update.message.reply_photo(photo = open(photopath,'rb'), caption = message, parse_mode="HTML", reply_markup=main_buttons)
    except Exception as e:
        print("error", str(e))
def cr_tomorrow(update,context):
    user_id = update.message.from_user.id
    if not user_region[user_id]:
        return STATE_REGION
    region_id = user_region[user_id]
    region = db.get_region(region_id)

    dt = str(datetime.now().date() + timedelta(days=1))
    calendar = db.get_calendar_by_region(region_id, dt)
    photopath = "1.jpg"
    message ="<b>Ramazon</b> 2021 \n<b>{}</b> vaqti \n \n Saharlik: <b>{}</b>\n Iftorlik: <b>{}</b>".format(
    region['name'], calendar['fajr'], calendar['maghrib'][:5])

    update.message.reply_photo(photo = open(photopath,'rb'), caption = message, parse_mode="HTML", reply_markup=main_buttons)
def cr_month(update,context):
    try:
            user_id = update.message.from_user.id
            if not user_region[user_id]:
                return STATE_REGION
            region_id = user_region[user_id]
            region = db.get_region(region_id)
            photopath = "tables/region_{}.png".format(region['id'])
            message ="📅<b>Ramazon</b> 2021 \n<b>{}</b> vaqti📅".format(
            region['name'] )

            update.message.reply_photo(photo = open(photopath,'rb'), caption = message, parse_mode="HTML", reply_markup=main_buttons)
    except Exception as e:
        print("error", str(e))
def sc_region(update,context):
    buttons = region_buttons()
    update.message.reply_text("🇺🇿🇺🇿Sizga qaysi mintaqa bo'yicha ma'lumot berayin?🇺🇿🇺🇿", reply_markup=InlineKeyboardMarkup(buttons))
    return STATE_REGION
def sc_dua(update,context):
    photopath = "ramadan_dua.png"
    saharlik = "\t🤲🤲Og‘iz yopish duosi(Saharlik):\n\n <b>Navaytu an asuma sovma shahri ramazona minal fajri ilal mag‘ribi, xolisan lillahi ta’ala. Allohu akbar</b>"
    iftorlik ="\t🤲🤲Og‘iz ochish duosi(Iftorlik):\n\n <b>Allohumma laka sumtu va bika amantu va a’layka tavakkaltu va a’laa rizqika aftortu, fag‘firliy ma qoddamtu va maa axxortu</b>"
    update.message.reply_photo(photo = open(photopath,'rb'), caption ="{}\n {}\n".format(saharlik, iftorlik) , parse_mode="HTML", reply_markup=main_buttons)
def sc_channel(update,context):
    update.message.reply_text("@it_school_uzb kanalimizga obuna bo'ling. Bunda siz IT soahsini mukammal o'rganishingiz mumkin")


def main():
    #Updater
    updater=Updater(TOKEN,use_context=True)

    #Dispatcher event
    dispatcher= updater.dispatcher
    #Inline keyboard callback_data
    #dispatcher.add_handler(CallbackQueryHandler(inline_callback))
    conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start',start)],
    states = {
    STATE_REGION:[CallbackQueryHandler(inline_callback),
    MessageHandler(Filters.regex('^('+BTN_TODAY+')$'),cr_today),
    MessageHandler(Filters.regex('^('+BTN_TOMORROW+')$'),cr_tomorrow),
    MessageHandler(Filters.regex('^('+BTN_CALENDAR+')$'),cr_month),
    MessageHandler(Filters.regex('^('+BTN_REGION+')$'),sc_region),
    MessageHandler(Filters.regex('^('+BTN_DUA+')$'),sc_dua),
    MessageHandler(Filters.regex('^('+BTN_CHANNEL+')$'),sc_channel)
    ],
    STATE_CALENDAR:[
    MessageHandler(Filters.regex('^('+BTN_TODAY+')$'),cr_today),
    MessageHandler(Filters.regex('^('+BTN_TOMORROW+')$'),cr_tomorrow),
    MessageHandler(Filters.regex('^('+BTN_CALENDAR+')$'),cr_month),
    MessageHandler(Filters.regex('^('+BTN_REGION+')$'),sc_region),
    MessageHandler(Filters.regex('^('+BTN_DUA+')$'),sc_dua),
    MessageHandler(Filters.regex('^('+BTN_CHANNEL+')$'),sc_channel)
    ],
    },
    fallbacks = [CommandHandler('start',start)]
    )
    dispatcher.add_handler(conv_handler)
    #Start
    #dispatcher.add_handler(CommandHandler('start',start))
    updater.start_polling()
    updater.idle()
main()
