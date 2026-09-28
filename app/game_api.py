"""Core game state machine, exposed to the web UI via pywebview's js_api."""
import csv
import datetime
import os
import random

from data_loader import load_questions, QuestionBankError

MILESTONE_LEVEL = {5: 1, 10: 2, 15: 3, 20: 4, 21: 5}
LEVEL_LABEL = {
    0: "No Level",
    1: "Level 1",
    2: "Level 2",
    3: "Level 3",
    4: "Level 4",
    5: "FINAL WINNER",
}


def _level_of_question_number(qnum):
    if qnum <= 5:
        return 1
    if qnum <= 10:
        return 2
    if qnum <= 15:
        return 3
    if qnum <= 20:
        return 4
    return "final"


class Api:
    def __init__(self, window_getter, questions_xlsx_path, log_csv_path):
        self._get_window = window_getter
        self._xlsx_path = questions_xlsx_path
        self._log_path = log_csv_path
        self._bank = None
        self._bank_error = None
        self.level4_ever_used = set()  # question texts ever used in a level-4 slot (Q16-20 or Q21), across all contestants this session
        self._reload_bank()
        self._reset_run()

    # ---------- setup / bank ----------

    def _reload_bank(self):
        try:
            self._bank = load_questions(self._xlsx_path)
            self._bank_error = None
        except QuestionBankError as e:
            self._bank = None
            self._bank_error = str(e)

    def check_bank(self):
        self._reload_bank()
        if self._bank_error:
            return {"ok": False, "error": self._bank_error}
        counts = {lvl: len(qs) for lvl, qs in self._bank.items()}
        return {"ok": True, "counts": counts}

    # ---------- run state ----------

    def _reset_run(self):
        self.name = None
        self.questions = []
        self.current_index = 0
        self.correct_count = 0
        self.milestone_level = 0
        self.lifeline_used = False
        self.pending_option = None
        self.locked = False
        self.active = False

    def _pick_questions(self):
        bank = self._bank
        selected = []
        for level in (1, 2, 3):
            pool = bank[level][:]
            random.shuffle(pool)
            selected.extend(pool[:5])

        level4_pool = bank[4][:]
        random.shuffle(level4_pool)
        level4_chosen = level4_pool[:5]
        selected.extend(level4_chosen)
        for q in level4_chosen:
            self.level4_ever_used.add(q["question"])

        # Final question: never one that's ever appeared in a level-4 slot
        # (Q16-20 or Q21) for this or any earlier contestant this session.
        final_candidates = [q for q in bank[4] if q["question"] not in self.level4_ever_used]
        if not final_candidates:
            # Global pool exhausted -- fall back to just avoiding this
            # contestant's own Q16-20 picks so the game can still proceed.
            chosen_texts = {q["question"] for q in level4_chosen}
            final_candidates = [q for q in bank[4] if q["question"] not in chosen_texts]
        if not final_candidates:
            final_candidates = bank[4]

        final_q = random.choice(final_candidates)
        self.level4_ever_used.add(final_q["question"])
        selected.append(final_q)

        prepared = []
        for q in selected:
            opts = q["options"][:]
            random.shuffle(opts)
            prepared.append({"question": q["question"], "options": opts, "answer": q["answer"]})
        return prepared

    def start_contestant(self, name):
        name = (name or "").strip()
        if not name:
            return {"ok": False, "error": "Name is required."}

        self._reload_bank()
        if self._bank_error:
            return {"ok": False, "error": self._bank_error}

        self._reset_run()
        self.name = name
        self.questions = self._pick_questions()
        self.active = True
        return {"ok": True, "name": self.name}

    def get_current_question(self):
        if not self.active or self.current_index >= len(self.questions):
            return {"ok": False, "error": "No active question."}

        qnum = self.current_index + 1
        q = self.questions[self.current_index]
        level = _level_of_question_number(qnum)
        return {
            "ok": True,
            "number": qnum,
            "total": len(self.questions),
            "level": level,
            "question": q["question"],
            "options": q["options"],
            "timer_seconds": 60 if qnum >= 6 else 0,
            "points": self.correct_count * 5,
            "milestone_level": self.milestone_level,
            "milestone_label": LEVEL_LABEL[self.milestone_level],
            "lifeline_available": not self.lifeline_used,
            "is_milestone_question": qnum in MILESTONE_LEVEL,
        }

    def select_option(self, option_text):
        if not self.active or self.locked:
            return {"ok": False}
        self.pending_option = option_text
        return {"ok": True}

    def use_lifeline(self):
        if not self.active or self.lifeline_used or self.locked:
            return {"ok": False, "error": "Lifeline unavailable."}

        q = self.questions[self.current_index]
        correct = q["answer"]
        wrong_options = [o for o in q["options"] if o != correct]
        keep_wrong = random.choice(wrong_options)
        remaining = [correct, keep_wrong]
        random.shuffle(remaining)

        self.lifeline_used = True
        return {"ok": True, "options": remaining}

    def lock_in(self):
        if not self.active or self.locked:
            return {"ok": False, "error": "Nothing to lock in."}

        self.locked = True
        q = self.questions[self.current_index]
        qnum = self.current_index + 1
        is_correct = self.pending_option is not None and self.pending_option == q["answer"]

        if is_correct:
            self.correct_count += 1
            if qnum in MILESTONE_LEVEL:
                self.milestone_level = MILESTONE_LEVEL[qnum]

            if qnum == len(self.questions):
                self._log_result("WIN")
                result = {
                    "ok": True,
                    "correct": True,
                    "win": True,
                    "name": self.name,
                    "points": self.correct_count * 5,
                    "milestone_label": LEVEL_LABEL[self.milestone_level],
                }
                self.active = False
                return result

            return {
                "ok": True,
                "correct": True,
                "win": False,
                "milestone_hit": qnum in MILESTONE_LEVEL,
                "points": self.correct_count * 5,
                "milestone_level": self.milestone_level,
                "milestone_label": LEVEL_LABEL[self.milestone_level],
            }

        # wrong or timed out
        self._log_result("LOST")
        result = {
            "ok": True,
            "correct": False,
            "win": False,
            "name": self.name,
            "correct_answer": q["answer"],
            "points": self.correct_count * 5,
            "milestone_level": self.milestone_level,
            "milestone_label": LEVEL_LABEL[self.milestone_level],
        }
        self.active = False
        return result

    def next_question(self):
        if self.current_index + 1 >= len(self.questions):
            return {"ok": False, "error": "No more questions."}
        self.current_index += 1
        self.pending_option = None
        self.locked = False
        return {"ok": True}

    def quit_game(self):
        if not self.name:
            return {"ok": False}
        self._log_result("QUIT")
        result = {
            "ok": True,
            "name": self.name,
            "points": self.correct_count * 5,
            "milestone_level": self.milestone_level,
            "milestone_label": LEVEL_LABEL[self.milestone_level],
        }
        self.active = False
        return result

    def abort_game(self):
        self._reset_run()
        return {"ok": True}

    def next_contestant(self):
        self._reset_run()
        return {"ok": True}

    # ---------- logging ----------

    def _log_result(self, outcome):
        path = self._log_path
        is_new = not os.path.exists(path)
        qnum = self.current_index + 1
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow([
                    "timestamp", "name", "outcome", "level_reached",
                    "points", "lifeline_used", "last_question_number",
                ])
            writer.writerow([
                datetime.datetime.now().isoformat(timespec="seconds"),
                self.name,
                outcome,
                LEVEL_LABEL[self.milestone_level],
                self.correct_count * 5,
                "Yes" if self.lifeline_used else "No",
                qnum,
            ])

    # ---------- kiosk control ----------

    def exit_app(self):
        window = self._get_window()
        if window:
            window.destroy()
        return {"ok": True}
