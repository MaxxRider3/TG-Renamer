
# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import random
import time
from datetime import datetime
import pytz

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
from helper_funcs.display_progress import progress_for_pyrogram
from helper_funcs.help_Nekmo_ffmpeg import take_screen_shot

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image


@pyrogram.Client.on_message(pyrogram.Filters.video)
async def convert_to_file(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.BANNED_USER_TEXT,
            reply_to_message_id=update.message_id
        )
        return
    TRChatBase(update.from_user.id, update.text, "converttovideo")
    if update.reply_to_message is None:
        description = Translation.CUSTOM_CAPTION_UL_FILE
        download_location = Config.DOWNLOAD_LOCATION + "/"
        b = await bot.send_message(
            chat_id=update.chat.id,
            text="Analyzing Video.....😃",
            reply_to_message_id=update.message_id
        )
        start = datetime.now()
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update.video,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_START_VIDEO,
                b,
                c_time
            )
        )
        if the_real_download_location is not None:
            bot.edit_message_text(
                text=Translation.SAVED_RECVD_DOC_FILE,
                chat_id=update.chat.id,
                message_id=b.message_id
            )
            # don't care about the extension
           # await bot.edit_message_text(
              #  text=Translation.UPLOAD_START,
             #   chat_id=update.chat.id,
            #    message_id=a.message_id
          #  )
            logger.info(the_real_download_location)
            # get the correct width, height, and duration for videos greater than 10MB
            # ref: message from @BotSupport
            width = 0
            height = 0
            duration = 0
            metadata = extractMetadata(createParser(the_real_download_location))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
            if not os.path.exists(thumb_image_path):
                thumb_image_path = await take_screen_shot(
                    the_real_download_location,
                    os.path.dirname(the_real_download_location),
                    random.randint(
                        0,
                        duration - 1
                    )
                )
            logger.info(thumb_image_path)
            # 'thumb_image_path' will be available now
            metadata = extractMetadata(createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
            # get the correct width, height, and duration for videos greater than 10MB
            # resize image
            # ref: https://t.me/PyrogramChat/44663
            # https://stackoverflow.com/a/21669827/4723940
            Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
            img = Image.open(thumb_image_path)
            # https://stackoverflow.com/a/37631799/4723940
            # img.thumbnail((90, 90))
            img.resize((90, height))
            img.save(thumb_image_path, "JPEG")
            # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            # try to upload file
            c_time = time.time()
            await bot.send_document(
                chat_id=update.chat.id,
                document=the_real_download_location,
                caption=description,
                #duration=duration,
                #width=width,
                #height=height,
                #supports_streaming=True,
                # reply_markup=reply_markup,
                thumb=thumb_image_path,
                reply_to_message_id=update.text,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START_VIDEO,
                    b,
                    c_time
                )
            )
            end = datetime.now()
            try:
                os.remove(the_real_download_location)
              #  os.remove(thumb_image_path)
            except:
                pass
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG.format(end),
                chat_id=update.chat.id,
                message_id=b.message_id,
                disable_web_page_preview=True
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.REPLY_TO_DOC_FOR_C2V,
            reply_to_message_id=update.message_id
        )

