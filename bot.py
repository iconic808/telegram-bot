import telebot
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

TOKEN = "8726917533:AAFsDJHAxWPwCtRC5RglI2rjXQQASSRe1Os"
ADMIN_ID = 8419203344

bot = telebot.TeleBot(TOKEN)

demo_channel = "https://t.me/+C6f4L2w7KyM0MTY1"
how_channel = "https://t.me/+C6f4L2w7KyM0MTY1"

waiting_screenshot = {}
waiting_qr = False
user_category = {}

DB_FILE = "database.json"

# ✅ FIXED Categories
categories = [
    ("🥵 𝐂𝐏 𝐊𝐢𝐝$", "https://t.me/+C6f4L2w7KyM0MTY1"),
    ("😍 𝐌𝟎𝐌 𝐒𝟎𝐍", "https://t.me/+aX_BhutfN11kNWQ1"),
    ("🍑 𝐓€€𝐍 𝐆𝐥𝐑𝐋", "https://t.me/+aX_BhutfN11kNWQ1"),
    ("💋 𝐑@𝐏€ & 𝐅𝟎𝐑€𝐄", "https://t.me/+aX_BhutfN11kNWQ1"),
    ("💦 𝐥𝐍𝐃𝐢@𝐍 𝐃€$𝐢", "https://t.me/+aX_BhutfN11kNWQ1"),
]

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

𝐉𝐮𝐬𝐭 𝐩𝐚𝐲 𝐚𝐧𝐝 𝐠𝐞𝐭 𝐞𝐧𝐭𝐫𝐲...

𝐏𝐫𝐢𝐜𝐞 :- ₹𝟗𝟗
"""

payment_text = """
1️⃣ Scan QR & Pay ₹99
2️⃣ Click 'I HAVE PAID'
"""

# START
@bot.message_handler(commands=['start'])
def start(message):

    save_user(message.from_user.id)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💎 Get Premium",callback_data="buy"))
    markup.add(InlineKeyboardButton("🎬 Demo",url=demo_channel))
    markup.add(InlineKeyboardButton("📖 How",url=how_channel))

    bot.send_photo(
        message.chat.id,
        open("start.jpg","rb"),
        caption=start_text,
        reply_markup=markup
    )

# PHOTO HANDLER
@bot.message_handler(content_types=['photo'])
def photo_handler(message):

    global waiting_qr
    uid = message.from_user.id

    if waiting_qr and uid == ADMIN_ID:

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)

        with open("qr.jpg","wb") as f:
            f.write(downloaded)

        waiting_qr = False
        bot.reply_to(message,"✅ QR updated")
        return

    if uid not in waiting_screenshot:
        bot.reply_to(message,"⚠️ Click 'I HAVE PAID' first")
        return

    username = message.from_user.username or "NoUsername"

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Approve",callback_data="approve_"+str(uid)),
        InlineKeyboardButton("❌ Reject",callback_data="reject_"+str(uid))
    )

    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"Payment Screenshot\nUser: @{username}\nID: {uid}",
        reply_markup=markup
    )

    bot.reply_to(message,"⏳ Sent for verification")

# BUTTONS
@bot.callback_query_handler(func=lambda call: True)
def buttons(call):

    uid = call.from_user.id

    if call.data == "buy":

        markup = InlineKeyboardMarkup()

        for i, (name, link) in enumerate(categories):
            markup.add(InlineKeyboardButton(name, callback_data=f"cat_{i}"))

        markup.add(InlineKeyboardButton("❌ Cancel", callback_data="back"))

        bot.edit_message_caption(
            caption="📂 Select category 👇",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

    elif call.data.startswith("cat_"):

        index = int(call.data.split("_")[1])
        selected_name, selected_link = categories[index]

        user_category[uid] = selected_link

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ I HAVE PAID", callback_data="paid"))
        markup.add(InlineKeyboardButton("⬅️ Back", callback_data="buy"))

        media = InputMediaPhoto(
            open("qr.jpg","rb"),
            caption=f"{selected_name}\n\n{payment_text}"
        )

        bot.edit_message_media(
            media,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

    elif call.data == "paid":

        waiting_screenshot[uid] = True
        bot.send_message(uid,"📸 Send screenshot")

    elif call.data == "back":

        bot.delete_message(call.message.chat.id,call.message.message_id)
        start(call.message)

    elif call.data.startswith("approve_"):

        uid = int(call.data.split("_")[1])

        link = user_category.get(uid, "Contact Admin")

        bot.send_message(
            uid,
            f"✅ Payment Verified!\n\nJoin:\n{link}"
        )

        bot.edit_message_caption(
            caption="✅ Approved",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

        bot.answer_callback_query(call.id,"Approved",show_alert=True)

    elif call.data.startswith("reject_"):

        uid = int(call.data.split("_")[1])

        bot.send_message(uid,"❌ Payment Rejected")

        bot.edit_message_caption(
            caption="❌ Rejected",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

        bot.answer_callback_query(call.id,"Rejected",show_alert=True)

print("Bot Running...")
bot.infinity_polling(skip_pending=True)
