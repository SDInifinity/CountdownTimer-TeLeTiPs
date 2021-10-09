#Copyright ©️ 2021 TeLe TiPs. All Rights Reserved
#You are free to use this code in any of your project, but you MUST include the following in your README.md (Copy & paste)
# ##Credits - [Countdown Timer Telegram bot by TeLe TiPs] (https://github.com/teletips/CountdownTimer-TeLeTiPs)

# Changing the code is not allowed! Read GNU AFFERO GENERAL PUBLIC LICENSE: https://github.com/teletips/CountdownTimer-TeLeTiPs/blob/main/LICENSE
 
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from plugins.teletips_t import *
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.raw.functions.messages import UpdatePinnedMessage
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

bot=Client(
    "Countdown-TeLeTiPs",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"],
    channel_username = os.environ["CHANNEL_USERNAME"]
)

stoptimer = False

TELETIPS_MAIN_MENU_BUTTONS = [
            [
                InlineKeyboardButton('🙋‍♀️ Commands Help 🙋‍♀️', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('🚀 Developers 🚀', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton('👻 My Updates 👻', url='https://t.me/sl_bot_zone'),
            ],
            [
                InlineKeyboardButton('🏆 Adevertitments 🏆', callback_data="TUTORIAL_CALLBACK")
            ],
            [
                InlineKeyboardButton('💖 Rate Me 💖', url="https://t.me/slbotzone")
            ]
        ]

@bot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, lel):
  user_id = lel.from_user.id
  chat_id = lel.message.chat.id
  chat_u = Config.CHANNEL_USERNAME #channel for force sub
  if chat_u:
    channel = chat_u
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if lel.message.reply_to_message.from_user.id == user_id:
              lel.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(lel.id, text="❗ Join the mentioned '👨‍💻Channel👨‍💻' and press the '⛔Unmute Me⛔' button again.😇", show_alert=True)
      else:
        client.answer_callback_query(lel.id, text="⛔ You are muted by admins for other reasons 🥺🤗", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{lel.from_user.mention} is trying to Unmute himself but I can't unmute him because I am not an admin in this chat.😑")
      else:
        client.answer_callback_query(lel.id, text="❗ Warning: Don't click the button if you can speak freely.⚡⚡", show_alert=True)

@bot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_u = Config.CHANNEL_USERNAME #channel for force sub
  if chat_u:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator"):
      channel = chat_u
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
         try: #tahukai daala
              chat_u = chat_u.replace('@','')
              tauk = message.from_user.mention
              sent_message = message.reply_text(
                Config.WARN_MESSAGE,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("🗣 Unmute Me🔥", callback_data="START_CALLBACK")],
                  [InlineKeyboardButton("🔊 Join Channel🤖", url=f"https://t.me/{chat_u}")]]))
              client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))

