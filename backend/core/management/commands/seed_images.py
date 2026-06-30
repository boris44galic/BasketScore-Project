import hashlib
import os
import time
from io import BytesIO

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from leagues.models import League
from players.models import Player
from teams.models import Team

TIMEOUT = 15
RETRY_DELAY = 1.5

_HEADERS_DEFAULT = {"User-Agent": "Mozilla/5.0 (compatible; seeder/1.0)"}
_HEADERS_WIKI = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Referer": "https://en.wikipedia.org/",
}

_WIKIMEDIA_API_TEMPLATE = (
    "https://{host}/w/api.php"
    "?action=query&prop=imageinfo&iiprop=url"
    "&titles=File:{filename}&format=json"
)

# Wikipedia REST summary pages for team/league logos (fallback thumbnail source).
_WIKI_PAGES = {
    "EA7 Olimpia Milano":       "Pallacanestro_Olimpia_Milano",
    "Fenerbahce Beko":          "Fenerbah%C3%A7e_Basketball",
    "Anadolu Efes":             "Anadolu_Efes",
    "Panathinaikos BC":         "Panathinaikos_B.C.",
    "Olympiacos BC":            "Olympiacos_B.C.",
    "Alba Berlin":              "ALBA_Berlin",
    "Maccabi Tel Aviv":         "Maccabi_Tel_Aviv_B.C.",
    "AS Monaco Basketball":     "AS_Monaco_Basketball",
    "Saski Baskonia":           "Saski_Baskonia",
    "Zalgiris Kaunas":          "BC_%C5%BDalgiris",
    "Valencia Basket":          "Valencia_Basket",
    "Paris Basketball":         "Paris_Basketball",
    "Virtus Segafredo Bologna": "Pallacanestro_Virtus_Bologna",
    "Euroleague":               "EuroLeague",
}

# ESPN 3-letter abbreviations for NBA team rosters.
NBA_ESPN_ABBR = {
    "Boston Celtics":           "bos",
    "New York Knicks":          "ny",
    "Brooklyn Nets":            "bkn",
    "Philadelphia 76ers":       "phi",
    "Toronto Raptors":          "tor",
    "Chicago Bulls":            "chi",
    "Cleveland Cavaliers":      "cle",
    "Detroit Pistons":          "det",
    "Indiana Pacers":           "ind",
    "Milwaukee Bucks":          "mil",
    "Atlanta Hawks":            "atl",
    "Charlotte Hornets":        "cha",
    "Miami Heat":               "mia",
    "Orlando Magic":            "orl",
    "Washington Wizards":       "wsh",
    "Denver Nuggets":           "den",
    "Minnesota Timberwolves":   "min",
    "Oklahoma City Thunder":    "okc",
    "Portland Trail Blazers":   "por",
    "Utah Jazz":                "utah",
    "Golden State Warriors":    "gs",
    "Los Angeles Lakers":       "lal",
    "LA Clippers":              "lac",
    "Phoenix Suns":             "phx",
    "Sacramento Kings":         "sac",
    "Dallas Mavericks":         "dal",
    "Houston Rockets":          "hou",
    "Memphis Grizzlies":        "mem",
    "New Orleans Pelicans":     "no",
    "San Antonio Spurs":        "sa",
}

