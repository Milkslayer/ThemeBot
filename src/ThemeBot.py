import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

from telegram import ReplyKeyboardMarkup

from datetime import datetime
import random
import hashlib
from Constants import (COLLECTING_SUGGESTIONS, COLLECTING_TOKENS, REPLYING,
                       FINISHED_COLLECTING_SUGGESTIONS, FINISHED_COLLECTING_TOKENS)
import Messages
import DataPacket
import Constants
import uuid
from Utils import SeedGenerator
from Utils import IO
from Constants import (COLLECTING_SUGGESTIONS, COLLECTING_TOKENS, REPLYING,
                       FINISHED_COLLECTING_SUGGESTIONS, FINISHED_COLLECTING_TOKENS)

DEBUG = True


def start(update, context):
    if DEBUG:
        print(update)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=Messages.WELCOME_name % update.effective_user.username)


def help(update, context):
    if DEBUG:
        print(update)
    if update.effective_chat.type == "group":
        context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.HELP_GROUP)
    if update.effective_chat.type == "private":
        context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.HELP_PRIVATE)


def begin_theme_selection(update, context):
    if DEBUG:
        print(update)
        print("Theme selection initiated")
    if not DataPacket.is_process_started:
        if update.effective_chat.type == "group":
            context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.STARTING_THEME_SELECTION)
            DataPacket.is_process_started = True
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.SELECTION_PROCESS_ONLY_IN_GROUP)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.SELECTION_PROCESS_ALREADY_STARTED)


def generate_token(update, context):
    if DEBUG:
        print(update)
        print("User %s requested token" % update.effective_user.username)
    if DataPacket.is_process_started:
        if update.effective_chat.type != "group":
            username = update.effective_user.username
            if username not in DataPacket.members:
                member = DataPacket.make_member_object(username)
                DataPacket.members.update(member)
                DataPacket.members[username]["token"] = str(uuid.uuid4())

                IO.save_file_json(Constants.DATA_PATH + Constants.DATA_MEMBERS_FILENAME, DataPacket.members)

                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=Messages.GENERATED_TOKEN_IS % DataPacket.members[username]["token"])
                print("\tToken generated: %s" % DataPacket.members[username]["token"])
            else:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=Messages.TOKEN_ALREADY_GENERATED % DataPacket.members[username]["token"])
                print("\tUser already has token: %s" % DataPacket.members[username]["token"])

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=Messages.CANNOT_REQUEST_TOKEN_IN_GROUP)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=Messages.SELECTION_NOT_STARTED)


def begin_seed_generation(update, context):
    is_ready = True
    if DEBUG:
        print(update)
        print("Seed generation started")
    if update.effective_chat.type == "group":
        if not DataPacket.is_seed_generated:
            for member, data in DataPacket.members.items():
                if len(data["suggestions"]) == 0:
                    print("%s did not add any suggestions" % member)
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=Messages.MEMBER_NOT_ADDED_SUGGESTIONS_username % member)
                    is_ready = False
            if is_ready:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=Messages.START_SEED_GENERATION)
                return COLLECTING_TOKENS
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=Messages.SEED_IS_GENERATED % DataPacket.seed)
            return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.CANNOT_REQUEST_SEED_IN_GROUP)
    return ConversationHandler.END


def check_tokens_received(members: dict) -> list:
    not_received_from = []
    for member, data in members.items():
        if not data["token_received"]:
            not_received_from.append(member)
    return not_received_from


def collecting_tokens(update, context):
    if DEBUG:
        print(update)
        print(2)

    if update.effective_chat.type == "group":
        username = update.effective_user.username
        text = update.message.text.split(' ')
        print(text)
        if username in DataPacket.members:
            if len(text) == 2:
                if text[1] == DataPacket.members[username]["token"]:
                    DataPacket.members[username]["token_received"] = True
                    IO.save_file_json(Constants.DATA_PATH + Constants.DATA_MEMBERS_FILENAME, DataPacket.members)
                    context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=Messages.TOKEN_RECEIVED_FROM % username)

        tokens_not_received = check_tokens_received(DataPacket.members)
        if len(tokens_not_received) != 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=Messages.WAITING_FOR_TOKEN_FROM % str(tokens_not_received))
            return COLLECTING_TOKENS
        elif len(tokens_not_received) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=Messages.ALL_TOKENS_RECEIVED)
            return get_seed(update, context)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.MUST_BE_IN_GROUP)
        return COLLECTING_TOKENS


