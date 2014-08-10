import collections
Cmd = collections.namedtuple("Cmd", "add edit delete find read")
Op = collections.namedtuple("Op", "command title body params")
commands = Cmd("add", "edit", "delete", "find", "read")