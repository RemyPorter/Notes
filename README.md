# Notes
This Python application is a CLI version of Notational Velocity's note-taking.

# Usage
> notes.py add title "note body" tag1 tag2

> notes.py delete title

> note.py edit title "new body" moreTag1 moreTag2

> note.py find searchterm #finds titles, tags, and notes that contain that word

> note.py read title #prints the contents of that note

> note.py log #prints the git history of the note versions

> note.py git <git command> #pass through to git, works on the note repo.

Notes are stored in ~/.notes, but this can be changed with the -d flag. The -c flag will clean out the current repository.

# Will support…
The index will migrate to a real database, but for right now, I'm just pickling dictionaries. This will have some scaling problems with very large note databases (the -d flag is a good way to avoid that problem).