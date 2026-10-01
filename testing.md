# Kaun Banega Luckypati — Test Cases

How to use: run each case, mark **Pass / Fail** in the last column. "Bank" = `questions.xlsx` in the Desktop folder **Kaun Banega Luckypati**.

Legend: **P** = Pass, **F** = Fail, **N/A** = not applicable.

---

## 1. Install and first launch

| ID | Steps | Expected | Result |
|---|---|---|---|
| INS-01 | Delete the Desktop folder. Double-click the exe. | App opens fullscreen on the idle screen. A Desktop folder "Kaun Banega Luckypati" is created with `questions.xlsx`, `game-log.csv`, `.bank-version`. | |
| INS-02 | Open the new `questions.xlsx`. | 200 questions, 50 per level, columns: que, option1–4, answer, level. | |
| INS-03 | Open `game-log.csv`. | Header row only: timestamp, name, outcome, level_reached, points, lifeline_used, last_question_number. | |
| INS-04 | Launch the exe with no admin rights. | Runs without a UAC prompt or install step. | |
| INS-05 | Close the app, relaunch. | Same folder reused. Edits to `questions.xlsx` and log rows are kept. | |
| INS-06 | Machine with an older Desktop `questions.xlsx` and no `.bank-version`. Launch the new exe. | Desktop file replaced by the new bank; old one saved as `questions-old.xlsx`. | |
| INS-07 | Edit a question in the Desktop file, relaunch (same exe). | Edit is kept (not overwritten). | |
| INS-08 | Desktop redirected to OneDrive. Launch. | Folder is created on the real (OneDrive) Desktop. | |
| INS-09 | Hold `questions.xlsx` open in Excel, launch a **new** exe build with a different bank. | App still starts using the old file; replacement happens on the next launch after Excel is closed. | |

## 2. Idle and name screens

| ID | Steps | Expected | Result |
|---|---|---|---|
| IDL-01 | Launch app. | Logo, "+ New Contestant" button, intro music plays. | |
| IDL-02 | Open `questions.xlsx` in Excel, return to idle screen. | Yellow toast: "Close questions.xlsx in Excel…". Dismissible with ×. | |
| IDL-03 | Open `game-log.csv` in Excel. | Toast names game-log.csv. | |
| IDL-04 | Click New Contestant. | Name screen; Start Game disabled until a name is typed. | |
| IDL-05 | Type spaces only. | Start Game stays disabled. | |
| IDL-06 | Type a name, press Enter. | Game starts (same as clicking Start Game). | |
| IDL-07 | Type a Hindi (Devanagari) name. | Displays correctly in the intro, game header, exit screen and the CSV. | |
| IDL-08 | Name of 40+ characters. | Input limited to 40 characters. | |
| IDL-09 | Click Back on the name screen. | Returns to idle. | |

## 3. Question bank validation (error handling)

Make each change in the Desktop `questions.xlsx`, save, return to idle screen.

| ID | Change | Expected | Result |
|---|---|---|---|
| BNK-01 | Rename a column header (e.g. `que` → `question`). | Red banner: missing required column. Game does not start. | |
| BNK-02 | `answer` differs from every option by one character or a trailing space. | Banner: row N answer does not match any option (trailing spaces are trimmed; typos are not). | |
| BNK-03 | Leave a cell empty. | Banner: row N has an empty cell. | |
| BNK-04 | Level value `5` or text. | Banner: invalid / non-numeric level. | |
| BNK-05 | Fewer than 5 questions in a level. | Banner: Level N needs at least 5. | |
| BNK-06 | Level 4 with fewer than 6 questions. | Banner: Level 4 needs at least 6. | |
| BNK-07 | Delete the Desktop `questions.xlsx`, relaunch. | File is recreated from the bundled bank. | |
| BNK-08 | Fix the file and save. Return to idle. | Banner disappears; game starts. | |
| BNK-09 | Hindi question and options. | Display correctly; correct answer is recognised. | |

## 4. Question flow (the main button)

