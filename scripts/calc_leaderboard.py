#!/usr/bin/env python3
"""
calc_leaderboard.py
Reads all prediction files and the results file,
calculates scores, and writes data/leaderboard.json.

Scoring rules:
  - 3 points for each correct match result (1/X/2)
  - 10 points for guessing the tournament champion
"""

import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
PREDICTIONS_DIR = ROOT / "data" / "predictions"
RESULTS_FILE    = ROOT / "data" / "results.json"
LEADERBOARD_FILE = ROOT / "data" / "leaderboard.json"

MATCH_POINTS    = 3
CHAMPION_POINTS = 10


def load_results():
    with open(RESULTS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    matches = {
        k: v["result"]
        for k, v in data.get("matches", {}).items()
        if v.get("result") is not None
    }
    return matches, data.get("champion")


def load_predictions():
    participants = []
    for path in sorted(PREDICTIONS_DIR.glob("*.json")):
        if path.name == ".gitkeep":
            continue
        with open(path, encoding="utf-8") as f:
            try:
                p = json.load(f)
                participants.append(p)
            except json.JSONDecodeError:
                print(f"  ⚠️  Skipping malformed file: {path.name}")
    return participants


def score_participant(pred, played_results, result_champion):
    preds = pred.get("predictions", {})
    points = 0
    correct = 0
    total_predicted = 0

    for match_id, result in played_results.items():
        if match_id in preds:
            total_predicted += 1
            if preds[match_id] == result:
                points += MATCH_POINTS
                correct += 1

    champion_correct = False
    if result_champion and pred.get("champion") == result_champion:
        points += CHAMPION_POINTS
        champion_correct = True

    return {
        "name":             pred.get("name", ""),
        "surname":          pred.get("surname", ""),
        "emoji":            pred.get("emoji", "⚽"),
        "points":           points,
        "correct":          correct,
        "total_predicted":  total_predicted,
        "champion":         pred.get("champion") or "-",
        "champion_correct": champion_correct,
        "submitted_at":     pred.get("submitted_at", ""),
    }


def calc():
    print("📊 Calculating leaderboard...")

    played_results, result_champion = load_results()
    participants = load_predictions()

    print(f"   {len(played_results)} matches played, {len(participants)} participants")

    rankings = [
        score_participant(p, played_results, result_champion)
        for p in participants
    ]

    # Sort: points desc, then surname asc, then name asc
    rankings.sort(key=lambda x: (-x["points"], x["surname"].lower(), x["name"].lower()))

    for i, r in enumerate(rankings):
        r["rank"] = i + 1

    leaderboard = {
        "updated_at":      datetime.now(timezone.utc).isoformat(),
        "matches_played":  len(played_results),
        "total_matches":   72,
        "result_champion": result_champion,
        "rankings":        rankings,
    }

    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=2)

    print(f"✅ Leaderboard written: {len(rankings)} participants ranked")
    if rankings:
        top = rankings[0]
        print(f"   🥇 Leader: {top['emoji']} {top['name']} {top['surname']} — {top['points']} pts")


if __name__ == "__main__":
    calc()
