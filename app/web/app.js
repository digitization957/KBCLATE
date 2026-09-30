(function () {
  "use strict";

  const MILESTONE_MAP = { 5: 1, 10: 2, 15: 3, 20: 4, 21: 5 };
  const LEVEL_LABEL = { 0: "No Level", 1: "Level 1", 2: "Level 2", 3: "Level 3", 4: "Level 4", 5: "FINAL WINNER" };

  const screens = {
    idle: document.getElementById("screen-idle"),
    name: document.getElementById("screen-name"),
    intro: document.getElementById("screen-intro"),
    game: document.getElementById("screen-game"),
    exit: document.getElementById("screen-exit"),
    winner: document.getElementById("screen-winner"),
  };

  const el = (id) => document.getElementById(id);

  const sfx = {
    intro: el("sfx-intro"),
    beforeQue: el("sfx-before-que"),
    lock: el("sfx-lock"),
    correct: el("sfx-correct"),
    wrong: el("sfx-wrong"),
    tick: el("sfx-tick"),
  };

  function playSfx(a) {
    try {
      a.pause();
      a.currentTime = 0;
      a.play().catch(() => {});
    } catch (e) { /* ignore */ }
  }
  function stopSfx(a) {
    try { a.pause(); a.currentTime = 0; } catch (e) { /* ignore */ }
  }

  function showScreen(name) {
    Object.values(screens).forEach((s) => s.classList.remove("screen--active"));
    screens[name].classList.add("screen--active");
  }

  function api() {
    return window.pywebview && window.pywebview.api;
  }

  // ---------------- state ----------------
  let selectedIdx = null;
  let selectedText = null;
  let locked = false;
  let timerInterval = null;
  let currentQuestion = null; // last response from get_current_question

  // ---------------- confirm modal ----------------
  const modal = el("confirm-modal");
  let confirmCallback = null;
  function askConfirm(message, onConfirm) {
    el("confirm-message").textContent = message;
    confirmCallback = onConfirm;
    modal.classList.remove("hidden");
  }
  el("confirm-cancel").addEventListener("click", () => {
    modal.classList.add("hidden");
    confirmCallback = null;
  });
  el("confirm-ok").addEventListener("click", () => {
    modal.classList.add("hidden");
    if (confirmCallback) confirmCallback();
    confirmCallback = null;
  });

  // ---------------- IDLE screen ----------------
  function enterIdle() {
    stopAllSfx();
    showScreen("idle");
    api().check_bank().then((res) => {
      const warn = el("bank-warning");
      if (!res.ok) {
        warn.textContent = "Question bank problem: " + res.error;
        warn.classList.remove("hidden");
      } else {
        warn.classList.add("hidden");
      }
    });
  }

  function stopAllSfx() {
    Object.values(sfx).forEach(stopSfx);
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
  }

  el("btn-new-contestant").addEventListener("click", () => {
    el("input-name").value = "";
    el("name-error").classList.add("hidden");
    el("btn-start-game").disabled = true;
    showScreen("name");
    el("input-name").focus();
  });

  // ---------------- NAME screen ----------------
  el("input-name").addEventListener("input", () => {
    el("btn-start-game").disabled = el("input-name").value.trim().length === 0;
  });
  el("input-name").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !el("btn-start-game").disabled) el("btn-start-game").click();
  });
  el("btn-back-idle").addEventListener("click", enterIdle);

  el("btn-start-game").addEventListener("click", () => {
    const name = el("input-name").value.trim();
    if (!name) return;
    contestantName = name;
    api().start_contestant(name).then((res) => {
      if (!res.ok) {
        el("name-error").textContent = res.error || "Could not start game.";
        el("name-error").classList.remove("hidden");
        return;
      }
      enterIntro(res.name);
    });
  });

  // ---------------- INTRO screen ----------------
  function enterIntro(name) {
    el("intro-contestant-name").textContent = name;
    showScreen("intro");
    playSfx(sfx.intro);

    let moved = false;
    const proceed = () => {
      if (moved) return;
      moved = true;
      beginGameplay();
    };
    sfx.intro.onended = proceed;
    // fallback in case audio fails to load/play
    setTimeout(proceed, 6000);
  }

  // ---------------- GAME screen ----------------
  function beginGameplay() {
    showScreen("game");
    loadQuestion();
  }

  function loadQuestion() {
    stopSfx(sfx.beforeQue);
    api().get_current_question().then((q) => {
      if (!q.ok) return;
      currentQuestion = q;
      selectedIdx = null;
      selectedText = null;
      locked = false;

      el("header-name-pill").textContent = contestantName;
      el("header-level").textContent = q.level === "final" ? "FINAL QUESTION" : "LEVEL " + q.level;
      el("header-points").textContent = q.points;
      el("q-number").textContent = "Q" + q.number;
      el("question-text").textContent = q.question;

      const buttons = document.querySelectorAll(".option-btn");
      buttons.forEach((btn, i) => {
        btn.classList.remove("selected", "correct", "wrong", "removed");
        btn.disabled = false;
        const text = q.options[i] || "";
        btn.querySelector(".option-text").textContent = text;
        btn.dataset.text = text;
      });

      el("btn-lock-in").disabled = true;
      el("btn-lock-in").classList.remove("hidden");
      el("btn-next-question").classList.add("hidden");
      el("btn-lifeline").disabled = !q.lifeline_available;
      el("btn-quit").disabled = false;
      el("lifeline-badge-visual").classList.toggle("lifeline-badge--used", !q.lifeline_available);

      renderLadder(q.number, q.milestone_level);
      setupTimer(q.timer_seconds);
      playSfx(sfx.beforeQue);
    });
  }

  let contestantName = "";

  function renderLadder(currentNumber, milestoneLevel) {
    const list = el("ladder-list");
    list.innerHTML = "";
    for (let n = 1; n <= 21; n++) {
      const row = document.createElement("div");
      row.className = "ladder-row";
      const isMilestone = !!MILESTONE_MAP[n];
      if (isMilestone) row.classList.add("milestone");
      if (isMilestone && MILESTONE_MAP[n] <= milestoneLevel) row.classList.add("reached");
      if (n === currentNumber) row.classList.add("current");

      const left = document.createElement("span");
      left.className = "ladder-label";
      left.textContent = isMilestone ? LEVEL_LABEL[MILESTONE_MAP[n]] : "Q" + n;
      const right = document.createElement("span");
      right.textContent = (n * 5) + " pts";

      row.appendChild(left);
      row.appendChild(right);
      list.appendChild(row);
    }
  }

  function setupTimer(seconds) {
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    const ring = el("timer-ring");
    if (!seconds || seconds <= 0) {
      ring.classList.add("hidden");
      return;
    }
    ring.classList.remove("hidden");
    ring.classList.remove("timer-warn");
    ring.style.setProperty("--pct", 100);
    let remaining = seconds;
    const total = seconds;
    el("timer-value").textContent = remaining;
    timerInterval = setInterval(() => {
      remaining -= 1;
      el("timer-value").textContent = Math.max(remaining, 0);
      ring.style.setProperty("--pct", Math.max(remaining, 0) / total * 100);
      if (remaining <= 10) ring.classList.add("timer-warn");
      if (remaining <= 10 && remaining > 0) playSfx(sfx.tick);
      if (remaining <= 0) {
        clearInterval(timerInterval);
        timerInterval = null;
        handleTimeout();
      }
    }, 1000);
  }

  function handleTimeout() {
    if (locked) return;
    screens.game.classList.add("timeout-flash");
    setTimeout(() => screens.game.classList.remove("timeout-flash"), 900);
    api().select_option(null).then(() => performLockIn(true));
  }

  // option selection
  document.querySelectorAll(".option-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (locked || btn.classList.contains("removed")) return;
      document.querySelectorAll(".option-btn").forEach((b) => b.classList.remove("selected"));
      btn.classList.add("selected");
      selectedIdx = parseInt(btn.dataset.idx, 10);
      selectedText = btn.dataset.text;
      api().select_option(selectedText);
      el("btn-lock-in").disabled = false;
    });
  });

  el("btn-lock-in").addEventListener("click", () => performLockIn(false));

  function performLockIn(isTimeout) {
    if (locked) return;
    locked = true;
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
    el("btn-lock-in").disabled = true;
    document.querySelectorAll(".option-btn").forEach((b) => (b.disabled = true));
    el("btn-lifeline").disabled = true;
    el("btn-quit").disabled = true;
    stopSfx(sfx.beforeQue);
    playSfx(sfx.lock);

    setTimeout(() => {
      api().lock_in().then(handleLockResult);
    }, 1500);
  }

  function markOptionByText(text, cls) {
    document.querySelectorAll(".option-btn").forEach((b) => {
      if (b.dataset.text === text) b.classList.add(cls);
    });
  }

  function handleLockResult(res) {
    if (!res.ok) return;
    el("header-points").textContent = res.points;

    if (res.correct) {
      if (selectedText) markOptionByText(selectedText, "correct");
      playSfx(sfx.correct);

      if (res.win) {
        setTimeout(() => enterWinner(res.name), 1800);
        return;
      }

      if (res.milestone_hit) {
        renderLadder(currentQuestion.number, res.milestone_level);
      }
      el("btn-next-question").classList.remove("hidden");
      el("btn-lock-in").classList.add("hidden");
      el("btn-quit").disabled = false;
      return;
    }

    // wrong / timeout
    if (selectedText) markOptionByText(selectedText, "wrong");
    markOptionByText(res.correct_answer, "correct");
    playSfx(sfx.wrong);

    setTimeout(() => {
      enterExit({
        outcome: "WRONG ANSWER",
        name: res.name,
        milestone_label: res.milestone_label,
        points: res.points,
      });
    }, 2600);
  }

  el("btn-next-question").addEventListener("click", () => {
    api().next_question().then((res) => {
      if (res.ok) loadQuestion();
    });
  });

  el("btn-lifeline").addEventListener("click", () => {
    if (el("btn-lifeline").disabled) return;
    api().use_lifeline().then((res) => {
      if (!res.ok) return;
      el("btn-lifeline").disabled = true;
      // Force a fresh choice from the remaining two options: a pre-existing
      // selection may have been one of the two just removed, and locking
      // that in silently would submit an answer the operator can no longer see.
      selectedIdx = null;
      selectedText = null;
      el("btn-lock-in").disabled = true;
      document.querySelectorAll(".option-btn").forEach((b) => {
        b.classList.remove("selected");
        if (!res.options.includes(b.dataset.text)) {
          b.classList.add("removed");
          b.disabled = true;
        }
      });
    });
  });

  el("btn-quit").addEventListener("click", () => {
    askConfirm("Quit this contestant's game? They'll keep their last secured level.", () => {
      if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
      api().quit_game().then((res) => {
        if (!res.ok) return;
        enterExit({
          outcome: "QUIT",
          name: res.name,
          milestone_label: res.milestone_label,
          points: res.points,
        });
      });
    });
  });

  el("btn-abort").addEventListener("click", () => {
    askConfirm("Abort this run without recording a result?", () => {
      if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
      stopAllSfx();
      api().abort_game().then(() => enterIdle());
    });
  });

  // ---------------- EXIT screen ----------------
  function enterExit(data) {
    stopAllSfx();
    el("exit-outcome-label").textContent = data.outcome === "QUIT" ? "CONTESTANT QUIT" : "GAME OVER";
    el("exit-name").textContent = data.name;
    el("exit-level").textContent = data.milestone_label;
    el("exit-points").textContent = data.points + " points";
    showScreen("exit");
  }

  el("btn-next-contestant-exit").addEventListener("click", () => {
    api().next_contestant().then(() => enterIdle());
  });

  // ---------------- WINNER screen ----------------
  function enterWinner(name) {
    stopAllSfx();
    el("winner-name").textContent = name;
    showScreen("winner");
    playSfx(sfx.intro);
  }

  el("btn-next-contestant-winner").addEventListener("click", () => {
    api().next_contestant().then(() => enterIdle());
  });

  // ---------------- kiosk exit shortcut ----------------
  document.addEventListener("keydown", (e) => {
    if (e.ctrlKey && e.altKey && (e.key === "q" || e.key === "Q")) {
      askConfirm("Exit the kiosk app?", () => api().exit_app());
    }
  });

  // ---------------- boot ----------------
  function boot() {
    enterIdle();
    playSfx(sfx.intro);
  }

  if (window.pywebview) {
    boot();
  } else {
    window.addEventListener("pywebviewready", boot);
  }
})();
