import collections
Cmd = collections.namedtuple("Cmd", "add edit delete find read changelog revert")
Op = collections.namedtuple("Op", "command title body params")
commands = Cmd("add", "edit", "delete", "find", "read", "log", "undo")