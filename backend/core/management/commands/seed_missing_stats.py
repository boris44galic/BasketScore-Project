import random
from django.core.management.base import BaseCommand
from matches.models import Match
from players.models import Player, PlayerStats, PlayerMatchStatus


def rnd(lo, hi):
    return random.randint(lo, hi)


def make_stats(match, player, starter=True):
    in_game = starter or random.random() > 0.15
    mins = rnd(20, 38) if starter else (rnd(5, 20) if in_game else 0)
    if not in_game:
        mins = 0

    PlayerMatchStatus.objects.get_or_create(
        player=player,
        match=match,
        defaults={"in_game": in_game, "starter": starter},
    )

    if not in_game:
        return

    fg_att = rnd(4, 16)
    fg_made = rnd(0, fg_att)
    three_att = rnd(0, min(fg_att, 8))
    three_made = rnd(0, three_att)
    ft_att = rnd(0, 8)
    ft_made = rnd(0, ft_att)
    pts = fg_made * 2 + three_made + ft_made

    PlayerStats.objects.get_or_create(
        player=player,
        match=match,
        defaults={
            "points": pts,
            "rebounds": rnd(0, 12),
            "assists": rnd(0, 10),
            "steals": rnd(0, 4),
            "blocks": rnd(0, 4),
            "turnovers": rnd(0, 5),
            "fouls": rnd(0, 5),
            "minutes_played": mins,
            "fg_made": fg_made,
            "fg_attempted": fg_att,
            "three_pt_made": three_made,
            "three_pt_attempted": three_att,
            "ft_made": ft_made,
            "ft_attempted": ft_att,
        },
    )


class Command(BaseCommand):
    help = "Seed player stats for finished/live matches that are missing them"

    def handle(self, *args, **options):
        random.seed(99)

        target_statuses = ["finished", "live", "Finished", "Live"]
        matches = Match.objects.filter(
            status__name__in=target_statuses
        ).select_related("home_team", "away_team", "status")

        filled = 0
        skipped = 0

        for match in matches:
            if PlayerStats.objects.filter(match=match).exists():
                skipped += 1
                continue

            home_players = list(Player.objects.filter(team=match.home_team))
            away_players = list(Player.objects.filter(team=match.away_team))

            if not home_players and not away_players:
                self.stdout.write(f"  No players found for match {match.id} ({match.home_team} vs {match.away_team}), skipping")
                continue

            for i, p in enumerate(home_players):
                make_stats(match, p, starter=(i < 5))
            for i, p in enumerate(away_players):
                make_stats(match, p, starter=(i < 5))

            filled += 1
            self.stdout.write(f"  Filled stats for match {match.id}: {match.home_team} vs {match.away_team}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Filled: {filled} matches, Skipped (already had stats): {skipped}"
        ))