| ID | Steps | Expected | Result |
|---|---|---|---|
| FLW-01 | Start a game. After the intro music. | Q1 shows with **options hidden**; main button reads SHOW OPTIONS; 50:50 disabled. | |
| FLW-02 | Before-question music. | Plays when the question loads. | |
| FLW-03 | Press SHOW OPTIONS. | Soft chime; 4 options appear; button becomes LOCK IN (greyed out). | |
| FLW-04 | Select an option. | Option highlights; LOCK IN becomes active. | |
| FLW-05 | Select a different option. | Highlight moves; only one selected. | |
| FLW-06 | Press LOCK IN. | Lock sound; controls disabled; after ~1.5 s result shown. | |
| FLW-07 | Correct answer. | Option turns green, correct sound, points +5, button becomes NEXT QUESTION →. | |
| FLW-08 | Press NEXT QUESTION. | Next question loads with options hidden and button reset to SHOW OPTIONS. | |
| FLW-09 | Wrong answer. | Chosen option red, correct option green, wrong sound, then Game Over screen. | |
| FLW-10 | Options text is not readable before SHOW OPTIONS. | Option text not visible. | |
| FLW-11 | Q-number and "of 21" label. | Updates every question. | |
| FLW-12 | Prize ladder. | Current question highlighted; milestone rows (Q5/10/15/20/21) marked reached after securing. | |
| FLW-13 | Option order. | Differs between contestants / games (options are shuffled). Correct answer is judged by text, not position. | |

## 5. Timers

| ID | Steps | Expected | Result |
|---|---|---|---|
| TMR-01 | Q1–Q5. | No timer ring. | |
| TMR-02 | Q6–Q10. | Ring shows 30 before reveal; starts counting only on SHOW OPTIONS. | |
| TMR-03 | Q11–Q15. | 45 seconds. | |
| TMR-04 | Q16–Q20. | 60 seconds. | |
| TMR-05 | Q21 (final). | 60 seconds. | |
| TMR-06 | Wait on a timed question before pressing SHOW OPTIONS. | Timer does not move. | |
| TMR-07 | Last 10 seconds. | Ring turns warning colour; tick sound each second. | |
| TMR-08 | Timer reaches 0 with an option selected. | Counts as **wrong** (even if the selected option is correct); red flash; Game Over. | |
| TMR-09 | Timer reaches 0 with nothing selected. | Counts as wrong; Game Over. | |
| TMR-10 | Lock in before 0. | Timer stops and ticking stops. | |
| TMR-11 | Next timed question after a correct answer. | Timer resets to full, not started until SHOW OPTIONS. | |

## 6. 50:50 lifeline

| ID | Steps | Expected | Result |
|---|---|---|---|
| LIF-01 | Before SHOW OPTIONS. | 50:50 disabled. | |
| LIF-02 | After SHOW OPTIONS. | 50:50 enabled (if not used). | |
| LIF-03 | Press 50:50. | Exactly 2 options remain, one of them correct; the other two vanish. | |
| LIF-04 | Selected an option, then used 50:50. | Selection cleared; LOCK IN disabled until a new pick (even if the old pick survived). | |
| LIF-05 | Select a removed option. | Not clickable. | |
| LIF-06 | Try 50:50 again on the same or any later question. | Disabled; header badge shows as used. | |
| LIF-07 | Use 50:50 on a timed question. | Timer keeps running. | |
| LIF-08 | Use 50:50 with a stale selection from a previous game. | No effect on the new game (no stale selection). | |
| LIF-09 | Log after using 50:50. | `lifeline_used` = Yes. | |

## 7. Milestones, quit, results

| ID | Steps | Expected | Result |
|---|---|---|---|
| RES-01 | Fail on Q1–Q5. | Game Over, level "No Level", points as earned (+5 each correct). | |
| RES-02 | Pass Q5, fail on Q6–Q10. | Level 1 secured. | |
| RES-03 | Pass Q10, fail Q11–15. | Level 2 secured. | |
| RES-04 | Pass Q15, fail Q16–20. | Level 3 secured. | |
| RES-05 | Pass Q20, fail Q21. | Level 4 secured. | |
| RES-06 | Pass Q21. | WINNER screen with name; winner music; "FINAL WINNER" logged. | |
| RES-07 | Press Quit, then Cancel. | Game continues unchanged. | |
| RES-08 | Press Quit, then Confirm. | Exit screen "CONTESTANT QUIT", last secured level and points shown. | |
| RES-09 | Quit before Q5. | No level secured. | |
| RES-10 | Quit button during the lock-in delay. | Disabled while locking. | |
| RES-11 | Quit before pressing SHOW OPTIONS. | Works. | |
| RES-12 | Points. | 5 per correct answer; 105 max. | |
| RES-13 | "Next Contestant" on the exit/winner screen. | Returns to idle; new game is clean (no state carried over). | |
| RES-14 | Abort button. | Not present anywhere in the game screen. | |

