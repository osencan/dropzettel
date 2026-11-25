# Using Obsidian with Dropzettel: a beginner's guide

Dropzettel does the filing. This guide is about the other half: what you do in Obsidian with the notes once they are there, how to read the graph, and how to use the vault for brainstorming.

It assumes you have run setup, opened the vault folder in Obsidian and have a few captures filed. You do not need to know anything about Zettelkasten yet.

## The method in five sentences

A Zettelkasten is a box of small notes that link to each other. There are three kinds of note, and Dropzettel's folders follow them:

| Kind | What it is | Folder | Who writes it |
|---|---|---|---|
| Fleeting | A thought as it came to you, unpolished | `1 - Raw Notes` | You, through the inbox |
| Source (also called literature) | One note about one thing you read, watched or found | `2 - Sources` | Dropzettel, from the source and your comment |
| Permanent | One idea, in your own words, that still makes sense in a year | `4 - Zettelkasten` | Only you |

Collecting sources is not the goal. The value comes from the permanent notes and the links between them, because writing an idea in your own words is where you find out whether you understand it. Everything else in the vault exists to make that step easy.

## Set up Obsidian once

Open *Settings* and change these. All of them are core features unless marked.

- **Files and links → Default location for new notes:** `4 - Zettelkasten`. Notes you create by hand are your own notes; captures arrive through the inbox.
- **Files and links → Default location for new attachments:** `6 - Attachments`.
- **Core plugins → Templates:** switch it on and set the template folder to `5 - Templates`. The *Insert template* command then offers `Permanent Note`.
- **Core plugins:** make sure *Backlinks*, *Outgoing links*, *Graph view*, *Canvas*, *Bookmarks*, *Random note* and *Page preview* are on.
- **Community plugins → Dataview** (community plugin): install and enable it. The `To Check` dashboard needs it.
- **Bookmarks:** bookmark `0 - Dashboard/To Check` and `Start Here`, so they are one click away.

Three shortcuts carry most of the daily work (Ctrl in place of Cmd on Windows and Linux):

| Shortcut | What it does |
|---|---|
| Cmd+O | Quick switcher: jump to any note by typing part of its title |
| Cmd+P | Command palette: run any command by name |
| Cmd+G | Open the graph view |

## Anatomy of a filed note

Open any note in `2 - Sources`. From top to bottom:

- **Properties** (the frontmatter): `kind`, `status`, `action`, `captured`, `tags`, `topics`, `summary`, `url`. A note with `review: true` is one the librarian was unsure about, or whose source could not be read.
- **My note at capture:** your own words, verbatim, in a quote box. This is the only part of the note that is your thinking.
- **Summary, Key points, Why it might matter:** written by the model from the source. Treat them as a colleague's notes: useful for deciding whether to read the original, not a replacement for it.
- **Related:** links to notes that already existed in your vault.
- **Source:** the link or the original file.

`status` is the one property you change by hand:

| Status | Meaning |
|---|---|
| `to-check` | Still needs your attention; `action` says what kind (`read`, `watch`, `try`, `think`) |
| `done` | You dealt with it |
| `reference` | Nothing to do, kept for looking up |

## Knowledge grabbing: from capture to an idea of your own

### 1. Capture with a reason

Add one sentence of why whenever you can: "compare with how we onboard users", "might explain the retention drop". It costs five seconds, the librarian weighs it most, and it is the first thing you will want to read later.

### 2. Clear `To Check` once or twice a week

Open `0 - Dashboard/To Check`. For each item, pick one:

- Read or watch it now, then set `status: done`.
- Decide it is only worth keeping for lookup: `status: reference`.
- Decide it was not worth saving: `status: done`. Do not feel obliged to read everything you captured.

Ten minutes is enough. The point is that the list goes down, so you keep trusting it.

### 3. Read the weekly review

`0 - Dashboard/Weekly Review YYYY-Www` lists themes, connections between captures, and one to three candidates for a permanent note. It is a suggestion from a model that only saw titles and summaries, so expect some of it to miss. Take what is useful.

### 4. Write one permanent note

This is the step that matters, and one note a week is a good pace.

1. Create a note (it lands in `4 - Zettelkasten`), then run *Insert template* → `Permanent Note`.
2. Give it a title that is a claim, not a topic: "Spaced repetition works because forgetting is part of learning" instead of "Spaced repetition".
3. Write the idea in a few sentences, as if explaining it to someone else. Do not copy the summary.
4. Under *Where it came from*, link the source notes with `[[`.
5. Under *Connects to*, link at least one other permanent note, and write a few words on how they connect: "contradicts", "is an example of", "explains why". A link without a reason tells your future self very little.

If you cannot write the idea without looking at the source, you have found something to read again. That is the method working.

### 5. Tidy an index now and then

Each topic has a hub note in `3 - Indexes`. Dropzettel only appends lines under `## Captures`. Everything above that heading is yours: add an introduction, group your permanent notes, write down the open questions for that topic. A hub you have arranged yourself is the best entry point into a topic.

### Finding things again

Search (Cmd+Shift+F) understands properties and folders:

| Search | Finds |
|---|---|
| `[status:to-check]` | Everything still open |
| `[review:true]` | Notes the librarian was unsure about |
| `[kind:video]` | All videos |
| `tag:#note-taking` | Notes with that tag |
| `path:"4 - Zettelkasten" learning` | Your own notes that mention learning |
| `path:"2 - Sources" -[status:done] pricing` | Unfinished sources about pricing |

`0 - Dashboard/Tag Registry` shows the tag vocabulary, and the Capture Log of the month shows where each capture went and why.

## Reading the graph

