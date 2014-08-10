# Notes
This Python application is a CLI version of Notational Velocity's note-taking.

# Usage
> notes.py add title "note body" tag1 tag2

> notes.py delete title

> note.py edit title "new body" moreTag1 moreTag2

Searching is not yet implemented.

Notes are stored in ~/.notes, but this can be changed with the -d flag. The -c flag will clean out the current repository.

# Will support…
Eventually, I plan to make this tool use git for versioning.