# Fallback URL lists for Euroleague team logos (tried in order).
EUROLEAGUE_LOGO_URLS = {
    "Real Madrid":              ["https://a.espncdn.com/i/teamlogos/soccer/500/86.png"],
    "FC Barcelona":             ["https://a.espncdn.com/i/teamlogos/soccer/500/83.png"],
    "EA7 Olimpia Milano":       ["https://upload.wikimedia.org/wikipedia/commons/9/9a/Pallacanestro_Olimpia_Milano_logo.png"],
    "Fenerbahce Beko":          ["https://a.espncdn.com/i/teamlogos/soccer/500/2375.png"],
    "Anadolu Efes":             ["https://upload.wikimedia.org/wikipedia/en/f/f7/Anadolu_Efes_S.K._logo.png"],
    "Panathinaikos BC":         ["https://upload.wikimedia.org/wikipedia/en/8/85/PAO_BC_logo.png"],
    "Olympiacos BC":            ["https://a.espncdn.com/i/teamlogos/soccer/500/3064.png"],
    "Bayern Munich Basketball": ["https://a.espncdn.com/i/teamlogos/soccer/500/132.png"],
    "Alba Berlin":              ["https://upload.wikimedia.org/wikipedia/commons/6/69/ALBA_BERLIN_Logo.svg"],
    "Partizan Mozzart Bet":     ["https://a.espncdn.com/i/teamlogos/soccer/500/382.png"],
    "Crvena Zvezda":            ["https://a.espncdn.com/i/teamlogos/soccer/500/385.png"],
    "Maccabi Tel Aviv":         ["https://upload.wikimedia.org/wikipedia/en/e/e7/Maccabi_Tel_Aviv_BC_logo.png"],
    "AS Monaco Basketball":     ["https://a.espncdn.com/i/teamlogos/soccer/500/1969.png"],
    "Saski Baskonia":           ["https://upload.wikimedia.org/wikipedia/en/4/41/Saski_Baskonia_logo.png"],
    "Virtus Segafredo Bologna": ["https://upload.wikimedia.org/wikipedia/it/7/71/Virtus_Pallacanestro_Bologna_logo.png"],
    "Zalgiris Kaunas":          ["https://upload.wikimedia.org/wikipedia/en/2/2c/BC_Zalgiris_logo.png"],
    "Valencia Basket":          ["https://upload.wikimedia.org/wikipedia/en/e/e4/Valencia_Basket_logo.png"],
    "Paris Basketball":         ["https://upload.wikimedia.org/wikipedia/fr/3/37/Paris_Basketball_logo.png"],
}

LEAGUE_LOGO_URLS = {
    "NBA":         ["https://a.espncdn.com/i/teamlogos/leagues/500/nba.png"],
    "Euroleague":  ["https://upload.wikimedia.org/wikipedia/en/0/04/Euroleague_Basketball_logo.png"],
}

# Brand colours (bg, fg) used for placeholder generation.
TEAM_COLORS = {
    "Boston Celtics":           ("#007A33", "#FFFFFF"),
    "New York Knicks":          ("#006BB6", "#F58426"),
    "Brooklyn Nets":            ("#000000", "#FFFFFF"),
    "Philadelphia 76ers":       ("#006BB6", "#ED174C"),
    "Toronto Raptors":          ("#CE1141", "#000000"),
    "Chicago Bulls":            ("#CE1141", "#000000"),
    "Cleveland Cavaliers":      ("#860038", "#FDBB30"),
    "Detroit Pistons":          ("#C8102E", "#1D42BA"),
    "Indiana Pacers":           ("#002D62", "#FDBB30"),
    "Milwaukee Bucks":          ("#00471B", "#EEE1C6"),
    "Atlanta Hawks":            ("#E03A3E", "#C1D32F"),
    "Charlotte Hornets":        ("#1D1160", "#00788C"),
    "Miami Heat":               ("#98002E", "#F9A01B"),
    "Orlando Magic":            ("#0077C0", "#C4CED4"),
    "Washington Wizards":       ("#002B5C", "#E31837"),
    "Denver Nuggets":           ("#0E2240", "#FEC524"),
    "Minnesota Timberwolves":   ("#0C2340", "#236192"),
    "Oklahoma City Thunder":    ("#007AC1", "#EF3B24"),
    "Portland Trail Blazers":   ("#E03A3E", "#000000"),
    "Utah Jazz":                ("#002B5C", "#00471B"),
    "Golden State Warriors":    ("#1D428A", "#FFC72C"),
    "Los Angeles Lakers":       ("#552583", "#FDB927"),
    "LA Clippers":              ("#C8102E", "#1D428A"),
    "Phoenix Suns":             ("#1D1160", "#E56020"),
    "Sacramento Kings":         ("#5A2D81", "#63727A"),
    "Dallas Mavericks":         ("#00538C", "#002B5E"),
    "Houston Rockets":          ("#CE1141", "#000000"),
    "Memphis Grizzlies":        ("#5D76A9", "#12173F"),
    "New Orleans Pelicans":     ("#0C2340", "#C8102E"),
    "San Antonio Spurs":        ("#C4CED4", "#000000"),
    "Real Madrid":              ("#FFFFFF", "#00529F"),
    "FC Barcelona":             ("#A50044", "#004D98"),
    "EA7 Olimpia Milano":       ("#CC0000", "#FFFFFF"),
    "Fenerbahce Beko":          ("#FFED00", "#003D7D"),
    "Anadolu Efes":             ("#003D7D", "#D4AF37"),
    "Panathinaikos BC":         ("#006633", "#FFFFFF"),
    "Olympiacos BC":            ("#CC0000", "#FFFFFF"),
    "Bayern Munich Basketball": ("#DC052D", "#0066B2"),
    "Alba Berlin":              ("#0000A0", "#FFFFFF"),
    "Partizan Mozzart Bet":     ("#000000", "#FFFFFF"),
    "Crvena Zvezda":            ("#CC0000", "#FFFFFF"),
    "Maccabi Tel Aviv":         ("#FFD700", "#0057B7"),
    "AS Monaco Basketball":     ("#CC0000", "#FFFFFF"),
    "Saski Baskonia":           ("#003DA5", "#FFFFFF"),
    "Virtus Segafredo Bologna": ("#000000", "#FFFFFF"),
    "Zalgiris Kaunas":          ("#006400", "#FFFFFF"),
    "Valencia Basket":          ("#000000", "#FF7F00"),
    "Paris Basketball":         ("#FF0000", "#FFFFFF"),
}