## 8. Question selection rules

| ID | Steps | Expected | Result |
|---|---|---|---|
| SEL-01 | A full game. | Q1–5 from Level 1, Q6–10 Level 2, Q11–15 Level 3, Q16–20 Level 4, Q21 Level 4. | |
| SEL-02 | No repeats within one game. | 21 distinct questions. | |
| SEL-03 | Q21. | Never a question already used in anyone's Level 4 slot this session. | |
| SEL-04 | Several contestants in a row. | Q21 is never a question used in any Level 4 slot earlier this session (Q16–20 may repeat across contestants). | |
| SEL-05 | Edit the bank between contestants and save. | New questions picked up at the next "Start Game". | |

## 9. Logging

| ID | Steps | Expected | Result |
|---|---|---|---|
| LOG-01 | Finish a game by wrong answer. | One row: timestamp, name, outcome, level reached, points, lifeline, last question number. | |
| LOG-02 | Finish by quit. | Row with outcome QUIT. | |
| LOG-03 | Finish by timeout. | Row logged as a wrong/timeout result. | |
| LOG-04 | Win. | Row with final winner outcome. | |
| LOG-05 | Hindi name. | Opens correctly in Excel (UTF-8 BOM). | |
| LOG-06 | `game-log.csv` open in Excel during lock-in. | Game does **not** freeze; the answer result still shows (log write may be skipped/retried). | |
| LOG-07 | Several contestants. | Rows append; nothing overwritten. | |

## 10. Kiosk behaviour

| ID | Steps | Expected | Result |
|---|---|---|---|
| KSK-01 | Launch. | Fullscreen, no window controls. | |
| KSK-02 | Press Ctrl+Alt+Q, Cancel. | Dialog closes, app continues. | |
| KSK-03 | Press Ctrl+Alt+Q, Confirm. | App closes. | |
| KSK-04 | Press Alt+F4. | Asks for confirmation before closing. | |
| KSK-05 | Exit mid-game and relaunch. | No crash; no partial row logged for the interrupted game. | |

## 11. Audio

| ID | Event | Expected sound | Result |
|---|---|---|---|
| AUD-01 | Idle / launch | Main intro music | |
| AUD-02 | Intro screen | Intro music; moves to Q1 when it ends (or after 6 s fallback) | |
| AUD-03 | Question loaded | Before-question music | |
| AUD-04 | SHOW OPTIONS | Soft chime | |
| AUD-05 | LOCK IN | Option-lock sound; before-question music stops | |
| AUD-06 | Correct | Correct sound | |
| AUD-07 | Wrong / timeout | Wrong sound | |
| AUD-08 | Last 10 s | Tick each second | |
| AUD-09 | Winner | Intro music | |
| AUD-10 | Return to idle | All sounds stop except idle music | |

## 12. Visual and robustness

| ID | Steps | Expected | Result |
|---|---|---|---|
| VIS-01 | Different screen resolutions (1366×768, 1920×1080, 4K). | Layout scales; question, options, ladder and buttons all visible, no overflow. | |
| VIS-02 | Very long question or option text (English and Hindi). | Text wraps or shrinks; nothing is cut off. | |
| VIS-03 | Fonts. | Anton / Poppins load offline; Devanagari uses a system font. | |
| VIS-04 | No internet connection. | Everything works (all assets bundled). | |
| VIS-05 | Rapid double-click on the main button. | No skipped step; no double lock-in. | |
| VIS-06 | Click an option rapidly while locking. | Ignored once locked. | |
| VIS-07 | Play 10 contestants in a row without closing the app. | No slowdown or leftover state. | |
| VIS-08 | Low disk space on C:. | App still plays; if the log cannot be saved, the game does not freeze. | |

## 13. Regression checklist (run before every release)

1. INS-01, INS-06, INS-07
2. BNK-02, BNK-05
3. FLW-01 → FLW-09 on Q1
4. TMR-02, TMR-06, TMR-08
5. LIF-01 → LIF-06
6. RES-02, RES-06, RES-08
7. SEL-03
8. LOG-06
9. KSK-03, KSK-04

## Automated checks

`python app/tools_smoke_test.py` runs the game-logic tests (timers per question number, lifeline once only, timeout counts as wrong, milestones, quit levels, Q21 exclusion, cross-contestant exclusion). All must print `ALL SMOKE TESTS PASSED`.
