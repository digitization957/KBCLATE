"""Standalone smoke test for game_api.Api, no GUI involved.
Simulates: full 21-question win, a mid-game wrong answer fallback, a quit,
lifeline usage, and a timeout (pending_option=None). Prints PASS/FAIL.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_api import Api, MILESTONE_LEVEL, LEVEL_LABEL

XLSX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "questions.xlsx")
LOG_CSV = os.path.join(tempfile.gettempdir(), "kbc_smoke_test_log.csv")


def make_api():
    return Api(lambda: None, XLSX, LOG_CSV)


def answer_correctly(api, q):
    ans = None
    # cheat: peek at internal question to find correct answer text
    internal_q = api.questions[api.current_index]
    for opt in q["options"]:
        if opt == internal_q["answer"]:
            ans = opt
            break
    api.select_option(ans)
    return api.lock_in()


def test_full_win():
    api = make_api()
    res = api.start_contestant("  Alice  ")
    assert res["ok"], res
    assert api.name == "Alice"

    for i in range(21):
        q = api.get_current_question()
        assert q["ok"], q
        assert q["number"] == i + 1
        expected_timer = 60 if (i + 1) >= 6 else 0
        assert q["timer_seconds"] == expected_timer, (i, q)

        result = answer_correctly(api, q)
        assert result["ok"] and result["correct"], (i, result)

        if i + 1 == 21:
            assert result["win"] is True
            assert result["milestone_label"] == "FINAL WINNER"
        else:
            assert result["win"] is False
            nxt = api.next_question()
            assert nxt["ok"], nxt

    print("test_full_win: PASS")


def test_wrong_fallback():
    api = make_api()
    api.start_contestant("Bob")
    # answer Q1-6 correctly (crosses milestone at Q5 -> Level 1), fail Q7
    for i in range(6):
        q = api.get_current_question()
        result = answer_correctly(api, q)
        assert result["correct"]
        api.next_question()
    assert api.milestone_level == 1, api.milestone_level

    # Q7: answer wrong on purpose
    q = api.get_current_question()
    assert q["number"] == 7
    wrong_opt = None
    internal_q = api.questions[api.current_index]
    for opt in q["options"]:
        if opt != internal_q["answer"]:
            wrong_opt = opt
            break
    api.select_option(wrong_opt)
    result = api.lock_in()
    assert result["ok"] and result["correct"] is False
    assert result["milestone_level"] == 1
    assert result["milestone_label"] == "Level 1"
    print("test_wrong_fallback: PASS")


def test_timeout_forces_wrong_even_if_correct_was_selected():
    api = make_api()
    api.start_contestant("Cara")
    q = api.get_current_question()
    internal_q = api.questions[api.current_index]
    api.select_option(internal_q["answer"])  # selected correct...
    api.select_option(None)  # ...but timeout clears it before lock_in (per JS handleTimeout)
    result = api.lock_in()
    assert result["correct"] is False, "timeout must count as wrong even if correct was pre-selected"
    print("test_timeout_forces_wrong: PASS")


def test_lifeline_once_only():
    api = make_api()
    api.start_contestant("Dev")
    r1 = api.use_lifeline()
    assert r1["ok"] and len(r1["options"]) == 2
    r2 = api.use_lifeline()
    assert r2["ok"] is False
    print("test_lifeline_once_only: PASS")


def test_quit_before_milestone_gives_no_level():
    api = make_api()
    api.start_contestant("Eve")
    result = api.quit_game()
    assert result["ok"]
    assert result["milestone_label"] == "No Level", result
    assert result["points"] == 0
    print("test_quit_before_milestone_gives_no_level: PASS")


def test_final_question_excludes_level4_used_pool():
    api = make_api()
    api.start_contestant("Finn")
    level4_used = {api.questions[i]["question"] for i in range(15, 20)}
    final_q = api.questions[20]["question"]
    assert final_q not in level4_used, "Q21 must not repeat a Q16-20 question"
    print("test_final_question_excludes_level4_used_pool: PASS")


def test_cross_contestant_global_exclusion():
    import random

    api = make_api()
    all_level4 = api._bank[4]
    assert len(all_level4) >= 7, "sample bank needs enough level-4 questions for this test"
    # Keep only the LAST question untouched; mark every other level-4
    # question (including what will deterministically be this contestant's
    # own Q16-20 picks, since shuffle is disabled below) as already used
    # in a level-4 slot by an earlier contestant this session.
    untouched = all_level4[-1]["question"]
    api.level4_ever_used = {q["question"] for q in all_level4[:-1]}

    original_shuffle = random.shuffle
    random.shuffle = lambda seq: None  # deterministic bank order for this test
    try:
        api.start_contestant("Grace")
    finally:
        random.shuffle = original_shuffle

    final_q_text = api.questions[20]["question"]
    assert final_q_text == untouched, (
        f"expected the one still-untouched level-4 question to be forced into Q21, got: {final_q_text}"
    )
    print("test_cross_contestant_global_exclusion: PASS")


def test_abort_does_not_log(tmp_desktop_check=True):
    api = make_api()
    api.start_contestant("Ghost")
    r = api.abort_game()
    assert r["ok"]
    assert api.active is False
    assert api.name is None
    print("test_abort_does_not_log: PASS (no assertion on file, just state reset)")


if __name__ == "__main__":
    test_full_win()
    test_wrong_fallback()
    test_timeout_forces_wrong_even_if_correct_was_selected()
    test_lifeline_once_only()
    test_quit_before_milestone_gives_no_level()
    test_final_question_excludes_level4_used_pool()
    test_cross_contestant_global_exclusion()
    test_abort_does_not_log()
    print("\nALL SMOKE TESTS PASSED")
