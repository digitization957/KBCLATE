"""Loads the question bank from data/questions.xlsx."""
import os
import openpyxl

REQUIRED_COLUMNS = ["que", "option1", "option2", "option3", "option4", "answer", "level"]


class QuestionBankError(Exception):
    pass


def load_questions(xlsx_path):
    if not os.path.exists(xlsx_path):
        raise QuestionBankError(f"Question bank not found: {xlsx_path}")

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb.active

    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        raise QuestionBankError("Question bank is empty.")

    header = [str(c).strip().lower() if c is not None else "" for c in rows[0]]
    col_index = {}
    for col in REQUIRED_COLUMNS:
        if col not in header:
            raise QuestionBankError(f"Question bank is missing required column: '{col}'")
        col_index[col] = header.index(col)

    by_level = {1: [], 2: [], 3: [], 4: []}
    for row_num, row in enumerate(rows[1:], start=2):
        if row is None or all(c is None for c in row):
            continue
        que = row[col_index["que"]]
        options = [row[col_index[f"option{i}"]] for i in range(1, 5)]
        answer = row[col_index["answer"]]
        level = row[col_index["level"]]

        if que is None or answer is None or level is None or any(o is None for o in options):
            raise QuestionBankError(f"Row {row_num} has an empty cell.")

        try:
            level = int(level)
        except (TypeError, ValueError):
            raise QuestionBankError(f"Row {row_num} has a non-numeric level: {level!r}")

        options = [str(o).strip() for o in options]
        answer = str(answer).strip()

        if level not in by_level:
            raise QuestionBankError(f"Row {row_num} has an invalid level: {level} (must be 1-4)")
        if answer not in options:
            raise QuestionBankError(
                f"Row {row_num}: answer '{answer}' does not exactly match any of its options."
            )

        by_level[level].append({
            "question": str(que).strip(),
            "options": options,
            "answer": answer,
        })

    for level in (1, 2, 3, 4):
        if len(by_level[level]) < 5:
            raise QuestionBankError(
                f"Level {level} has only {len(by_level[level])} questions; needs at least 5."
            )
    if len(by_level[4]) < 6:
        raise QuestionBankError(
            "Level 4 needs at least 6 questions (5 for Q16-20 plus 1 spare for the final question)."
        )

    return by_level
