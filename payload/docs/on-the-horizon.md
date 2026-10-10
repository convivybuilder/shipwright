<!-- authorship: human -->
# On the horizon

Convivy Builder is itself only partially built -- perhaps perpetually so. At some point in late summer 2026, it crossed a threshold of becoming complete enough to me (Jay) that it became the only development platform I want to use. And thus it became the platform used to build itself, along with some other things.

Because I find it helpful in its current state, and others might find it helpful too, I'm sharing it despite it being far from perfect. It has some UI wonkiness, a couple features in Deck that don't really make sense (I have no idea what "Promote to crew..." means exactly and how it differs from pinning a crew to the rail), and some important configurations that haven't shipped yet -- specifically, 1) sessions and the Keel running on a Linux server instead of a Mac server, and 2) multiple user accounts for different types of agents, as a way to control each agent-type's permissions.

Finishing those issues is first on the roadmap.

After that, here's what I see as the higher priority items I'll likely work on next.

## A mobile Deck

Currently I use Claude "remote control" on the Claude mobile app to shepherd sessions along on my phone. This works, but 1) I don't get access to all the highly productive features in Deck such as the Slate, the Course, and the PR queue, nor the session stats that I use to stay on top of costs and context; and 2) it means all of the session text passes through Anthropic's servers. Not a huge security risk, probably, but why expose more than is required?

The obvious move here is a good iOS version of Deck that brings over the most useful features of Deck. Deck is a Swift desktop app so I'm hoping the port doesn't require sacrificing any key elements.

Once an operator can access their sessions from two Deck apps at the same time, it opens the door pretty wide for...

## Multiplayer sessions

This was one of the first use cases I heard from a friend; they want to use multiplayer sessions to bring along their coworker/s both with the target projects they're working on, and on how to get the most from an agentic development platform. There will of course be some trickiness here in terms of which operator has permission to do what, but I think pretty resolvable by creating an admin/owner role, and tons of opportunity for exploration.

## Enterprise scale

Convivy Builder is architected to work at enterprise scale -- the Keel is meant to serve many operators running many sessions over a large organization, collaborating on multiple projects across one or more repositories.

Of course, actually deploying Builder in that environment will reveal where the current implementation can't work at that scale. So there will be some (a lot of, I'm guessing) work in making this real.

## Modular parts

In my opinion, the most promising part of Convivy Builder is the way the parts -- the Library, the Chart House, the Bosun, the Individuator, and the sessions -- work together to keep agents and projects on track and moving forward. That said, none of the individual modules are particularly thoughtfully constructed internally. A Library module with top-notch indexing and search capability would surely bring token cost down and results quality up. I'd like to clearly define each module by its interfaces and requirements, to make it easy for users to drop in their own components -- probably specifically the Library more than any other -- and still work seamlessly.

I suspect this goes hand-in-hand with enterprise scale, since it will be those use cases where users need customization to index and access their knowledge base and memory artifacts.
