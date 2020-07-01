import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from telegram import ReplyKeyboardMarkup

from datetime import datetime
import random
import hashlib
import Commands


class ThemeBot:
    def __init__(self, token):
        self.updater = updater = Updater(token=token, use_context=True)
        self.dispatcher = updater.dispatcher
        self.init_command_handlers()
        self.init_message_handlers()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def init_command_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", Commands.start))
        self.dispatcher.add_handler(CommandHandler("help", Commands.help))
        self.dispatcher.add_handler(CommandHandler("begin_theme_selection", Commands.begin_theme_selection))
        self.dispatcher.add_handler(CommandHandler("generate_token", Commands.generate_token))
        self.dispatcher.add_handler(CommandHandler("add_suggestions", Commands.add_suggestions))
        self.dispatcher.add_handler(CommandHandler("begin_seed_generation", Commands.begin_seed_generation))
        self.dispatcher.add_handler(CommandHandler("get_theme", Commands.get_theme))

    def init_message_handlers(self):
        self.dispatcher.add_handler(MessageHandler(Filters.command, Commands.unknown))

    def start_bot(self):
        self.updater.start_polling()

#
# CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
#

#
#
# def add_suggestions(update, context):
#     if update.effective_chat.type != 'group':
#         if len(contestants[update.effective_user.username]['suggestions']) != 0:
#             context.bot.send_message(chat_id=update.effective_chat.id,
#                                      text="Looks like you already have added your suggestions")
#             return ConversationHandler.END
#         else:
#             context.bot.send_message(chat_id=update.effective_chat.id,
#                                  text="Send me a message with your suggestions (separated by ',') "
#                                       "Please don't try to hack me. My developer did not implement any error handling")
#             return TYPING_REPLY
#     else:
#         context.bot.send_message(chat_id=update.effective_chat.id,
#                                  text="You cannot do this in a group")
#
#
# def received_information(update, context):
#     if update.effective_user.username in contestants:
#         user_suggestions = update.message.text.split(',')
#
#         if len(user_suggestions) != 10:
#             context.bot.send_message(chat_id=update.effective_chat.id,
#                                      text="Lol. I need 10 words separated by comma (,)")
#         else:
#             contestants[update.effective_user.username]['suggestions'] = user_suggestions
#             save()
#             context.bot.send_message(chat_id=update.effective_chat.id,
#                                      text="Thank you. Your suggestions have been added")
#             done(update, context)
#             return ConversationHandler.END
#     return True
#
#
# def done(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text="Thank you!")
#     s_list = contestants[update.effective_user.username]['suggestions']
#
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text="Your suggestions are: " + str(s_list))
#     ConversationHandler.END
#
#
# conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('add_suggestions', add_suggestions)],
#         states={
#                 TYPING_REPLY: [MessageHandler(Filters.text, received_information)],
#
#             },
#         fallbacks=[MessageHandler(Filters.regex('^asdasdasdsad$'), done)]
#     )
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# start_handler = CommandHandler('start', start)
# help_handler = CommandHandler('help', help)
# token_handler = CommandHandler('get_token', get_token)
# get_game_topic_handler = CommandHandler('get_game_topic', get_game_topic)





