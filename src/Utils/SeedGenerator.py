from datetime import datetime
import random
import hashlib
import copy

seeding_tokens: list = []


def add_tokens(tokens: list):
    global seeding_tokens
    seeding_tokens = copy.deepcopy(tokens)


def generate_seed():
    global seeding_tokens
    hash_string = ''
    for token in seeding_tokens:
        hash_string += str(token)

    hash_string += str(datetime.now())

    hash_object = hashlib.sha256(hash_string.encode())
    return hash_object.hexdigest()


def get_theme(suggestions: list, seed) -> str:
    random.seed(seed)
    rand_int = random.randint(0, len(suggestions)-1)
    return suggestions[rand_int]