# ── Core fetch helpers ────────────────────────────────────────────────────────

def _hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _resolve_wikimedia_url(wiki_url: str) -> str | None:
    """Resolve a direct upload.wikimedia.org URL to the real CDN URL via API."""
    try:
        after = wiki_url.replace("https://upload.wikimedia.org/wikipedia/", "")
        parts = after.split("/")
        wiki = parts[0]
        filename = parts[-1]
        host = "commons.wikimedia.org" if wiki == "commons" else f"{wiki}.wikipedia.org"
        api_url = _WIKIMEDIA_API_TEMPLATE.format(host=host, filename=filename)
        r = requests.get(api_url, timeout=TIMEOUT, headers=_HEADERS_WIKI)
        if r.status_code != 200:
            return None
        for page in r.json().get("query", {}).get("pages", {}).values():
            url = (page.get("imageinfo") or [{}])[0].get("url")
            if url:
                return url
    except Exception:
        pass
    return None


def _fetch(url: str, retries: int = 4) -> bytes | None:
    is_wiki = "wikipedia.org" in url or "wikimedia.org" in url
    if "upload.wikimedia.org" in url:
        resolved = _resolve_wikimedia_url(url)
        if resolved and resolved != url:
            url = resolved
    headers = _HEADERS_WIKI if is_wiki else _HEADERS_DEFAULT
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=TIMEOUT, headers=headers, allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 500:
                return r.content
            if r.status_code == 429:
                time.sleep(5 * (2 ** attempt))
                continue
        except requests.RequestException:
            pass
        if attempt < retries - 1:
            time.sleep(RETRY_DELAY)
    return None


def _fetch_first(urls: list[str]) -> tuple[bytes | None, str | None]:
    for url in urls:
        data = _fetch(url)
        if data:
            return data, url
    return None, None


# ── Wikipedia thumbnail helpers ───────────────────────────────────────────────

def _wikipedia_thumb(page_slug: str) -> bytes | None:
    """Fetch a rendered thumbnail for any Wikipedia page slug."""
    try:
        time.sleep(1.0)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_slug}"
        r = requests.get(url, timeout=TIMEOUT, headers=_HEADERS_WIKI)
        if r.status_code != 200 or not r.text:
            return None
        thumb_url = r.json().get("thumbnail", {}).get("source")
        if not thumb_url:
            return None
        time.sleep(0.8)
        return _fetch(thumb_url)
    except Exception:
        return None


def _wikipedia_entity_thumb(entity_name: str) -> bytes | None:
    """Look up entity_name in _WIKI_PAGES map and fetch its thumbnail."""
    page = _WIKI_PAGES.get(entity_name)
    return _wikipedia_thumb(page) if page else None


def _wikipedia_player_thumb(first: str, last: str) -> bytes | None:
    """
    Try to find a player's Wikipedia page thumbnail.
    Tries "{First_Last}", "{Last,_First}" and a few other common patterns.
    """
    slug = f"{first}_{last}".replace(" ", "_")
    data = _wikipedia_thumb(slug)
    if data:
        return data
    # Some players have disambiguating suffixes or inverted name order
    slug2 = f"{last},_{first}".replace(" ", "_")
    return _wikipedia_thumb(slug2)


# ── ESPN helpers ──────────────────────────────────────────────────────────────

