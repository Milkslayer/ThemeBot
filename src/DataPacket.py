members = {}
theme = None
seed = ""
is_process_started = False
is_seed_generated = False

def make_theme_object():
    return {
        "is_theme_generated": 0,
        "theme": ""
    }

def make_member_object(name: str):
    return {
        name: {
            'token': '',
            'suggestions': [],
            "token_received": False
        }
    }