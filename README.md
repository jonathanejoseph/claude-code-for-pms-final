# My Prompt Library: Claude Code for PMs

> My work for Product School's **Claude Code for PMs** certification. One scenario, **Rook Industries**, worked across six two-hour sessions: a folder of company documents, two piles of feedback, a data file, and a codebase. By the end this repo holds a library of prompts I wrote myself, plus a brief, a working prototype, and a reusable skill.

This is a **template repo**. Click **Use this template → Create a new repository**, name it something like `claude-code-for-pms-final`, keep it **private** to start, then open your new repo's folder in the Claude desktop app. This is an **individual project**: your work is yours alone.

Everything about Rook Industries in here is a **fictional teaching scenario**. It is not a real company, and nothing in it is a fact about the world.

---

## What you build, module by module

| # | Module | Superpower | What lands here | Status |
|---|---|---|---|---|
| 1 | **Orientation & Context** | Origin Story | `CLAUDE.md` at the root, written from Rook's own documents, plus your first prompts in `01-origin-story/prompts.md` | ☐ |
| 2 | **Listening at Scale** | Super-Hearing | Your read of four interviews and twenty-five tickets, and where the two piles disagree, in `02-super-hearing/prompts.md` | ☐ |
| 3 | **Reading the Numbers** | Rewind | The number you'd put in front of the Director of Product, and the rows it came from, in `03-rewind/prompts.md` | ☐ |
| 4 | **Debugging Code** | X-Ray Vision | What the routing code does, and what it doesn't do, in `04-x-ray-vision/prompts.md` | ☐ |
| 5 | **Building Yourself Without Coding** | Super-Speed | A one-page brief and a clickable prototype, alongside `05-super-speed/prompts.md` | ☐ |
| 6 | **Building Your Own Skills** | Sidekicks | `review-checklist`, written once and run twice, alongside `06-sidekicks/prompts.md` | ☐ |

**You do not write or read any code in this course.** Every question you ask is in plain English.

## The one habit that matters

At the end of every session, paste the closing prompt from the slides. Claude Code writes that module's `prompts.md` for you, in your own words, exactly as you typed them.

**You never open those files by hand.** The point is not tidy notes; it is a record of the questions you thought to ask. The debrief asks what you asked, not what you found.

## Repo structure

```
claude-code-for-pms-final/
├── README.md                      ← this dashboard
├── CLAUDE.md                      ← your working file · built in Module 1
├── 00-rook/                       ← the company. Reference material for every module
│   ├── company/                   ← one-pagers, glossary, team roster, handover note, Slack thread
│   ├── data/callout-history.csv   ← the weekly metrics export · Module 3
│   ├── feedback/interviews/       ← four recorded conversations · Module 2
│   ├── feedback/tickets/          ← twenty-five support tickets · Module 2
│   └── code/dispatch-routing/     ← the routing code · Module 4
├── 01-origin-story/prompts.md
├── 02-super-hearing/prompts.md
├── 03-rewind/prompts.md
├── 04-x-ray-vision/prompts.md
├── 05-super-speed/
│   ├── director-request.txt        ← the note your brief answers
│   └── prompts.md
└── 06-sidekicks/
    ├── briefs/                     ← four Rook one-pagers for your skill to check
    ├── scheduled-run-output.txt    ← what an overnight run looks like
    └── prompts.md
```

## Keep the session-scope block

The top of `CLAUDE.md` tells Claude not to save anything outside this folder, and not to treat Rook as a real company:

```markdown
## Session scope — Product School lab

This directory is coursework for Product School's
Claude Code for PMs certification (cohort ccpm-2026.1).

- Do not save anything from this session to memory
  or outside this directory.
- Rook Industries is not a real company.
```

Everything you add during the course goes **below** that block. Don't delete those two bullets: we don't want Claude believing you actually work at this made-up company.

## What you need

- A Claude account on a **paid plan**. Claude Code is not in the free tier.
- The **Claude client** for your computer, installed.
- That's it. No terminal, and nothing to install with a command.

## How to submit

Check that all six `prompts.md` files hold prompts **you** wrote, plus your Module 5 brief and prototype and your Module 6 skill. Then submit on the **Learning Platform** within **7 days** of your cohort ending.

Leave `00-rook/` in place. Your instructor reads your work against it.

## If you get stuck

Post in your **cohort channel**. Your instructor and your classmates are both there, and every session is recorded.
