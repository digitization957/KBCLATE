# Kaun Banega Luckypati — Operator Guide

![Questions](https://img.shields.io/badge/question%20bank-200%20questions-brightgreen) ![Platform](https://img.shields.io/badge/platform-Windows-blue) ![Build](https://img.shields.io/badge/build-passing-success)

## Running it
Double-click `KaunBanegaLuckypati.exe`. No installation, no admin rights needed.

The first time it runs, it creates a folder named **"Kaun Banega Luckypati"** on your
Desktop containing:
- `questions.xlsx` — your question bank (the bundled question bank, 200 questions (50 per level)).
- `game-log.csv` — a log of every contestant's result. Opens fine in Excel.

Every launch after that reuses the same folder — your edited questions and the
accumulated log are never overwritten or reset.

## Editing questions
When a new build ships an updated question bank, the first launch replaces the Desktop
`questions.xlsx` with it (your previous file is saved as `questions-old.xlsx`). Edits you
make afterwards are kept.

Open `questions.xlsx` on your Desktop and edit it directly (English or Hindi/Devanagari
both work). Columns, exactly as shown:

| que | option1 | option2 | option3 | option4 | answer | level |
|---|---|---|---|---|---|---|

- `answer` must be an **exact copy** of one of the four options (copy-paste it, don't
  retype it, to avoid a trailing space or typo breaking the match).
- `level` is 1, 2, 3, or 4.
- You need **at least 5 questions in levels 1–3**, and **at least 6 in level 4**
  (5 for questions 16–20, plus spares for the final question).
- More questions per level = more variety across contestants. 20–30+ per level is a
  good target if you expect a lot of players.
- **Close the file in Excel before starting a new contestant** if you were mid-edit —
  the app re-reads the file each time someone starts, and an unsaved edit won't be
  picked up until you save.
- If something's wrong with the file (missing column, not enough questions, answer
  that doesn't match an option), the idle screen shows a red warning banner naming
  the exact problem instead of failing silently.

## How a game works
- 21 questions: Q1–5 (Level 1, no timer), Q6–10 (Level 2, 30 s), Q11–15 (Level 3, 45 s),
  Q16–20 (Level 4, 60 s), then Q21, the final question (60 s), also drawn from the
  Level 4 pool but never a question already used in anyone's Level 4 slot this session.
- Each question: the question shows first; **Show Options** reveals the options (soft
  chime) and starts the timer; select one, **Lock In**; if correct, **Next Question**.
  It is one button that changes label at each step.
- Milestone prizes at Q5 / Q10 / Q15 / Q20 / Q21. A wrong answer or a quit falls back
  to the last milestone actually secured; failing before Q5 secures nothing.
- One 50:50 lifeline per contestant, usable on any question.
- Running points (+5/question) are visible throughout; the physical prize per level is
  handled by you/management outside the app — the app only tracks which level was reached.

## Operator controls (bottom bar during a question)
- **50:50** — available only after Show Options; removes two wrong options. Once per contestant.
- **Show Options / Lock In / Next Question** — the single main button (see above).
- **Quit** — ends the contestant's game now, keeping their last secured level. Asks for
  confirmation first.

## Exiting the kiosk
The app is fullscreen with no visible window controls, by design. Press
**Ctrl+Alt+Q** and confirm to close it. Closing it any other way (Alt+F4, etc.) will
also now ask for confirmation first, so a stray keypress won't kill it mid-game.

## After the event
Open `game-log.csv` on the Desktop in Excel to see every contestant's result:
name, outcome (WIN / LOST / QUIT), level reached, points, whether they used the
lifeline, and which question number they were on.

If you keep `game-log.csv` open in Excel *while the game is running*, a result
that can't be appended because the file is locked is written instead to
`game-log.csv.pending.csv` in the same folder — check there too if a contestant's
result seems missing after the event.