def get_seed(update, context):
    tokens = []
    for data in DataPacket.members.values():
        tokens.append(data["token"])
    SeedGenerator.add_tokens(tokens)
    DataPacket.seed = SeedGenerator.generate_seed()
    DataPacket.is_seed_generated = True
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your seed is %s" % str(DataPacket.seed))
    return ConversationHandler.END


def get_theme(update, context):
    if DEBUG:
        print(update)
    if DataPacket.is_seed_generated:
        if DataPacket.theme is None:
            DataPacket.theme = DataPacket.make_theme_object()

            mega_suggestion_list = []
            tokens = []
            for data in DataPacket.members.values():
                mega_suggestion_list += data["suggestions"]
                tokens += data["token"]
            DataPacket.theme["theme"] = SeedGenerator.get_theme(mega_suggestion_list, DataPacket.seed)
            DataPacket.theme["is_theme_generated"] = 1

            IO.save_file_json(Constants.DATA_PATH + Constants.DATA_THEME_FILENAME, DataPacket.theme)

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=Messages.GENERATED_THEME_IS % DataPacket.theme["theme"])

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.THEME_ALREADY_SELECTED % "theme")

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.SEED_NOT_GENERATED)


def add_suggestions(update, context):
    if DEBUG:
        print(update)
    if update.effective_chat.type != 'group':
        if update.effective_user.username in DataPacket.members:
            context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.SEND_ME_SUGGESTIONS)

            return COLLECTING_SUGGESTIONS
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.TOKEN_NOT_GENERATED)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.CANNOT_DO_THIS_IN_GROUP)
        return True


def collecting_suggestions(update, context):
    if DEBUG:
        print(update)
    suggestions = update.message.text.split(',')
    for suggestion in suggestions:
        suggestion = suggestion.lower()
        if len(suggestion) == 0:
            continue
        if suggestion in DataPacket.members[update.effective_user.username]["suggestions"]:
            continue
        DataPacket.members[update.effective_user.username]["suggestions"].append(suggestion)
    IO.save_file_json(Constants.DATA_PATH + Constants.DATA_MEMBERS_FILENAME, DataPacket.members)

    context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.SUGGESTIONS_ADDED)
    return finished_adding_suggestions(update, context)


def finished_adding_suggestions(update, context):
    suggestions = DataPacket.members[update.effective_user.username]["suggestions"]
    context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.YOUR_SUGGESTIONS_ARE + str(suggestions))
    return ConversationHandler.END


def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="User cancelled conversations")
    return ConversationHandler.END


def unknown(update, context):
    if DEBUG:
        print(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.UNKNOWN_COMMAND)


class ThemeBot:
    def __init__(self, token):
        self.updater = updater = Updater(token=token, use_context=True)
        self.dispatcher = updater.dispatcher
        self.init_command_handlers()
        self.init_conversation_handler()
        self.init_message_handlers()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def init_command_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", start))
        self.dispatcher.add_handler(CommandHandler("help", help))
        self.dispatcher.add_handler(CommandHandler("begin_theme_selection", begin_theme_selection))
        self.dispatcher.add_handler(CommandHandler("generate_token", generate_token))
        self.dispatcher.add_handler(CommandHandler("get_theme", get_theme))

    def init_message_handlers(self):
        self.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    def init_conversation_handler(self):
        suggestion_handler = ConversationHandler(
            entry_points=[CommandHandler('add_suggestions', add_suggestions)],
            states={
                COLLECTING_SUGGESTIONS: [MessageHandler(Filters.text, collecting_suggestions)],
            },
            fallbacks=[MessageHandler(Filters.regex('^Cancel$'), cancel)]
        )
        token_handler = ConversationHandler(
            entry_points=[CommandHandler('begin_seed_generation', begin_seed_generation)],
            states={
                COLLECTING_TOKENS: [MessageHandler(Filters.text, collecting_tokens)],
            },
            fallbacks=[MessageHandler(Filters.regex('^Cancel$'), cancel)]
        )
        self.dispatcher.add_handler(suggestion_handler)
        self.dispatcher.add_handler(token_handler)

    def start_bot(self):
        self.updater.start_polling()
        self.updater.idle()







