
#A dictionary containing all commands, where each command has a "tag" (raw_text). 
#If the tag is True, the command must not be cleaned/filtered by the clear_target() function.
registry_commands = {
    "open": {"raw_text": False},
    "close": {"raw_text": False},
    "search": {"raw_text": True},
    "gemini": {"raw_text": True},
    "view tasks": {"raw_text": False},
    "view history": {"raw_text": False},
    "create task": {"raw_text": True},
    "play music": {"raw_text": True},
    "update": {"raw_text": False},
    "next music": {"raw_text": False},
    "stop music": {"raw_text": False},
    "start music": {"raw_text": False},
    "up volume": {"raw_text": False},
    "down volume": {"raw_text": False},   
}

#The tokens that will be discarded when clear-target() is executed
trash_tokens = {
    "a",
    "an",
    "the",
    "on",
    "for",
}