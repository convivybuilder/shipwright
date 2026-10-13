<!-- authorship: human -->
# Jay's tips

I created Convivy Builder as a byproduct of using long-lived Claude sessions, hosted on a remote personal server, to develop projects bit-by-bit over time.

## Why use long-lived projects

Most of the things many of us work on are long-term projects, even if we often tackle only a bite at a time.

If you develop software, you're familiar with the process. You have a list of things that need to be done, you take on one or two of those things, you test out your changes, tweak them until they work properly, merge those changes into the production code base, then move on. That sequence may take a few sessions. An incremental product release often consists of dozens or even a hundred of those sequences.

Applying this approach to work in other fields is helpful, when you start using agents. If every Monday you give your boss a breakdown of what you accomplished the previous week, you can make this a long-lived project with an agent. You create an ongoing session for your weekly report, work with the agent to make a system for capturing what you do without you having to log it, and then ask it to automatically create and submit the report every Monday. Your involvement becomes occasional chats with the agent to fix things that go wrong or make enhancements to improve the system.

One of the engineers I work with started a project like that earlier this year, and then it spread across our team. Then I started a project that captured all of those reports and made a digest of the team's activity each week.

At the end of each quarter, I am always asked to provide statistics on what we worked on, how much it cost and how much revenue that work enabled. Suddenly, because of the existence of the weekly digests, I found myself able to make a long-lived project out of *that* work, capturing the weekly digest of what we did, and comparing it to numbers from our sales side, and synthesizing the data. 

Now, assembling a report that previously took most of a week, I do -- or, as I joke, "I" "do" -- in minutes. And as part of the automation, the data gets put into a nice-looking presentation as well. 

This is a boring example, but let's face it, for most of us, we have a certain amount of boring work. Building a system to automate it and do a great job is way more fun than doing that work, and it's also very efficient.

Convivy Builder makes it really easy to turn any kind of knowledge-based work into long-lived (but mostly dormant) agentic projects, and keep them organized once you've built them.

## Fun projects

Principally I use builder to create software. I prefer it to any development platform I've ever used. Now that it's my primary system for making stuff, its reach has expanded too. Since the typical setup includes a server that can serve content privately over the Tailnet, it's easy to build a web app for any purpose.

Here's some fun, non software-development projects I've started and continue to use it for:

