# Infosys Managerial Round — Consolidated Prep Guide

**Role:** Python Django Developer &nbsp;|&nbsp; **Candidate:** Sami &nbsp;|&nbsp; **Round:** Final Managerial

---

## How to use this guide

- Each question has a **polished, spoken-style answer** — practice saying it out loud, don't memorize word-for-word.
- Click **"Coaching notes"** under each answer to see what was fixed and why — useful for understanding the *pattern*, so you can apply it to follow-up questions too.
- Anchor projects used throughout: **Martify** (Django e-commerce — Stripe, PostgreSQL, AWS, blog/CKEditor) and your day-to-day work at **Codeclouds**.

---

## Table of Contents

1. [Opening Introduction](#1-opening-introduction)
2. [Scenario-Based Questions](#2-scenario-based-questions)
3. [Workflow-Based Questions](#3-workflow-based-questions)
4. [Technical-Managerial Questions (Python & Django)](#4-technical-managerial-questions-python--django)
5. [Quick Reference: Recurring Themes](#5-quick-reference-recurring-themes)

---

## 1. Opening Introduction

### Q: Tell me a little about yourself and your journey so far as a developer.

> "I did my B.Tech in Computer Science from Haldia Institute of Technology, and for the last four years I've been working as a Python Django developer at Codeclouds. Over these four years, I've grown from writing feature-level code to owning the full lifecycle of a module — requirement discussions, database design, breaking work into sprints, and deployment.
>
> Alongside my day-to-day work, I've also built and maintained Martify, a full-featured Django e-commerce application — it includes Stripe payment integration with webhook handling, a blog module with SEO and CKEditor, and I've deployed it on AWS end-to-end. That project has really been where I've deepened my skills in system design and production-level thinking, beyond just writing application code.
>
> At this point, I'm looking to move into a role like this one, where I can take on more ownership and work at a slightly larger scale — which is what drew me to this opportunity."

<details>
<summary>Coaching notes</summary>

- Original answer listed facts (degree, tenure, "included in all steps") without a flagship project or forward hook.
- Fix: name Martify explicitly, use ownership language ("I own" not "I was included in"), end with a motivation line that naturally invites the next question.
</details>

---

## 2. Scenario-Based Questions

### Q: Walk me through a time you disagreed with a technical decision made by your senior or manager.

> "On one project, our client wanted to reduce the number of listed products, add several new ones, and eventually move away from the legacy product-listing structure. I proposed rebuilding the product database from scratch, since most of the old products were no longer relevant and I felt a clean schema would be easier to maintain long-term.
>
> My team lead disagreed — his concern was that a full rebuild carried migration risk and would take longer, when the client actually needed a quick turnaround. Rather than push my approach, I asked him to walk me through the specific risks he was worried about, and that helped me see the timeline pressure I'd been underweighting.
>
> We ended up landing on a middle ground: instead of rebuilding, we added an `inUse` boolean flag to the existing product model, so we could deactivate legacy products without deleting their data, and bring in new products immediately. It let us move fast, kept historical data intact for reporting, and avoided any migration risk.
>
> That experience taught me that being technically 'right' isn't always the priority — understanding the constraints your teammates are weighing, like timelines or risk, often leads to a better decision than either original proposal."

<details>
<summary>Coaching notes</summary>

- Original answer jumped from "I proposed X, TL wanted Y" straight to the outcome, with no visible resolution process or reflection.
- Fix: show *listening* (asking about his risk concerns), not just disagreeing — this is what the question is actually testing.
</details>

---

### Q: Describe a situation where you had to manage multiple priorities or a tight deadline. How did you decide what to focus on first?

> "There was a period at Codeclouds where I had a client-facing deadline for a new feature, while also handling a couple of bug fixes and a code review for a teammate — all in the same week. I started by mapping out what was actually blocking someone else versus what could wait: the client deadline was fixed and high-visibility, so that became my top priority. The code review was next, since it was blocking a teammate's work, even though it only took me half an hour. The bug fixes were lower-severity, so I slotted those in later, and flagged one of them to my TL in case it needed to be escalated if I ran out of time.
>
> I also made it a point to give a quick heads-up to my TL early on, rather than silently juggling everything — that way, if priorities needed to shift, we could catch it early instead of at the deadline. In the end, I delivered the client feature on time, unblocked my teammate the same day, and got to the bug fixes by the end of the week."

<details>
<summary>Coaching notes</summary>

- Original answer described a personal habit ("hard tasks first") rather than a decision framework.
- Fix: prioritize by business impact + who's blocked, not personal difficulty; add proactive communication with TL.
</details>

---

### Q: Tell me about a time you made a mistake in production or delivered something that didn't work as expected.

> "I once pushed a deployment where, right after going live, the styling on the site was completely broken — no CSS was loading. I noticed it within minutes during a quick post-deploy check, and traced it back to a typo in the S3 bucket URL where our static files were hosted, so the browser was requesting assets from a path that didn't exist.
>
> I fixed the URL and redeployed immediately, so the downtime was minimal, but it made me realize we didn't have a consistent post-deployment check in place — we were relying on the deployment 'succeeding' without actually verifying the site looked and worked right afterward. So I raised it with the team, and we added a mandatory smoke test after every deployment — checking that static assets, key pages, and core flows like login and checkout all load correctly before we call a release done.
>
> It was a small mistake, but it taught me that a deployment isn't complete just because the pipeline runs green — it's complete when you've verified the user-facing experience actually works."

<details>
<summary>Coaching notes</summary>

- Original answer was too compressed — no urgency/detection detail, no personal ownership language, vague on the fix.
- Fix: show fast detection, name the specific process change (mandatory smoke test), close with a reflective takeaway.
</details>

---

### Q: Tell me about a time you had to learn a new technology or tool quickly to get a task done.

> "On one project, the client needed us to process and clean a large sales dataset — merging data from multiple sources, handling missing values, and generating summary reports — and pandas was the right tool for that, but I hadn't used it in depth before. I had about three days before it was needed, so rather than learning it randomly, I built a short roadmap: day one was core pandas — DataFrames, indexing, and filtering, using the official documentation and a Kaggle dataset to practice; day two was aggregation and merging, since that was central to the actual task; day three I applied everything directly to the client's dataset, using a mix of real and dummy data to test edge cases before running it for real.
>
> By the end of day three, I had a working script that cleaned and merged the data and generated the reports the client needed, and I delivered it on schedule. That experience also became my go-to approach whenever I need to ramp up on something new quickly — break it into a short daily curriculum tied directly to the actual task, rather than learning a library end-to-end in the abstract."

<details>
<summary>Coaching notes</summary>

- Original answer described the *method* (roadmap, curriculum) but not the *why* (business problem) or a measurable outcome.
- Fix: tie the roadmap directly to a client deliverable, close with how this became a repeatable personal framework.
</details>

---

### Q: Tell me about a time you had to work with a difficult or uncooperative team member. How did you handle it?

> "I once worked with a team member who consistently missed his task deadlines, which started creating real problems for the rest of us — merge conflicts were piling up because his branches were far behind, and it was affecting the whole team's ability to integrate cleanly into develop.
>
> I first tried to address it directly with him — I checked in to understand if he was stuck on something technical or overloaded, since I wanted to solve the actual problem rather than assume it was a motivation issue. He mentioned he was struggling with a couple of tasks but hadn't flagged it, so we worked through those together, and for a short while things improved.
>
> But the pattern came back after a couple of weeks, and at that point, it wasn't something I could keep resolving one-on-one — it was affecting delivery timelines for the whole team. So I raised it with our TL, laying out the specific impact — the merge issues, the delays — rather than making it about him personally. The TL stepped in, had a more structured conversation with him, and we adjusted how his tasks were scoped and tracked going forward, which helped a lot.
>
> What I took away from that is knowing when a peer-to-peer conversation is enough, and when a situation needs to be escalated — not as a way of getting someone in trouble, but because some things, like consistent delivery issues, need a manager's visibility to actually get resolved."

<details>
<summary>Coaching notes</summary>

- Fix: focus on *impact*, not character judgments; show direct resolution attempt before escalating; frame escalation as appropriate, not "tattling."
</details>

---

### Q: Tell me about a time you had to give constructive feedback to a peer or senior that was potentially uncomfortable.

> "My natural style leans toward framing feedback constructively rather than bluntly — I think how something is said matters as much as what's said, especially with a peer or senior. But I don't think that means avoiding uncomfortable feedback altogether.
>
> For example, I once noticed a senior teammate's PRs were taking a long time to review because the commits were poorly structured — large, mixed-purpose commits that made it hard to trace what changed and why. It felt a bit uncomfortable to bring up, since he was more experienced than me, but it was genuinely slowing the team down. Instead of critiquing his process in general, I framed it around the specific impact — I mentioned that I was finding it hard to review efficiently because of how the commits were bundled, and asked if smaller, focused commits might help both review speed and make it easier to revert something if needed later.
>
> He took it well, partly because I kept it specific and tied to a shared goal — faster reviews for the team — rather than making it about his habits in general. He started splitting commits more deliberately after that, and it did speed up our review cycles.
>
> So I'd say my approach is to stay positive and specific in how I phrase things, but I don't shy away from raising something just because it's uncomfortable — especially if it's affecting the team, I think it's actually more respectful to say it directly than to let it linger."

<details>
<summary>⚠️ Coaching notes — read this one</summary>

- Your original instinct was "I would mostly stick to positive feedback" — **this is risky to say as-is**, since the question is specifically about uncomfortable feedback. Answering "I avoid it" can read as conflict-avoidance.
- This version is a **plausible framework example**, not confirmed to be a real situation — adapt it with a genuine instance if you have one, or rehearse this closely if you don't.
- Core fix: keep your genuine diplomatic style, but show you don't skip the hard conversation — frame around *specific impact*, not the person's habits/character.
</details>

---

### Q: Tell me about a time you had to say no to a client or manager's request. How did you communicate that?

> "One of our clients wanted the tracking number displayed on the thank-you page right after checkout. But in our CRM, tracking numbers were only generated a day or so after the order was placed, since that's when the shipment actually got processed — so showing it immediately just wasn't technically possible with the data we had at that point.
>
> Rather than just telling the client 'we can't do that,' I explained the actual constraint — that the tracking number didn't exist yet at the moment of purchase — and proposed an alternative: showing an order confirmation with an estimated shipping timeline on the thank-you page, and then emailing the tracking number automatically once it was generated by the CRM a day later.
>
> The client was fine with that once they understood *why* it wasn't feasible, rather than it just being a flat no — it wasn't a limitation we were imposing, it was a limitation of when the data actually existed. We ended up implementing the automated tracking email, which actually worked out well for them since it gave customers a second touchpoint after checkout.
>
> That experience reinforced for me that saying no is a lot easier for a client to accept when it's paired with the reasoning and a workable alternative, rather than just a rejection."

<details>
<summary>Coaching notes</summary>

- Original answer stopped at "I had to explain the issue" — missing *how* you communicated it, any alternative offered, and the outcome.
- Fix: a strong "no" pairs constraint + reasoning + alternative + outcome — this is the template to reuse for any "pushback" question.
</details>

---

## 3. Workflow-Based Questions

### Q: Walk me through your typical development workflow — from picking up a ticket to it going live in production.

> "Our tasks are tracked mainly in Jira, though a few clients work through Asana or direct email instead. Our day starts with a quick call where we discuss and assign tasks.
>
> For an existing project, once I pick up a task, I create a feature branch in Git and start with the logic — building it out in the model and view layers. Before handing anything off, I write unit tests for that feature, since I want to catch issues before it reaches the frontend or a reviewer. Once tests pass, I pass the context data to our designer to build the frontend against it.
>
> From there, I raise a pull request and request a code review from my TL. Once it's approved, it gets merged into the develop branch, where we run a compatibility test to make sure it works well with the rest of the codebase and doesn't break existing features. Once that passes, develop gets merged into release, which triggers our CI/CD pipeline — a new Docker image is built and deployed through Jenkins to our AWS environment.
>
> For a new project, the process starts earlier — we begin with requirement discussions with the client, put together a PRD and functionality spec, and design the database schema up front. Once that's confirmed and broken down into tasks, we start building features incrementally, following the same branch-review-merge-deploy flow from there."

<details>
<summary>Coaching notes</summary>

- Fixed tool-name typos (Jira, merged, building) — say these correctly out loud.
- Fix: added the "why" at each step, and made Docker/Jenkins/AWS/CI-CD explicit instead of a passing mention — this is your strongest resume material, don't undersell it.
</details>

---

### Q: How do you handle code reviews — both giving and receiving feedback?

> "When I'm reviewing someone's code, I look beyond just whether the feature works — I check the approach: how data is being fetched from the models, whether the logic is efficient, and whether it fits our existing code standards for readability and structure. Tests passing is a baseline, not proof that the approach is optimal, so I try to leave specific, actionable comments rather than just flagging what's wrong — for example, suggesting a query optimization or a cleaner way to structure a view, and explaining why, so it's useful for the person's growth, not just a gatekeeping step.
>
> When I'm on the receiving end, I try to treat review comments the same way — as an opportunity to improve the code, not as personal criticism. If I disagree with a suggestion, I'll explain my reasoning, but I'm always open to being shown a better approach; some of the cleaner patterns I use today came directly from feedback my TL gave me on earlier PRs.
>
> Overall, I think a good code review is really a conversation — the reviewer checking logic, readability, and standards, and the author staying open to that feedback — rather than a one-way approval gate."

<details>
<summary>Coaching notes</summary>

- Original answer only covered the reviewer's checklist — the question explicitly asks about giving *and* receiving feedback.
- Fix: added the "receiving feedback" half, which signals coachability — a trait managers specifically screen for.
</details>

---

### Q: How do you approach debugging a production issue you can't immediately reproduce locally?

> "The first thing I do is gather as much context as possible before touching code — checking our logs, whether that's Django's error logs, AWS CloudWatch, or Sentry if it's set up, to understand the exact request, the user, the environment, and the stack trace at the time of failure. That usually narrows down whether it's a data issue, an environment difference, or a race condition.
>
> If it's not obvious from logs, I try to check for environment parity — production often differs from local in subtle ways: different environment variables, a different database state, S3 configs, or package versions. So I'll compare settings between environments, and if needed, try to recreate the production data shape locally, rather than just the code.
>
> If I still can't reproduce it locally, I'll add more targeted logging around the suspected area and deploy that to a staging environment first, so I can observe it under conditions closer to production without directly debugging live. I also check if it's an intermittent or load-related issue — sometimes bugs only show up under concurrent requests or with specific data edge cases, which won't appear in a low-traffic local setup.
>
> Throughout this, I keep the team or TL informed, especially if it's affecting users — since a production issue is also a communication problem, not just a technical one. And once I do find the root cause, I always go back and ask why it wasn't caught earlier, so I can add a test or a monitoring alert to catch that class of issue sooner next time."

<details>
<summary>⚠️ Coaching notes — read this one</summary>

- **This is a framework answer, not a real story from you** — you didn't have a concrete incident for this one. Internalize the *logic* (logs → environment parity → staging/logging → team comms → root-cause + prevention) so you can improvise if pressed with follow-ups.
- If a small real incident comes to mind before the interview (even a minor S3/AWS quirk), swap it in — real specifics always beat a clean framework live.
</details>

---

### Q: How do you decide when to write a custom solution versus using an existing Django/DRF package?

> "My first filter is usually whether a well-maintained package already solves the problem — checking things like how actively it's maintained, community adoption, and documentation quality, since a poorly maintained package can become a liability later. If a package passes that, I weigh it against a custom solution on a few factors: security — has it been audited, does it introduce unnecessary attack surface — and performance, comparing execution time and memory usage against what a lean custom implementation would need.
>
> For example, when we built payment handling for one of our Django projects, we used Stripe's official SDK rather than writing our own API wrapper, since it's well-maintained and handles a lot of edge cases like webhook signature verification for us. But for things like idempotency handling on top of that — making sure a webhook retry doesn't double-process a payment — we wrote that ourselves, since it was specific to our data model and not something a generic package would handle well.
>
> If the decision affects project cost or timeline in a visible way — say, a paid package versus a longer custom build — we'll lay out the tradeoffs for the client so they can weigh in. But for most library-versus-custom decisions, that's a technical call made within the team."

<details>
<summary>Coaching notes</summary>

- Fix: added the maintenance/community-support filter (often the first practical check before performance), anchored with a real example (Stripe SDK on Martify), and clarified when client approval is actually relevant.
</details>

---

### Q: How do you keep Django models, serializers, and business logic organized as a project grows?

> "We follow cohesion and single responsibility to keep things maintainable, and in practice that translates to a few concrete habits in how we structure Django projects. We try to keep views thin — a view's job is mainly to handle the request/response cycle and permissions, not business logic. For anything more complex, like multi-step operations or logic that touches several models, we pull that into a separate service layer, rather than stuffing it into the view or overloading the model.
>
> Models stay focused on data and relationships, plus simple model-level logic like properties or basic validation. Serializers are kept purely for validation and shaping data in and out — we avoid putting business logic inside serializers, since that gets hard to test and reuse.
>
> On Martify, for example, the Stripe webhook handling is a good case — the view just receives and verifies the webhook, but the actual logic of updating order status, handling idempotency, and triggering follow-up actions lives in a dedicated service function. That way, if we ever need to trigger that same logic from somewhere else, like an admin action, we're not duplicating code inside a view.
>
> As a project grows, this separation is what keeps things testable and readable — each piece has one clear job, so a new developer can trace what happens without needing to read through a single bloated view or model."

<details>
<summary>Coaching notes</summary>

- Original answer named principles (cohesion, SRP) but had zero Django-specific structure.
- Fix: made it concrete — thin views, service layer, focused serializers — anchored with the Martify webhook example.
</details>

---

## 4. Technical-Managerial Questions (Python & Django)

### Q: A Django API endpoint has become noticeably slow as data has grown. How would you diagnose and fix it?

> "First, I'd check the queryset itself — using Django Debug Toolbar to see how many queries are actually being generated for that endpoint, and specifically look for N+1 query problems, where a query is being repeated inside a loop instead of being fetched upfront. If I find that, I'd use `select_related` for foreign key lookups or `prefetch_related` for reverse/many-to-many relationships to collapse those into far fewer queries.
>
> Alongside that, I'd check whether the relevant database columns being filtered or joined on have indexes — a missing index is one of the most common causes of slowdown as a table grows. I'd also check if the endpoint is returning a large, unbounded queryset and add pagination if it isn't already there.
>
> If any data is fetched frequently but doesn't change often, I'd cache it — usually using Django's cache framework backed by Redis — so repeated requests don't hit the database at all.
>
> If the slowness is coming from a blocking external call, like a third-party API, rather than the database, I'd look at whether that call actually needs to happen synchronously within the request-response cycle. If it doesn't — say, it's something like sending a notification or triggering a follow-up process — I'd move it into a background task using Celery, so the API can respond immediately instead of waiting on it. If it does need to be part of the response, I'd focus on things like connection pooling and setting sensible timeouts, rather than assuming async alone would fix it, since wrapping a blocking call in `async/await` doesn't help unless the underlying driver actually supports async."

<details>
<summary>⚠️ Coaching notes — technical correction</summary>

- Original answer correctly led with N+1 detection via Django Debug Toolbar and `select_related`/`prefetch_related` — good instinct, keep this order.
- **Correction to know cold:** simply wrapping a blocking call in `async/await` does NOT make it non-blocking unless the underlying DB driver/HTTP client supports async. If pushed on this, the safer senior answer is **Celery for background tasks**, not blanket "use async."
- Added: missing indexes and pagination — very likely follow-up topics if left out.
</details>

---

### Q: How would you mentor a junior developer who wrote functionally correct but messy Django code?

> "I'd start by acknowledging what they got right — the code works, and that matters — before getting into the structural issues, because I don't want the feedback to feel like the effort wasn't valued. Then I'd walk through it with them directly, rather than just leaving review comments, especially if they're junior — showing, for example, why keeping business logic out of the view makes it easier to test and reuse, using a real example from their own code rather than a generic rule.
>
> Concretely, I'd probably pick one or two of the more repeated issues — say, business logic in the view — and pair with them to refactor just that one piece together, so they see the reasoning applied hands-on rather than just being told 'move this to a service layer.' I'd rather fix the pattern with them once than list every issue and have them feel overwhelmed.
>
> I'd also point them to how we've structured similar things elsewhere in the codebase, so they have a concrete reference to follow next time, and I'd keep an eye on their next couple of PRs to reinforce it — calling out when they do apply the pattern well, since positive reinforcement usually sticks better than only correcting mistakes.
>
> Ultimately, the goal isn't just to fix that one PR — it's to help them build the instinct for structuring code that way going forward, so I try to make sure they understand the 'why,' not just the 'what.'"

<details>
<summary>Coaching notes</summary>

- Original answer stated the goal ("build a habit of structured code") with no method or empathy angle — the two things mentoring questions actually screen for.
- Fix: added concrete method (pairing on one issue, not overwhelming with a full list), tone/empathy, and follow-through (checking next PRs).
</details>

---

### Q: How do you decide between Django's ORM and raw SQL for a complex reporting query?

> "My default is to stay within the ORM as long as possible — partly for the built-in protection against SQL injection, but also because ORM queries stay readable and maintainable for the rest of the team, and they adapt automatically if the underlying schema changes.
>
> For most complex reporting needs, I've found the ORM can actually handle more than it gets credit for — using `annotate` and `aggregate` for grouped calculations, `F` expressions for field-level comparisons, and `Q` objects for complex filtering, or even subqueries when I need to pull in related aggregated data. So before reaching for raw SQL, I'd try to push the ORM as far as it reasonably goes.
>
> I'd only drop to raw SQL when the query genuinely needs something the ORM can't express efficiently — for example, complex window functions, multi-table CTEs, or a performance-critical aggregation where the ORM-generated query is inefficient compared to hand-written SQL. And even then, I'd use Django's parameterized raw queries rather than string-formatting values directly, so we don't lose that SQL injection protection just because we've stepped outside the ORM."

<details>
<summary>Coaching notes</summary>

- Original answer was too binary (ORM vs. raw SQL, nothing in between).
- Fix: added the ORM's actual advanced toolkit (`annotate`, `aggregate`, `F`, `Q`, subqueries) as the middle ground, and noted security still matters even inside raw SQL (parameterized queries).
</details>

---

### Q: What's your philosophy on test coverage in a Django/DRF project — what do you prioritize testing?

> "My philosophy is that coverage should be prioritized by risk and complexity, not just a percentage target — I'd rather have strong coverage on business-critical logic, like payment handling or webhook processing, than chase 100% coverage on simple CRUD views that are unlikely to break. So when I'm writing tests, I focus first on the core logic — model methods, service functions, anything with conditional branches or edge cases — using Django's `TestCase` and DRF's `APITestCase` for endpoint-level tests, along with factories to generate realistic test data instead of hardcoding fixtures everywhere.
>
> For most features, I write the unit tests alongside the implementation and make sure they pass before raising a PR for review. But for certain critical paths — like Stripe webhook handling on Martify, where correctness really matters and edge cases like duplicate events or failed payments need to be handled precisely — I'll write the test cases first, so I'm designing the function around clearly defined expected behavior rather than testing after the fact.
>
> Once individual features are merged, we also run a broader smoke and functionality test across the app, to catch anything that might break at the integration level even if each feature passed its own tests in isolation."

<details>
<summary>Coaching notes</summary>

- Original answer described *when* tests happen in the pipeline, but not the *philosophy/priorities* the question actually asked for.
- Fix: added risk-based coverage philosophy (not 100%), named tools (`TestCase`, `APITestCase`, factories), and gave TDD its own moment with the Stripe webhook example.
</details>

---

## 5. Quick Reference: Recurring Themes

Keep these threads in mind — they came up across multiple answers and are likely to resurface as follow-ups:

- **Martify** is your strongest anchor project — Stripe webhooks + idempotency, service-layer architecture, AWS deployment, blog/CKEditor/SEO. Know it inside-out.
- **Ownership language** — say "I own," "I decided," "I raised it with my TL," not passive phrasing like "I was included in."
- **Impact over character** — when discussing conflict or difficult teammates, always frame around business/team impact, never personality.
- **Reasoning + alternative** — whenever you say "no" or push back, pair it with the *why* and a proposed alternative, not a flat rejection.
- **Escalation is a skill, not a failure** — knowing when to involve a TL/manager is itself a signal of maturity, not weakness.
- **Django-specific vocabulary** — thin views, service layer, `select_related`/`prefetch_related`, `annotate`/`aggregate`, Celery for background tasks — use these terms explicitly rather than describing them generically.

---

*Prep guide compiled from mock managerial-round Q&A. Review out loud, not silently — tone and pacing matter as much as content in a face-to-face round.*
