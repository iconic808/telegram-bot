import telebot
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

TOKEN = "8687497631:AAE4niCmKtkhPsAy44zn04-bZOjJYg94Kd4"
ADMIN_ID = 5888788582

bot = telebot.TeleBot(TOKEN)

premium_channel = "https://t.me/+Pjf9kjog2Y81Njg1"
demo_channel = "https://t.me/+Pjf9kjog2Y81Njg1"
how_channel = "https://t.me/+Pjf9kjog2Y81Njg1"

waiting_screenshot = {}
waiting_qr = False

DB_FILE = "database.json"


# DATABASE
def load_db():
    try:
        with open(DB_FILE,"r") as f:
            return json.load(f)
    except:
        return {"users":[]}


def save_db(data):
    with open(DB_FILE,"w") as f:
        json.dump(data,f)


db = load_db()
users = set(db["users"])


def save_user(uid):
    if uid not in users:
        users.add(uid)
        db["users"] = list(users)
        save_db(db)


# TEXT
start_text = """
𝐕𝐢𝐝𝐞𝐨 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 🌸

𝐅𝐨𝐫 𝐃𝐞𝐬𝐢 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 𝐋𝐨𝐯𝐞𝐫𝐬 😋

𝐍𝐨 𝐒𝐧#𝐩, 𝐏𝐮𝐫𝐞 𝐃𝐞𝐬𝐢 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 😙

𝐫𝐚𝐫𝐞 𝐃𝐞𝐬𝐢 𝐥𝐞#𝐤𝐬 𝐞𝐯𝐞𝐫.... 🎀

𝐉𝐮𝐬𝐭 𝐩𝐚𝐲 𝐚𝐧𝐝 𝐠𝐞𝐭 𝐞𝐧𝐭𝐫𝐲...

𝐍𝐨 - 𝐀𝐝𝐬 𝐒𝐡#𝐭 🔥

𝐏𝐫𝐢𝐜𝐞 :- ₹𝟗𝟗.𝟎𝟎/-

𝐕𝐚𝐥𝐢𝐝𝐢𝐭𝐲 :- 𝐥𝐢𝐟𝐞𝐭𝐢𝐦𝐞
"""


payment_text = """
1️⃣ 𝐒𝐜𝐚𝐧 𝐐𝐑 & 𝐏𝐚𝐲 ₹𝟗𝟗
2️⃣ 𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 '𝐈 𝐇𝐀𝐕𝐄 𝐏𝐀𝐈𝐃' 𝐛𝐮𝐭𝐭𝐨𝐧 𝐛𝐞𝐥𝐨𝐰 👇
"""


# START
@bot.message_handler(commands=['start'])
def start(message):

    save_user(message.from_user.id)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💎 Get Premium",callback_data="buy"))
    markup.add(InlineKeyboardButton("🎬 Premium Demo",url=demo_channel))
    markup.add(InlineKeyboardButton("📖 How To Get Premium",url=how_channel))

    bot.send_photo(
        message.chat.id,
        open("start.jpg","rb"),
        caption=start_text,
        reply_markup=markup
    )


# USERS
@bot.message_handler(commands=['users'])
def users_count(message):

    if message.from_user.id != ADMIN_ID:
        return

    bot.reply_to(message,f"👥 Total Users: {len(users)}")


# BROADCAST
@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        text = message.text.split(" ",1)[1]
    except:
        bot.reply_to(message,"Usage:\n/broadcast your message")
        return

    for user in users:
        try:
            bot.send_message(user,text)
        except:
            pass

    bot.reply_to(message,"✅ Broadcast Sent")


# SET DEMO
@bot.message_handler(commands=['setdemo'])
def set_demo(message):

    global demo_channel

    if message.from_user.id != ADMIN_ID:
        return

    try:
        demo_channel = message.text.split(" ")[1]
        bot.reply_to(message,"✅ Demo channel updated")
    except:
        bot.reply_to(message,"Usage:\n/setdemo https://t.me/channel")