The graph draws every note as a dot and every link as a line. It does not think for you, but it is good at showing shape: what clusters, what is isolated, what connects two areas.

### Make it readable first

Open it with Cmd+G, then use the settings panel in its corner.

**Filters.** Put this into the search field:

```
-path:"0 - Dashboard" -path:"5 - Templates"
```

The Capture Log and the weekly reviews link to every note, so without this filter they sit in the middle like a hairball and hide the real structure. Leave *Attachments* off. Switch *Tags* on only when you want to see which tags hold notes together.

**Groups.** Add one group per folder so the colour tells you the kind of note:

| Group query | Suggested meaning |
|---|---|
| `path:"4 - Zettelkasten"` | Your permanent notes; give them the strongest colour |
| `path:"3 - Indexes"` | Topic hubs |
| `path:"2 - Sources"` | Sources |
| `path:"1 - Raw Notes"` | Thoughts |

**Display.** Raise the text fade threshold if titles clutter the view. Arrows are useful once you write permanent notes, because they show which note points to which.

### What the shapes tell you

- **A hub with many source dots and no permanent note near it:** a topic you keep collecting on and have not thought about yet. This is the clearest signal for what to write next.
- **A permanent note with one link:** an idea you wrote down and never connected. Open it and ask what it supports or contradicts.
- **A note linked to two clusters:** a bridge between two topics. Bridges are where unexpected ideas tend to come from, so read them first when brainstorming.
- **Dots with no lines** (switch *Orphans* on): mostly older notes that were never linked. Link them or let them be.
- **A cluster that grew quickly:** what currently has your attention, whether you planned it or not. The *Animate* button replays the vault's growth over time.

### The local graph is the one you will use most

The global graph is an overview. For actual work, open a note and run *Open local graph* from the command palette (it is also in the note's *More options* menu). It shows only that note's neighbourhood.

- Set **Depth** to 2 to see neighbours of neighbours. This is where you notice that two notes you never linked share a source or a topic.
- Drag the local graph to the right sidebar and it follows whichever note you have open.
- Apply the same groups, so your own notes stand out from the sources.

### Honest limits

A dense, colourful graph proves nothing. Dropzettel adds topic and related links automatically, so the graph looks connected from the first week; those links were chosen by a model. The connections that count are the ones between your permanent notes, because you wrote the reason for each. If the strongest colour in your graph is rare, the vault is a collection, not yet a Zettelkasten.

## Brainstorming with the vault

Start from a question, not from the graph. "What could the onboarding for the new app look like?" works. "Let me look at my notes" does not.

**1. Ask the vault.** Open an AI agent in the vault folder and ask it the question. The vault's `AGENTS.md` tells it to answer from your notes, cite them as `[[links]]`, and say when the vault has nothing. Ask for connections across topics: "Which captures from different topics connect to this?" Then open the cited notes yourself; the answer is a starting list, not the result.

**2. Walk the neighbourhood.** Open the most relevant note, set the local graph to depth 2, and follow lines that surprise you. Use the *Backlinks* pane and its *Unlinked mentions* section, which lists notes that use the same words without being linked. Each one is a connection you can make with one click.

**3. Force a collision.** Run *Open random note* three times and ask of each note: what would this say about my question? Most pairings give nothing. The one that does is usually an idea you would not have reached by searching, because search only finds what you already thought to look for.

**4. Lay it out on a canvas.** Create a canvas (command palette → *Create new canvas*) and drag in the five to ten notes that came up. Move them around, group them, draw arrows, add text cards for the thoughts that appear. A canvas is the right place for half-formed ideas because nothing in it has to be a finished note.

**5. Keep the result.** Before you close the session:

- Write the one or two ideas that survived as permanent notes, each linked to the notes it came from.
- Send loose ideas and open questions through the inbox like any other thought, so they are logged and come back in the weekly review.
- Link the canvas from the relevant index note if you want to return to it.

A session that ends without at least one new permanent note or one new link has usually been browsing.

## Two dashboards worth adding

Paste these into a note of your own. Both need Dataview.

Your permanent notes, least connected first, so you see which ideas stand alone:

````markdown
```dataview
TABLE length(file.inlinks) AS "Links in", length(file.outlinks) AS "Links out"
FROM "4 - Zettelkasten"
SORT length(file.inlinks) ASC
```
````

Open sources by topic, to choose what to read next:

````markdown
```dataview
TABLE kind AS "Kind", action AS "To", topics AS "Topic"
FROM "2 - Sources"
WHERE status = "to-check"
SORT captured DESC
```
````

## A weekly routine that fits in half an hour

| Step | Time | What |
|---|---|---|
| Capture | All week, seconds each | Share sheet or inbox folder, with one sentence of why |
| Clear | 10 minutes | `To Check`: read, mark `done` or `reference` |
| Review | 5 minutes | Weekly Review: pick one candidate |
| Write | 15 minutes | One permanent note with two links and their reasons |

## Common mistakes

- **Collecting without writing.** Two hundred sources and no permanent notes is a bookmark folder with better search. Write one note a week.
- **Treating the summary as your knowledge.** The summary is the model's reading of the source. Your knowledge is what you can write without it.
- **Reorganising folders and tags.** The librarian handles filing; time spent rearranging is time not spent thinking. Fix a note that was filed wrongly and move on.
- **Topics as titles.** "Pricing" is a topic and belongs in `3 - Indexes`. A permanent note states something: "Annual plans work when the first month already proved the value."
- **Long permanent notes.** One idea per note. If a note needs headings, it is two or three notes.
- **Judging the vault by the graph.** Judge it by whether it helped you answer a question last month.
