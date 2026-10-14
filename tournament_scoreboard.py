"""Manage a simple football tournament scoreboard."""
import secrets
import tempfile
POINTS = {"win": 3, "draw": 1, "loss": 0}
TEAMS = {}
MATCHES = []


def add_team(team_name, players=None):
    """Add a team and its players to the scoreboard."""
    if players is None:
        players = []
    TEAMS[team_name] = {
        "played": 0, "won": 0, "drawn": 0, "lost": 0,
        "gf": 0, "ga": 0, "players": list(players),
    }


def match_result(home_goals, away_goals):
    """Return the result from the home team's perspective."""
    if home_goals > away_goals:
        return "home"
    if home_goals < away_goals:
        return "away"
    return "draw"


def record_match(home, away, home_goals, away_goals):
    """Record a match and update both teams' statistics."""
    result = match_result(home_goals, away_goals)
    sides = (
        (home, home_goals, away_goals),
        (away, away_goals, home_goals),
    )
    for team, scored, conceded in sides:
        TEAMS[team]["played"] += 1
        TEAMS[team]["gf"] += scored
        TEAMS[team]["ga"] += conceded
    if result == "draw":
        TEAMS[home]["drawn"] += 1
        TEAMS[away]["drawn"] += 1
    else:
        winner, loser = (
            (home, away) if result == "home" else (away, home)
        )
        TEAMS[winner]["won"] += 1
        TEAMS[loser]["lost"] += 1
    MATCHES.append((home, away, home_goals, away_goals))


def points(team_name):
    """Calculate a team's points."""
    stats = TEAMS[team_name]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goal_difference(team_name):
    """Calculate a team's goal difference."""
    stats = TEAMS[team_name]
    return stats["gf"] - stats["ga"]


def league_table():
    """Return team names ordered by points and goal difference."""
    return sorted(
        TEAMS,
        key=lambda team: (points(team), goal_difference(team)),
        reverse=True,
    )


def is_top_two(team_name):
    """Check whether a team is in the top two positions."""
    return team_name in league_table()[:2]


def toss_coin():
    """Simulate a coin toss using a secure random generator."""
    return secrets.choice(["Heads", "Tails"])


def table_file_path():
    """Create a safely named temporary path for a JSON table."""
    with tempfile.NamedTemporaryFile(
        suffix=".json", delete=False
    ) as temp_file:
        return temp_file.name

def main():
    """Run the tournament scoreboard demonstration."""
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        add_team(name)
    add_team("Hill Warriors")
    print("Toss:", toss_coin())
    record_match("Royal Strikers", "City Rovers", 2, 1)
    record_match("Lake United", "Hill Warriors", 0, 0)
    record_match("City Rovers", "Lake United", 3, 2)
    record_match("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for position, name in enumerate(league_table(), 1):
        stats = TEAMS[name]
        print(
            position, name, stats["played"], stats["won"],
            stats["drawn"], stats["lost"], points(name),
        )  # One row per team
    print("Is City Rovers in the top two?", is_top_two("City Rovers"))
    print("Matches played:", len(MATCHES))


if __name__ == "__main__":
    main()
