<details>
<summary><strong>1. "Tell me a little about yourself and your journey so far as a developer."</strong></summary>

### Answer

I did my B.Tech in Computer Science from Haldia Institute of Technology, and for the last four years I've been working as a Python Django developer at Codeclouds. Over these four years, my role has gradually expanded beyond just developing features. I’ve had the opportunity to be involved in requirement discussions, database design, sprint planning, and deployment, which has given me a better understanding of the complete development lifecycle.

Alongside my day-to-day work, I've also built and maintained Martify, a full-featured Django e-commerce application — it includes Stripe payment integration(in sandbox mode) with webhook handling, a blog module with SEO and CKEditor, and I've deployed it on AWS temporarily using my own AWS account. 
At this stage, I’m looking for a role where I can gradually take on more responsibility, contribute to larger-scale projects, and continue growing as a backend developer. 
I’ve also been developing an interest in event-driven architecture, so I’d be excited to explore opportunities to work with that kind of architecture if they come up.
</details>

<details>
<summary><strong>2. "Walk me through a time you disagreed with a technical decision made by your senior or manager. How did you handle it?"</strong></summary>

### Answer

On one project, our client wanted to reduce the number of listed products, add several new ones, and eventually move away from the legacy product-listing structure. I proposed rebuilding the product database from scratch, since most of the old products were no longer relevant and I felt a clean schema would be easier to maintain long-term.

My team lead disagreed — his concern was that a full rebuild carried migration risk and would take longer, when the client actually needed a quick turnaround. Rather than push my approach, I asked him to walk me through the specific risks he was worried about, and that helped me see the timeline pressure I'd been underweighting.

We ended up landing on a middle ground: instead of rebuilding, we added an inUse boolean flag to the existing product model, so we could deactivate legacy products without deleting their data, and bring in new products immediately. It let us move fast, kept historical data intact for reporting, and avoided any migration risk.
That experience taught me that being technically 'right' isn't always the priority — understanding the constraints your teammates are weighing, like timelines or risk, often leads to a better decision than either original proposal.
</details>

<details>
<summary><strong>3. Describe a situation where you had to manage multiple priorities or a tight deadline. How did you decide what to focus on first?</strong></summary>

### Answer

There was a period at Codeclouds where I had a client-facing deadline for a new feature, while also handling a couple of bug fixes and a code review for a teammate — all in the same week. I started by mapping out what was actually blocking someone else versus what could wait: the client deadline was fixed and high-visibility, so that became my top priority. The code review was next, since it was blocking a teammate's work, even though it only took me half an hour. The bug fixes were lower-severity, so I slotted those in later, and flagged one of them to my TL in case it needed to be escalated to someone else if I ran out of time.

I also made it a point to give a quick heads-up to my TL early on, rather than silently juggling everything — that way, if priorities needed to shift, we could catch it early instead of at the deadline. In the end, I delivered the client feature on time, unblocked my teammate the same day, and got to the bug fixes by the end of the week
</details>

<details>
  <summary>
    <strong>
      4. Tell me about a time you made a mistake in production or delivered something that didn't work as expected. What happened, and how did you handle it?
    </strong>
  </summary>
  ### Answer

  I once pushed a deployment where, right after going live, the styling on the site was completely broken — no CSS was loading. I noticed it within minutes during a quick post-deploy check, and traced it back to a typo in the S3 bucket URL where our static files were hosted, so the browser was requesting assets from a path that didn't exist.
I fixed the URL and redeployed immediately, so the downtime was minimal, but it made me realize we didn't have a consistent post-deployment check in place — we were relying on the deployment 'succeeding' without actually verifying the site looked and worked right afterward. So I raised it with the team, and we added a mandatory smoke test after every deployment — checking that static assets, key pages, and core flows like login and checkout all load correctly before we call a release done.
It was a small mistake, but it taught me that a deployment isn't complete just because the pipeline runs green — it's complete when you've verified the user-facing experience actually works
</details>

<details>
  <summary>
    <strong>
      5. Tell me about a time you had to learn a new technology or tool quickly to get a task done. How did you approach it?
    </strong>
  </summary>
  ### Answer

  On one project, the client needed us to process and clean a large sales dataset — merging data from multiple sources, handling missing values, and generating summary reports — and pandas was the right tool for that, but I hadn't used it in depth before. I had about three days before it was needed, so rather than learning it randomly, I built a short roadmap: day one was core pandas — DataFrames, indexing, and filtering, using the official documentation and a Kaggle dataset to practice; day two was aggregation and merging, since that was central to the actual task; day three I applied everything directly to the client's dataset, using a mix of real and dummy data to test edge cases before running it for real.
By the end of day three, I had a working script that cleaned and merged the data and generated the reports the client needed, and I delivered it on schedule. That experience also became my go-to approach whenever I need to ramp up on something new quickly — break it into a short daily curriculum tied directly to the actual task, rather than learning a library end-to-end in the abstract.
</details>

<details>
  <summary>
    <strong>
      6. Walk me through your typical development workflow — from picking up a ticket or requirement, to it going live in production. What does that process look like on your team at Codeclouds?
    </strong>
  </summary>
  ### Answer

 Our tasks are tracked mainly in Jira, though a few clients work through Asana or direct email instead. Our day starts with a quick call where we discuss and assign tasks.
For an existing project, once I pick up a task, I create a feature branch in Git and start with the logic — building it out in the model and view layers. Before handing anything off, I write unit tests for that feature, since I want to catch issues before it reaches the frontend or a reviewer. Once tests pass, I pass the context data to our designer to build the frontend against it.
From there, I raise a pull request and request a code review from my TL. Once it's approved, it gets merged into the develop branch, where we run a compatibility test to make sure it works well with the rest of the codebase and doesn't break existing features. Once that passes, develop gets merged into release, which triggers our CI/CD pipeline — a new Docker image is built and deployed through Github Action to our AWS environment.
For a new project, the process starts earlier — we begin with requirement discussions with the client, put together a PRD and functionality spec, and design the database schema up front. Once that's confirmed and broken down into tasks, we start building features incrementally, following the same branch-review-merge-deploy flow from there.
</details>