def _espn_build_nba_player_map() -> dict[str, int]:
    """
    Fetch all 30 NBA team rosters from ESPN and return {display_name: espn_id}.
    Uses ~30 requests instead of one per player.
    """
    result: dict[str, int] = {}
    for team_name, abbr in NBA_ESPN_ABBR.items():
        try:
            url = (
                f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
                f"/teams/{abbr}/roster"
            )
            r = requests.get(url, timeout=TIMEOUT, headers=_HEADERS_DEFAULT)
            if r.status_code != 200:
                continue
            for athlete in r.json().get("athletes", []):
                pid = athlete.get("id")
                name = athlete.get("displayName") or athlete.get("fullName")
                if pid and name:
                    result[name] = int(pid)
            time.sleep(0.4)
        except Exception:
            continue
    return result


def _espn_headshot(espn_id: int) -> bytes | None:
    url = f"https://a.espncdn.com/i/headshots/nba/players/full/{espn_id}.png"
    return _fetch(url)


# ── Placeholder generator ─────────────────────────────────────────────────────

def _make_placeholder_png(text: str, bg_hex: str, fg_hex: str, size: int = 256) -> bytes:
    bg = _hex_to_rgb(bg_hex)
    fg = _hex_to_rgb(fg_hex)
    img = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size // 3
        )
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - tw) / 2, (size - th) / 2), text, fill=fg, font=font)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _team_initials(name: str) -> str:
    words = [w for w in name.split() if w and w[0].isupper()]
    return f"{words[0][0]}{words[-1][0]}" if len(words) >= 2 else name[:2].upper()


def _is_svg(data: bytes) -> bool:
    sample = data[:512].lstrip()
    return sample.startswith(b"<svg") or b"<svg" in sample[:256]


def _svg_to_png(data: bytes) -> bytes:
    try:
        import cairosvg
        return cairosvg.svg2png(bytestring=data, output_width=256, output_height=256)
    except ImportError:
        return data


def _normalise(data: bytes, source_url: str | None) -> tuple[bytes, str]:
    if _is_svg(data) or (source_url and source_url.lower().endswith(".svg")):
        converted = _svg_to_png(data)
        ext = "png" if not _is_svg(converted) else "svg"
        return converted, ext
    return data, "png"


# ── Django ImageField save helpers ───────────────────────────────────────────

def _save_league_logo(league: League, data: bytes, ext: str) -> None:
    filename = f"{league.name.lower().replace(' ', '_')}.{ext}"
    league.logo.save(filename, ContentFile(data), save=False)
    league.save(update_fields=["logo"])


def _save_team_logo(team: Team, data: bytes, ext: str) -> None:
    filename = f"{team.name.lower().replace(' ', '_')}.{ext}"
    team.logo.save(filename, ContentFile(data), save=False)
    team.save(update_fields=["logo"])


def _save_player_image(player: Player, data: bytes) -> None:
    slug = f"{player.first_name}_{player.last_name}".lower().replace(" ", "_")
    uid = hashlib.md5(str(player.id).encode()).hexdigest()[:6]
    player.image_url.save(f"{slug}_{uid}.png", ContentFile(data), save=False)
    player.save(update_fields=["image_url"])


