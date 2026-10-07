# Centipede Repair Lab

This project is a single-file Centipede-lite clone using **Pygame**. It introduces students to segment-chain movement, chain splitting, and projectile-vs-grid collision using a small, readable object-oriented codebase.

---

## What's Provided

A working Centipede-lite game with:

- A player confined to the bottom band of the screen who fires straight up
- A centipede made of chained segments that winds back and forth across the screen, dropping a row whenever it hits a border or a mushroom
- A field of mushrooms that block the centipede's path and can be shot down
- Wave-based difficulty, lives, and scoring, including splitting the centipede into two independent chains when a body segment is hit

It has **one deliberate bug** and **three optional features** left as empty functions. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python game.py
```

**Controls:** Arrow keys to move, Space to fire, `R` to reset.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the mushroom durability bug

> A mushroom is supposed to survive four hits before it's cleared from the field. In the current build, mushrooms disappear after only three hits instead. Check the comparison in `hit_mushroom` against `MUSHROOM_HP` (which is defined as 4 near the top of the file).

### Task 2: Implement `mushroom_color(hp)`

> Called once per mushroom per frame in `draw`, as `color = mushroom_color(hp) or (200 - (MUSHROOM_HP - hp) * 40, 80, 170)`. It receives the mushroom's remaining hit points (1 through `MUSHROOM_HP`) and should return an `(r, g, b)` color, or `None` to keep the default (which fades as the mushroom takes damage). Idea: make a mushroom flash white on the frame it's hit.

### Task 3: Implement `on_segment_hit(segment, score)`

> Called from `split_chain` right after a body segment is destroyed, the chain it belonged to is split into two, and points are added (100 for a head shot, 10 otherwise). It receives the `Segment` that was hit and the score after this hit's points were added. Its return value is ignored. Idea: a spark effect at the segment's last position, or a bonus for head shots beyond the extra points already awarded.

### Task 4: Implement `wave_speed_bonus(wave)`

> Called every frame in `update`, as `effective_tick = TICK / (wave_speed_bonus(self.wave) or 1)`, where a smaller tick means segments step more often (move faster). It receives the current wave number and should return a speed multiplier, or `None` for the default speed. Idea: return `1 + 0.15 * (wave - 1)` so later waves are noticeably faster.

---

## Expected Behavior

- The centipede reverses direction and drops a row whenever it reaches a border or a mushroom, and never steps outside the playfield
- Shooting a mushroom four times clears it from the field; fewer hits just chips away at its color
- Shooting the head segment shortens the chain by one and keeps a single head; shooting a body segment splits the chain into two independent chains, each with its own head
- Touching any segment costs a life, unless the player is briefly invulnerable right after a respawn
- Clearing every segment starts the next, faster wave

---

## Folder Structure

```
centipede/
├── game.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
