import Messages
import DataPacket
import Constants
import uuid
from Utils import SeedGenerator
from Utils import IO


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


# TODO: Add handlers for conversation
def begin_seed_generation(update, context):
    if DEBUG:
        print(update)


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


# TODO: Add handlers for conversation
def add_suggestions(update, context):
    if DEBUG:
        print(update)


def unknown(update, context):
    if DEBUG:
        print(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text=Messages.UNKNOWN_COMMAND)