* **Trip planning**. The plan becomes a live app I use, as typical, to document my itinerary (here's your plane, catch a cab to the airport by this time) and store and organize recommendations people have given me, plan some meals, and so forth. I leave a session handy in Builder, and then, when I think of an improvement to the app ("can you add a map link to every eatery, that opens in Google Maps and shows the route from my hotel") or new information to include ("my friend just gave me his list of favorite coffee shops in the city"), I just have the agentic crew add it. During the trip, I have a place to upload notes and photos, and the end results can feed my own recommendations to friends, or just notes for myself for later.

* **Hobbies and Activities**. It's hard to keep track of the minutiae of the things I know are important, in say, tennis. What strings do I use, and when do I need to change them? String-changing time depends partially on how many hours I've played since the previous string change, which is hard for me to keep track of. It's trivial, though, to make an app with Builder to note what strings I use for what racquet, log how many hours I've played each week, and generally store things I want to work on or have successfully worked on, and to investigate possible changes I might make and then make notes of what I want to try out. Basically any activity where some kind of journaling or notes makes the experience more enjoyable, is made easier by building an app for it and improving the app over time.

* **Finances**. OK, it's not exactly *fun*, but still. I spend a couple months every Spring finding and classifying all our previous year's expenses to organize a spreadsheet to send to our tax preparer. This year, I created an app that does the bulk of that work, and just surfaces questions about the items it couldn't obviously classify. Now, not only will I be able to send our tax preparer a packet in January without laboring too hard over it, I'll have a rough draft done in early November so if any changes are suggested for the current tax year, I can make them.

These are personal-level projects, but there are (more complex) versions of these types of projects that a lot of folks can do at their work. And most of them, I've never thought of and don't know anything about. But if you, I don't know, design and build custom wood-fired saunas, I'm sure there's at least a few ongoing parts of your work that could be turned into agentic projects requiring less of your time and providing highly optimized output. I've done a whole virtual remodel of a house in Sketchup, in about 5% of the time it took me to do pre-LLM. There's probably something for you.

## Jay's Tips

Now we get to my actual tips on how to get the most of your early experiences with Convivy Builder.

### Ask the Steward

Tell the Steward what you have in mind. Bounce some ideas off it. Brainstorm. Ask it to create a project and crew for you. If your project doesn't need a crew, at least give it its own CO (Crew Organizer). As the project grows a crew may develop.

### If you want it, make it so

We get used to using a product, and when it doesn't do exactly what we want, we shrug our shoulders and say, oh well. With Builder, there's a better way. Just tell the Steward or your project's CO, I want it to work this way. You may get questions back, or considerations to think about. Engage, and by the end, you'll probably have exactly what you want. Sometimes it's startling what you can do quickly with this tools. Don't be confused -- you can basically build anything you can imagine (if it works in software) with this system.

This applies equally to Builder itself, and to the projects you're working on. Everything is more malleable now than it has ever been.

### Start with a Bead

If you have a simple ongoing project like my tennis app, you probably don't need a Bead for it. But as soon as you have a vision of something more complex, it's worth spending the time to define exactly what you are trying to build. Work with the Steward and the project CO, let them use the `/bead` skill, and do your best to get it right. Don't worry though if you have to change it later, it's easy.

Working with a Bead will help keep sessions on track in the future.

### Keep your decisions accurate and well-documented

When we move fast on human teams, we often eschew bureaucratic overhead like recording our decisions, because we can keep track of that in our heads, and we don't want to spend the time. The nature of LLMs is that they don't have actual biological memories, instead they have written text in the form of instructions and reference material. So if you want them to make decisions that serve your vision, you have to write all your decisions and details in the very documents they will later reference.

Much more of my time is spent on creating and maintaining a ledger of decisions and goals, than on making the sure the code itself is written a certain way. The code either works or it doesn't. The documentation, if it doesn't hang together and express itself correctly, you'll find out in ways that you may find frustrating.

### Use the Course

I love good project management tools, although I have never fully cottoned to Jira just because its power comes at the expense of being somewhat heavyweight for smaller teams with less PM capability. Now, when you move at full throttle in agentic development, the overhead of any external tool is challenging to justify. 

That's why Builder includes its own basic project management system, that is fully integrated into the world of the agents.

* The Bead describes where you are going.
* Your Course is how you get there.
* Each item on the course is an Epic (the term Epic comes from software development processes, we lose the nautical motíf for a moment here).
* An Epic is composed of work items which, when completed, will close the Epic
* The completion of an Epic (or a combination or Epics, if you designate it) marks a Waypoint on the Course.
* Progress toward the Bead is measured by how many Waypoints you pass
* Any course corrections (bugs, small changes) are made into work items stored on the Corrections Queue until addressed.
* It's easy to change the Bead when you change what you want, to add Epic when you realize you need them, or add work items including corrections as required.

This is lightweight, which is nice.

More importantly: everything is stored in the Library, specifically in the Chart House, and handed to the agents when they are individuated (literally, they are brought into being as individuals from the clay of raw materials that includes the decisions you've made and recorded). This way, agents always know what they're working on and how it fits into the goals of the system. The system also allows for many separate agents to work in parallel without colliding, by requiring agents to *check out* the epic they're working on. If an epic isn't checked out, an agent is free to check it out and work on it; if it checked out, they need to wait and work on something else in the meantime.

How the agents are interacting with the system is always visible in Deck (in the cockpit), and all the contents are visible in Orient (in the Chart House section).

### Don't let the agents merge PRs

This may be controversial, and to be clear, merging all your own PRs is not a requirement. You can YOLO the everloving hell out whatever you build, and have the agents go to TOWN. It probably works fine to just let them cook. 

(Note, if you're not a software developer, you may not know what PRs are. The abbreviation is short for "Pull Request", a term which is equally opaque. A PR is a batch of changes to code or documentation, that you've made and tested out on your own environment, that you want to move to the "official" product.)

Furthermore, you don't need to use PRs, or Github, or write software to make cool things in Convivy Builder. But if you do use it to build software, you will probably use GitHub and make PRs. For those who do, Convivy Builder has a default configuration that the agents will not merge PRs -- they will leave that for only you to do.

Here's why I merge all my own PRs and why I recommend you do it too. The biggest challenge when project development moves at high speed and high volume is what has become known as "cognitive debt". Which is a way of saying, it's hard to keep track of WTF is going on. 

The big service you get from merging every PR is knowing, every time any change goes live, more or less what it is.

When I merge the PR, I don't actually read the description text in the PR body -- the agents write them, it's a mountain of words -- and I certainly don't read the code. I look at the title, think about how it interacts with the system as it is, and confirm my expectation of what is happening. Then I smash the green button. Over time I have a reasonably good idea of where my project stands.

(Side note: Some folks will find the idea of not reading code controversial. IMO, code is a way for people to communicate to other people how a bit of software works -- it's an exercise in humans writing for humans. As a longtime professional writer of both prose and code, I just don't find code itself interesting or relevant any more. I find prose more relevant than ever. Your mileage may vary, and I might change my mind later. Who knows.)

Anyway, take a minute to read the title of PR, you'll be less like to get confused about things later. And, if you do get confused about where things stand, just ask the CO. It's fine.