@bot.on_message(filters.command(['start','help']) & filters.private)
async def start(client, message):
    text = START_TEXT
    reply_markup = InlineKeyboardMarkup(TELETIPS_MAIN_MENU_BUTTONS)
    await message.reply(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
    
@bot.on_callback_query()
async def callback_query(client: Client, query: CallbackQuery):
    if query.data=="HELP_CALLBACK":
        TELETIPS_HELP_BUTTONS = [
            [
                InlineKeyboardButton("🙋‍♀️ Back Mein Menu ", callback_data="START_CALLBACK")
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_HELP_BUTTONS)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="GROUP_CALLBACK":
        TELETIPS_GROUP_BUTTONS = [
            [
                InlineKeyboardButton("🇱🇰 Main Support", url="https://t.me/sl_bot_zone")
            ],
            [
                InlineKeyboardButton("🌎 Advertitments 🏆", url="https://t.me/slbotzone")
            ],
            [
                InlineKeyboardButton("🙋‍♀️ Back", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_GROUP_BUTTONS)
        try:
            await query.edit_message_text(
                GROUP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    

    elif query.data=="TUTORIAL_CALLBACK":
        TELETIPS_TUTORIAL_BUTTONS = [
            [
                InlineKeyboardButton("SL Bot Zone", url="https://t.me/szteambots")
            ],
            [
                InlineKeyboardButton("WL Film World", url="https://t.me/FilmAndTVSeriasChat")
            ],
            [
                InlineKeyboardButton("Developer", url="https://t.me/omindas")
            ],
            [
                InlineKeyboardButton("🙋‍♀️ Back", callback_data="START_CALLBACK"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_TUTORIAL_BUTTONS)
        try:
            await query.edit_message_text(
                TUTORIAL_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass      
          
    elif query.data=="START_CALLBACK":
        TELETIPS_START_BUTTONS = [
            [
                InlineKeyboardButton('🙋‍♀️ Commands Help 🙋‍♀️', callback_data="HELP_CALLBACK")
            ],
            [
                InlineKeyboardButton('🚀 Developers 🚀', callback_data="GROUP_CALLBACK"),
                InlineKeyboardButton(',👻 My Updates 👻', url='https://t.me/sl_bot_zone'),
            ],
            [
                InlineKeyboardButton('🏆 Adertitments 🏆', callback_data="TUTORIAL_CALLBACK")
            ],
            [
                InlineKeyboardButton('💖 Rate Me 💖', url="https://t.me/slbotzone")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(TELETIPS_START_BUTTONS)
        try:
            await query.edit_message_text(
                START_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass    

@bot.on_message(filters.command('set'))
async def set_timer(client, message):
    global stoptimer
    try:
        if message.chat.id>0:
            return await message.reply('⛔️ Try this command in a **group chat**.')
        elif not (await client.get_chat_member(message.chat.id,message.from_user.id)).can_manage_chat:
            return await message.reply('👮🏻‍♂️ Sorry, **only admins** can execute this command.')    
        elif len(message.command)<3:
            return await message.reply('❌ **Incorrect format.**\n\n✅ Format should be like,\n<code> /set seconds "event"</code>\n\n**Example**:\n <code>/set 86400 "TIME LEFT UNTIL NEW YEAR"</code>')    
        else:
            user_input_time = int(message.command[1])
            user_input_event = str(message.command[2])
            get_user_input_time = await bot.send_message(message.chat.id, user_input_time)
            await get_user_input_time.pin()
            if stoptimer: stoptimer = False
            if 0<user_input_time<=10:
                while user_input_time and not stoptimer:
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve [Jobs](https://telegra.ph/file/290b04f8fb43495294ffc.mp4)'.format(user_input_event, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(1)
                    user_input_time -=1
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 10<user_input_time<60:
                while user_input_time>0 and not stoptimer:
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(3)
                    user_input_time -=3
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 60<=user_input_time<3600:
                while user_input_time>0 and not stoptimer:
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**m** : {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, m, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(3)
                    user_input_time -=3
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 3600<=user_input_time<86400:
                while user_input_time>0 and not stoptimer:
                    h=user_input_time%(3600*24)//3600
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**h** : {:02d}**m** : {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, h, m, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(7)
                    user_input_time -=7
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif user_input_time>=86400:
                while user_input_time>0 and not stoptimer:
                    d=user_input_time//(3600*24)
                    h=user_input_time%(3600*24)//3600
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**d** : {:02d}**h** : {:02d}**m** : {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, d, h, m, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(9)
                    user_input_time -=9
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            else:
                await get_user_input_time.edit(f"🤷🏻‍♂️ I can't countdown from {user_input_time}")
                await get_user_input_time.unpin()
    except FloodWait as e:
        await asyncio.sleep(e.x)

@bot.on_message(filters.command('stopc'))
async def stop_timer(Client, message):
    global stoptimer
    try:
        if (await bot.get_chat_member(message.chat.id,message.from_user.id)).can_manage_chat:
            stoptimer = True
            await message.reply('🛑 Countdown stopped.')
        else:
            await message.reply('👮🏻‍♂️ Sorry, **only admins** can execute this command.')
    except FloodWait as e:
        await asyncio.sleep(e.x)

print("Countdown Timer is alive!")
bot.run()

#Copyright ©️ 2021 TeLe TiPs. All Rights Reserved
