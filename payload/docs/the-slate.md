# The Slate

Each crew has a Slate: a sheet in Deck where the crew's session leaves the questions it needs you to
answer, and where you keep notes to give that session when it reaches a good moment to hear them.
Like a bead, which is a project's short description of where it is going, this page describes
Builder as it is designed to work, and the system is still catching up to that design.

That first sentence uses three more of Builder's own words. A crew is one project and everything working
on it. A session is the conversation with Claude, an AI model, that does a crew's work. Deck is the
desktop application where you pilot each project hands-on.

The name comes from the slate kept by a ship's helm, where the officer of the watch chalked events
as they happened and copied them into the log at the change of watch.

## Why it exists

The Slate solves two small problems that add up over a working day.

**Questions get lost.** A session working for you stops to ask things: which of two approaches you
prefer, whether a change may go ahead, what a word in your request meant. It asks in the middle of
its work, and by the time you look, the question has scrolled far up the conversation or the session
has moved on to a fresh one. The Slate keeps every open question in one place, written to make sense
on its own, so you can answer them on your own schedule, one at a time, while the session carries on
with other work.

**Your own thoughts interrupt.** You think of things to tell a session while it is busy. Saying
them at once pulls it off the thread it is following. A note on the Slate waits until you send it.

## Questions the session asks you

The crew's session puts a question on the Slate the moment it first asks it. Each question appears
as a card. It is written in plain English, with no reference numbers or shorthand, so it still reads
correctly days later.

To answer, write your answer on the question's card and press **Send**. The session receives your
question and answer together as one message. A turn is one stretch of the session's work between
your messages. If the session is in the middle of a turn, the message waits until the turn ends, so
sending never interrupts its work.

What happens to the card next depends on your answer.

- **When your answer settles the question**, the session closes it, and the card leaves the Slate.
- **When your answer opens a discussion**, the session replies in the conversation and the card
  stays on the Slate, marked answered. You can change your answer and send it again.
- **When you answer in the conversation instead**, the session closes the card itself.

Deck shows, beside each crew, how many of its questions are waiting for you, so you can see where
you are needed without opening every project.

## Notes you hold for the session

Start a note on the Slate whenever something occurs to you. It stays a draft, which you can edit or
delete as often as you like. When the session reaches a break point, a natural pause between pieces
of work, press **Send**. The session receives the note as a message, and the card leaves the Slate.

The session never edits, sends or deletes your notes. They are yours until you send them.

## Where the Slate is kept

Each crew's Slate is a file on the machine that runs the crew, in a folder under `~/.local/state`
that only the account Builder runs as, and an administrator, can read. In that path, `~` stands for
the account's home folder. A session sometimes rolls over, handing its work to a fresh conversation.
The Slate lasts through that, because it belongs to the crew and not to any one conversation.
It stays on that machine, and Deck reads and writes it there over SSH, the same connection it runs
your sessions through.

The session works its side of the Slate with the `co-ask` command, which the install puts on its
path, meaning the session can run it by name. You work yours in Deck.
