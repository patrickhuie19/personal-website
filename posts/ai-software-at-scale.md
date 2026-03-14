---
title: "AI Software At Scale"
date: "2026-03-14"
description: "Thoughts on AI in SDLC at established software engineering organizations"
---

Software engineering is writing code that will scale in several directions. It will scale to many customers. It will scale to be written by many internal maintainers. That last point is important. 1 extremely good developer working on a project to ship an POC or demo for leadership could crank something out over a weekend. But productionizing it, making it integrate with the current suite of offerings, and setting it up to be worked on by many contributors is the time consuming part.

Most successful mid to large businesses started over 10 years ago. Writing software back then wasn't all that fast, so the relative cost of deploying it wasn't so painful. And, when they had manual release processes, the cost of QA'ing the software was low. Deploy it to stage, run a script that performs CRUD operations across the 3 central entities of the system, press go. Onto the next feature.

Overtime, the number of features that need to be QA'd increase, as well as the number of environments the software is deployed in. You start winning global business, so you need to deploy across the globe. Customers want to be able to interact with your platform on web, mobile, cli. And as the business has grown, the monorepo has gotten massive, with 10k+ unit tests, 1000 integration tests. You run load tests and the most gnarly QA processes nightly rather than on the PR.

Each individual decision was well intentioned.

Now writing software is cheap, so the relative cost of deploying it is an order of magnitude higher than it was.

Let's put aside technology companies who have reached dominant market share in a space with few competitors and lucrative margins. Let's also put aside companies whose growth is constrained by technology supply, i.e. they have fundamental scaling challenges to address in their software architecture.

Companies who earn incremental revenue and market share from better serving their customers are product led growth companies. The cheapest way to better serve customers is by making intentional additions (and deletions) to the codebase. 

The cost of composing the diffs that make these new features is now much much closer to the cost of making a clear decision on how a current offering should be changed.

Writing software for product led growth has never been cheaper and faster. 

So, you've increased your ability to write software by 5-10x. Why is the velocity still the same?

The velocity is still the same, if not worse, because the review and deployment blockers, which you previously found ways to scale linearly with velocity (at best! often sub-linearly) by hiring a great devops person who shifted some tests to run in a higher env rather than a lower env because we take more time to monitor changes in higher envs anyways, is now the bottleneck.

Let's start with the deployment problem.

The only good way to start with the deployment problem is to take the view that, barring emergencies, there is absolutely no room for humans in the loop. The absolute last action a human should take is hit the big green merge button.

After that, it should be automatically deployed by pipeline software. Whatever your concern is, I wager that it can and should be solved by your pipeline. Yes, for your very complicated web app, you can now have an AI agent use MCP to click around on a device emulator. Yes, even if you don't deploy the software you write, you can ship tooling and scripts that will automatically pull whatever artifacts are needed from a container registry, package manager, or other binary host. Yes, when the software promotes from gamma to prod, and your oncall starts to get pages, the pipeline should automatically rollback to the last known good version, and mark that deployment hash as unsuitable for deployment in that env.

Use off the shelf tooling where you can. If you can reduce the problems that you solve as a business to the problems of a peer business, and you know they use a pipeline, you can use a pipeline too. 

AWS obsessively uses pipelines in its software, and AWS operates a highly available developer platform with control plane and data plane APIs, complex configuration management, deployments over different environments and over a permutation of different security concerns. I know this because I worked there.

For the vast majority of software engineers reading this, your business reduces to AWS. So, please do yourself, and your team a favor, and use a pipeline!

Try as much as possible to not build it yourself. Use off the shelf tooling.

The review problem is a harder one to solve. When we look at reviewing code, we're looking at a fuzzy problem. A reviewer reviewing your code is looking for some basic things - like are your variables name reasonable, have you abstracted the right bits, will this code degrade the experience or performance for any users, etc. Some of those things are deterministically testable, and need to be part of your CI gates to merging a PR to main. i.e. lint. i.e. unit tests. i.e. integration tests.

Some of the things in a review aren't deterministically testable. Like a reviewer is going to start extracting logic to decouple an interface between teams, and the change you are making will block that extraction. Or, take the element of style. There are many ways to code the solution to a problem, and in software we still believe in individual expression, so things like whether you drill a channel or a relayer struct through your interfaces will receive different judgements from different reviewers. 

The way, imho, to fix this is for each reviewer to have a review agent that they deploy from their devspace. The agent has a list of criteria for review that the individual reviewer cares about, and applies it to the PR. 

In the long run, if we achieve Dario's vision of a Country of Geniuses in a Datacenter, I hope that those geniuses will spend a lot of compute cycles on expanding the reach of autogenerated software. Today, we use autogenerated software in networking protocols like grpc. You define the interface, and the tooling takes care of generating the server and client code that send the bits over the wire. We can certainly expand that - you have a go http server you're defining the performs CRUD operations? Use an autogenerated library, with some configurations, that can express the basic CRUD routes.

One important part of these autogenerated libraries is they have to incorporate the concerns of scale we discussed earlier. For instance, if you are able to use the auto-generated code up until you need a read replica for an analytics job that runs nightly, then the abstraction handling and power of the autogenerated library is not good enough. Similarily, the autogenerated code should be able handle the additions of new core business entities. 

The natural side effect of this is constraint. I'd argue that this is a good thing. So many software engineers are re-inventing the wheel each time to solve the same problem. You want a server with one DB that stores artifacts to blob storage? Sweet, there's no reason why we shouldn't be able to autogenerate that code in the most popular languages and the choice of a few standard libs.

That's why these LLMs are so insanely useful to begin with. They can mattern match a problem and spit out a diff that solves it with some certainty. Solving it with 100% certainty requires constraining what the autogenerated software can do. 

I think prior to LLM's few software engineers were willing to give up their individual taste in the code that they were writing and reviewing. But as agents write more and more code, they've already given that up, so the transition to more autogenerated code will be less painful.

If the autogenerated libraries are able to achieve the power I'm thinking about here, then the review burden of software will decrease by orders of magnitude. You don't review the autogenerated clients and servers the grpc-go library creates. You only review the interfaces configured in proto3 language.