---
title: "The flexy things"
date: "2026-03-14"
description: "On agents, interfaces, and workflows."
---

LLMs are a cheaper intro to automation, but will eventually build themselves out of many exchange roles. 

When it comes to business, I believe in ruthless automation of undifferentiated heavy lifting. 

What are some good examples of this? You ship software, but haven't invested in using a pipeline that deploys your code throughout environments and qa's it automatically at each stage. So you hire DevOps engineers to do this on behalf of your engineers. 

The above example has multiple failures, but the most important failure is one of process. Simply, no one sat down to write a binding workflow that would constrain how software was deployed. Maybe they looked at the QA process and decided that some commits just needed higher validation than others, and there was no reliable way to signal this. Or more likely, a few different engineers with good inuition looked at this, emoted "are you f*** kidding me?", but lacked the tools and enablement to go and establish it. 

Another example: security engineers. In an organization who have decided they will to operate from principles of least trust, all incremental access to resources must be brokered by a centralized agent who says "yay" or "nay". The process looks the same. Engineer submits a request, gives a valid reason. The security engineer looks at the request, reads the reason, and then looks at their seat in the org, perhaps their tenure, and maybe any context they have about them from interactions on slack and gives them access. 

The above example similarily has failures of process and clarity. What does the security engineering team really desire? They want access to resources to be granted with fine-grained policies. They want the grant of access to be logged and stored in a database. They want an ability to revoke access at any given time if they detect abuse. They want tools to detect abuse. The process here is straightforward but requires decision making. What are the resources in our universe we are applying a principle of least trust to? How are we ingesting access and usage logs? How do we detect compromise? Are there resources that we would only grant based on a minimal tenure or by access to understanding of how "good" an engineer is?

These are interfaces that exist between people and systems. But the universe of resources hasn't been programatically identified, so interfaces can't be established between them. Without interfaces we can not automate. For instance, an access decision based on the standing of the engineer would require understanding - what teams have they worked with in the past? what codebases do they commit software to? have their managers rated them in good standing in performance reviews? is this a special hire by the ELT who needs to move fast? does their manager approve?

Agents today, however, can precisely work with fuzzy interfaces. Said differently, they can:
* take the security request
* read the reason for access
* reason about the resource and its knowledge and confidentiality boundaries
* pull the performance reviews and determine standing
* pull the codebases the engineer commits to
* use slack APIs to pull an interaction graph for the engineer
* send a request to the manager for approval
* put this all together to write a one sentence recommendation to a security engineer with all the artifacts above tracked


An agent could also be used to:
* Build a tool that runs nightly that builds a graph of engineers and the codebases they commit to
* Build a tool that runs quarterly to refresh an internal list of engineers and their standing
* Build a tool that catalogues current and past employees and the access to resources they have
* Build a tool that analyzes slack data and builds a graph of engineers and their interaction points between teams
* Build an automated approval tool that reads through all of these systems, and deterministically applies a yes/no judgement. If yes, the engineer is automatically approved. If no, onto a human for review.


Agents will be used for the flexy bits to start, because it immediately overcomes the sin of not establishing a proper interface. A faithful engineer or two may build this agent. The demo of it working will immediately resonate with and please leadership, as well as the security team ICs and engineering teams. 

But the flexy thing here should just be the wedge. If the agents are truly going to be a country of geniuses in a datacenter, then I pose they will see that this problem can be reduced from a fuzzy one to a non-fuzzy one. That it is ripe to be solved with a deterministic workflow. 

The alternative is investing into a harness of agents. One agent QA's the other agents work. A third agent evaluates the false positive and false negative rate and makes adjustments to both systems automatically. In the short term, the inference cost is minimal. But in the long term you're allocating headcount to solve a problem that can be automated. It's just an LLM head instead of a human one.

I see this as a parallel to computer science theory. Those familiar with CS theory know that theorists like to play a game called reduction. I.e. can a certain problem be mathematically shown to reduce to a known problem if you make some transformations to it? If it can, then the problem is solvable with the same set of tools that the other problem can be solved with. 

What fuzzy problems can't be reduced to deterministic problems?

There are certain problems where the cost of establishing the interfaces necessary is too high, because to appropriately achieve the outcome you need, you will have to enumerate every single input and output of the system. A good example of this is a task that junior investment bankers and consultants are familiar with: building strategy decks. You need to outlay information in a reasonably defined format, but the amount of information is always different enough, the logos of companies always different enough, the amount of key things to highlight always different enough. You end up with a different amount of slides, a different amount of logos and analysis text per slide. And that's just with building the first draft, before your MD hits you with 5 rounds of comments at 1am.

It's possible, but the cost of establishing it is high. Perhaps the highest cost is being able to establish a language of design that can capture all the ways that the MD's judgement for layout, information variety, and information density can be captured.