# SET HOW
@bot.message_handler(commands=['sethow'])
def set_how(message):

    global how_channel

    if message.from_user.id != ADMIN_ID:
        return

    try:
        how_channel = message.text.split(" ")[1]
        bot.reply_to(message,"✅ How channel updated")
    except:
        bot.reply_to(message,"Usage:\n/sethow https://t.me/channel")


# SET PREMIUM
@bot.message_handler(commands=['setpremium'])
def set_premium(message):

    global premium_channel

    if message.from_user.id != ADMIN_ID:
        return

    try:
        premium_channel = message.text.split(" ")[1]
        bot.reply_to(message,"✅ Premium channel updated")
    except:
        bot.reply_to(message,"Usage:\n/setpremium https://t.me/channel")


# SET QR
@bot.message_handler(commands=['setqr'])
def set_qr(message):

    global waiting_qr

    if message.from_user.id != ADMIN_ID:
        return

    waiting_qr = True
    bot.reply_to(message,"📷 Send new QR image")


# QR UPDATE
@bot.message_handler(content_types=['photo'])
def photo_handler(message):

    global waiting_qr

    uid = message.from_user.id

    # QR UPDATE (ADMIN)
    if waiting_qr and uid == ADMIN_ID:

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)

        with open("qr.jpg","wb") as f:
            f.write(downloaded)

        waiting_qr = False

        bot.reply_to(message,"✅ QR updated successfully")
        return


    # SCREENSHOT VERIFICATION
    if uid not in waiting_screenshot:

        bot.reply_to(
            message,
            "⚠️𝐓𝐇𝐈𝐒 𝐈𝐒 𝐍𝐎𝐓 𝐂𝐎𝐑𝐑𝐄𝐂𝐓 𝐒𝐄𝐋𝐄𝐂𝐓𝐈𝐎𝐍 🥲\n𝐏𝐋𝐄𝐀𝐒𝐄, 𝐒𝐄𝐋𝐄𝐂𝐓 𝐅𝐑𝐎𝐌 𝐎𝐏𝐓𝐈𝐎𝐍𝐒✅"
        )
        return


    waiting_screenshot.pop(uid)

    username = message.from_user.username or "NoUsername"

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Approve",callback_data="approve_"+str(uid)),
        InlineKeyboardButton("❌ Reject",callback_data="reject_"+str(uid))
    )

    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"Payment Screenshot\n\nUser: @{username}\nID: {uid}",
        reply_markup=markup
    )

    bot.reply_to(message,"⏳ Screenshot sent for verification")


# BUTTONS
@bot.callback_query_handler(func=lambda call: True)
def buttons(call):

    uid = call.from_user.id

    if call.data == "buy":

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ I HAVE PAID",callback_data="paid"))
        markup.add(InlineKeyboardButton("❌ Cancel",callback_data="back"))

        media = InputMediaPhoto(
            open("qr.jpg","rb"),
            caption=payment_text
        )

        bot.edit_message_media(
            media,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )


    elif call.data == "paid":

        waiting_screenshot[uid] = True
        bot.send_message(uid,"📸 Please send your payment screenshot now.")


    elif call.data == "back":

        bot.delete_message(call.message.chat.id,call.message.message_id)
        start(call.message)


    elif call.data.startswith("approve_"):

        uid = int(call.data.split("_")[1])

        bot.send_message(
            uid,
            "✅ Payment Verified!\n\nJoin your private channel:\n"+premium_channel
        )

        bot.edit_message_caption(
            caption="✅ Payment Approved",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

        bot.answer_callback_query(call.id,"Approved",show_alert=True)


    elif call.data.startswith("reject_"):

        uid = int(call.data.split("_")[1])

        bot.send_message(uid,"❌ Payment Rejected")

        bot.edit_message_caption(
            caption="❌ Payment Rejected",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

        bot.answer_callback_query(call.id,"Rejected",show_alert=True)


print("Bot Running...")
bot.infinity_polling(skip_pending=True)
