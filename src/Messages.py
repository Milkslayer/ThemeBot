HELP_GROUP = '''
What I can do for you:
/begin_theme_selection - Begin theme selection process. Users that wish to participate must initiate a chat with me 
and generate a token. Afterwards the user can add suggestions to the list of themes. When all users have added
their suggestions the /begin_seed_generation command can be fired.
/begin_seed_generation - Generates random seed for theme selection. After initiating the commands the users have to 
give their generated tokens back to me in this chat. After all tokens are gathered I will spit out a random seed.
/get_theme - Only works if all previous steps have been completed. I will use the generated seed to choose between the
suggested themes and pick one.
'''

HELP_PRIVATE = '''
What I can do for you:
/generate_token - Generate unique token
/add_suggestions - You can add one or multiple separated by ','
'''

WELCOME_name = "Hi %s. I am Game Jam Bot. Type /help for commands"

STARTING_THEME_SELECTION = "Ok. Let's pick a theme. Every member must generate a token. " \
                           "Please initiate a private conversation and generate your token. When all members have a" \
                           "token the process can continue"

SELECTION_PROCESS_ONLY_IN_GROUP = "You can only begin the theme selection process in a group"
SELECTION_PROCESS_ALREADY_STARTED = "Theme selection process has already been initiated"

SELECTION_NOT_STARTED = "You must initiate the selection process in a group"

CANNOT_REQUEST_TOKEN_IN_GROUP = "You cannot request Token in a group"
CANNOT_REQUEST_SEED_IN_GROUP = "You can only generate a seed in group chat"
CANNOT_DO_THIS_IN_GROUP = "You cannot do this in a group."
GENERATED_TOKEN_IS = "Yor token is generated: %s"
TOKEN_ALREADY_GENERATED = "You already have a token: %s"
SEED_NOT_GENERATED = "You must must generate a seed to use this command"
GENERATED_THEME_IS = "Your new theme is: %s"
THEME_ALREADY_SELECTED = "The theme is already selected. The theme is: %s"
UNKNOWN_COMMAND = "Sorry, I didn't understand that command."

MEMBER_NOT_ADDED_SUGGESTIONS_username = "%s has not added any suggestions."
START_SEED_GENERATION = "Seed generation has begun. Please give me your generated tokens."
SEND_ME_SUGGESTIONS = '''Send me a message with your suggestions (separated by ',') 
Please don't try anything funny. My developer did not implement any error handling'''

SUGGESTIONS_ADDED = "Thank you. Your suggestions have been added."
THANK_YOU = "Thank You!"
YOUR_SUGGESTIONS_ARE = "Your suggestions are: "
TOKEN_NOT_GENERATED = "You need to generate a token first."