# ── Command ───────────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = "Seed images for leagues, teams, and players"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", action="store_true",
            help="Re-download and overwrite existing images",
        )
        parser.add_argument(
            "--only", choices=["leagues", "teams", "players"],
            help="Seed only a specific category",
        )

    def handle(self, *_args, **options):
        force = options["force"]
        only = options.get("only")

        media_root = settings.MEDIA_ROOT
        for subdir in ("league_logos", "team_logos", "player_images"):
            os.makedirs(os.path.join(media_root, subdir), exist_ok=True)

        if not only or only == "leagues":
            self._seed_leagues(force)
        if not only or only == "teams":
            self._seed_teams(force)
        if not only or only == "players":
            self._seed_players(force)

        self.stdout.write(self.style.SUCCESS("\nImage seeding complete!"))

    # ── Leagues ───────────────────────────────────────────────────────────────

    def _seed_leagues(self, force: bool) -> None:
        self.stdout.write("\n[Leagues]")
        for league in League.objects.all():
            if league.logo and not force:
                self.stdout.write(f"  SKIP  {league.name}")
                continue
            urls = LEAGUE_LOGO_URLS.get(league.name)
            if not urls:
                self.stdout.write(f"  SKIP  {league.name} (no URL defined)")
                continue

            data, winning_url = _fetch_first(urls)
            if not data:
                data = _wikipedia_entity_thumb(league.name)
                winning_url = None

            if data:
                data, ext = _normalise(data, winning_url)
                _save_league_logo(league, data, ext)
                self.stdout.write(f"  OK    {league.name}")
            else:
                _save_league_logo(
                    league,
                    _make_placeholder_png(league.name[:3].upper(), "#1a1a2e", "#e0e0e0"),
                    "png",
                )
                self.stdout.write(f"  FAIL  {league.name} — placeholder")

    # ── Teams ─────────────────────────────────────────────────────────────────

    def _seed_teams(self, force: bool) -> None:
        self.stdout.write("\n[Teams — NBA]")
        for team in Team.objects.filter(name__in=NBA_ESPN_ABBR):
            if team.logo and not force:
                self.stdout.write(f"  SKIP  {team.name}")
                continue
            abbr = NBA_ESPN_ABBR[team.name]
            data = _fetch(f"https://a.espncdn.com/i/teamlogos/nba/500/{abbr}.png")
            if data:
                _save_team_logo(team, data, "png")
                self.stdout.write(f"  OK    {team.name}")
            else:
                self._team_placeholder(team)
                self.stdout.write(f"  FAIL  {team.name} — placeholder")

        self.stdout.write("\n[Teams — Euroleague]")
        for team in Team.objects.filter(name__in=EUROLEAGUE_LOGO_URLS):
            if team.logo and not force:
                self.stdout.write(f"  SKIP  {team.name}")
                continue
            data, winning_url = _fetch_first(EUROLEAGUE_LOGO_URLS[team.name])
            if not data:
                data = _wikipedia_entity_thumb(team.name)
                winning_url = None
            if data:
                data, ext = _normalise(data, winning_url)
                _save_team_logo(team, data, ext)
                self.stdout.write(f"  OK    {team.name}")
            else:
                self._team_placeholder(team)
                self.stdout.write(f"  FAIL  {team.name} — placeholder")

    def _team_placeholder(self, team: Team) -> None:
        bg, fg = TEAM_COLORS.get(team.name, ("#1a1a2e", "#ffffff"))
        _save_team_logo(team, _make_placeholder_png(_team_initials(team.name), bg, fg), "png")

    # ── Players ───────────────────────────────────────────────────────────────

    def _seed_players(self, force: bool) -> None:
        nba_team_names = set(NBA_ESPN_ABBR.keys())

        # ── Step 1: build ESPN player ID map from all 30 team rosters ──────
        self.stdout.write("\n[Players — building ESPN roster map…]")
        espn_map = _espn_build_nba_player_map()
        self.stdout.write(f"  ESPN: {len(espn_map)} players found across 30 rosters")

        # ── Step 2: process each player ─────────────────────────────────────
        self.stdout.write("[Players — downloading photos]")
        players = Player.objects.select_related("team").all()
        total = players.count()
        ok = skip = placeholder = 0

        for player in players:
            if player.image_url and not force:
                skip += 1
                continue

            full_name = f"{player.first_name} {player.last_name}"
            team_name = player.team.name if player.team else ""
            is_nba = team_name in nba_team_names
            data = None

            if is_nba:
                # Primary: ESPN CDN headshot
                espn_id = espn_map.get(full_name)
                if espn_id:
                    data = _espn_headshot(espn_id)

            if not data:
                # Fallback for both NBA and EuroLeague: Wikipedia page thumbnail
                data = _wikipedia_player_thumb(player.first_name, player.last_name)

            if data:
                _save_player_image(player, data)
                ok += 1
            else:
                # Final fallback: team-coloured placeholder with initials
                bg, fg = TEAM_COLORS.get(team_name, ("#1a1a2e", "#ffffff"))
                initials = f"{player.first_name[0]}{player.last_name[0]}".upper()
                _save_player_image(player, _make_placeholder_png(initials, bg, fg))
                placeholder += 1

            done = ok + placeholder
            if done % 30 == 0:
                self.stdout.write(
                    f"  {done}/{total - skip}  ESPN/wiki={ok}  placeholder={placeholder}"
                )

        self.stdout.write(
            f"  Done: {ok} real photos · {placeholder} placeholders · {skip} skipped"
        )
