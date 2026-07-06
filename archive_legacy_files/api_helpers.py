"""
API helpers: Quote of the Day, GitHub, LeetCode, Codeforces
"""
import requests
import random
from datetime import date, datetime
from data.questions import MOTIVATIONAL_QUOTES

# ── Quote of the Day ──────────────────────────────────────
def get_quote_of_day() -> dict:
    """
    Try live API first; fall back to curated list seeded by today's date.
    """
    today = date.today()
    try:
        resp = requests.get("https://zenquotes.io/api/today", timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            if data and isinstance(data, list):
                return {"quote": data[0]["q"], "author": data[0]["a"], "source": "live"}
    except Exception:
        pass

    # Deterministic fallback seeded by date
    idx = (today.toordinal()) % len(MOTIVATIONAL_QUOTES)
    q = MOTIVATIONAL_QUOTES[idx]
    return {"quote": q["quote"], "author": q["author"], "source": "curated"}

# ── GitHub ────────────────────────────────────────────────
def fetch_github_profile(username: str, token: str = "") -> dict:
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        r = requests.get(f"https://api.github.com/users/{username}", headers=headers, timeout=6)
        if r.status_code == 200:
            d = r.json()
            return {
                "success": True,
                "name": d.get("name", username),
                "avatar": d.get("avatar_url", ""),
                "bio": d.get("bio", ""),
                "repos": d.get("public_repos", 0),
                "followers": d.get("followers", 0),
                "following": d.get("following", 0),
                "location": d.get("location", ""),
                "blog": d.get("blog", ""),
                "html_url": d.get("html_url", ""),
                "created_at": d.get("created_at", ""),
            }
        return {"success": False, "message": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def fetch_github_repos(username: str, token: str = "") -> list:
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        r = requests.get(
            f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10",
            headers=headers, timeout=6
        )
        if r.status_code == 200:
            return [
                {
                    "name": repo["name"],
                    "description": repo.get("description", ""),
                    "stars": repo["stargazers_count"],
                    "language": repo.get("language", "Unknown"),
                    "url": repo["html_url"],
                    "updated": repo["updated_at"][:10],
                }
                for repo in r.json()
            ]
    except Exception:
        pass
    return []

def fetch_github_contributions(username: str, token: str = "") -> dict:
    """Fetch contribution stats via GitHub GraphQL API"""
    if not token:
        return {"success": False, "message": "Token required for contribution data"}
    query = """
    {
      user(login: "%s") {
        contributionsCollection {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """ % username
    try:
        r = requests.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers={"Authorization": f"bearer {token}"},
            timeout=8
        )
        if r.status_code == 200:
            data = r.json()
            cc = data["data"]["user"]["contributionsCollection"]
            cal = cc["contributionCalendar"]
            days = []
            for week in cal["weeks"]:
                for day in week["contributionDays"]:
                    days.append({"date": day["date"], "count": day["contributionCount"]})
            return {
                "success": True,
                "total": cal["totalContributions"],
                "commits": cc["totalCommitContributions"],
                "prs": cc["totalPullRequestContributions"],
                "issues": cc["totalIssueContributions"],
                "days": days,
            }
    except Exception as e:
        return {"success": False, "message": str(e)}
    return {"success": False, "message": "Failed"}

# ── LeetCode ──────────────────────────────────────────────
def fetch_leetcode_profile(username: str) -> dict:
    """LeetCode public GraphQL API"""
    query = """
    {
      matchedUser(username: "%s") {
        username
        profile {
          realName
          reputation
          ranking
          userAvatar
          countryName
          company
          school
          skillTags
          aboutMe
        }
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
            submissions
          }
        }
        badges {
          id
          displayName
          icon
        }
      }
    }
    """ % username
    try:
        r = requests.post(
            "https://leetcode.com/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json", "Referer": "https://leetcode.com"},
            timeout=8
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("data", {}).get("matchedUser"):
                user = data["data"]["matchedUser"]
                profile = user.get("profile", {})
                stats = {}
                for item in user.get("submitStats", {}).get("acSubmissionNum", []):
                    stats[item["difficulty"]] = item["count"]
                return {
                    "success": True,
                    "username": user["username"],
                    "name": profile.get("realName", username),
                    "ranking": profile.get("ranking", "N/A"),
                    "reputation": profile.get("reputation", 0),
                    "avatar": profile.get("userAvatar", ""),
                    "country": profile.get("countryName", ""),
                    "company": profile.get("company", ""),
                    "skills": profile.get("skillTags", []),
                    "easy": stats.get("Easy", 0),
                    "medium": stats.get("Medium", 0),
                    "hard": stats.get("Hard", 0),
                    "total": stats.get("All", 0),
                    "badges": len(user.get("badges", [])),
                }
    except Exception as e:
        return {"success": False, "message": str(e)}
    return {"success": False, "message": "User not found"}

# ── Codeforces ────────────────────────────────────────────
def fetch_codeforces_profile(handle: str) -> dict:
    try:
        r = requests.get(
            f"https://codeforces.com/api/user.info?handles={handle}",
            timeout=6
        )
        if r.status_code == 200:
            data = r.json()
            if data["status"] == "OK":
                user = data["result"][0]
                return {
                    "success": True,
                    "handle": user["handle"],
                    "rating": user.get("rating", 0),
                    "max_rating": user.get("maxRating", 0),
                    "rank": user.get("rank", "unrated"),
                    "max_rank": user.get("maxRank", "unrated"),
                    "contribution": user.get("contribution", 0),
                    "friends": user.get("friendOfCount", 0),
                    "avatar": user.get("titlePhoto", ""),
                    "country": user.get("country", ""),
                    "organization": user.get("organization", ""),
                }
    except Exception as e:
        return {"success": False, "message": str(e)}
    return {"success": False, "message": "Handle not found"}

def fetch_codeforces_submissions(handle: str) -> dict:
    try:
        r = requests.get(
            f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=100",
            timeout=8
        )
        if r.status_code == 200:
            data = r.json()
            if data["status"] == "OK":
                subs = data["result"]
                accepted = [s for s in subs if s.get("verdict") == "OK"]
                problems_solved = set(
                    f"{s['problem']['contestId']}{s['problem']['index']}"
                    for s in accepted
                )
                tags = {}
                for s in accepted:
                    for tag in s["problem"].get("tags", []):
                        tags[tag] = tags.get(tag, 0) + 1
                return {
                    "success": True,
                    "total_submissions": len(subs),
                    "accepted": len(accepted),
                    "unique_solved": len(problems_solved),
                    "tags": dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]),
                }
    except Exception:
        pass
    return {"success": False, "message": "Failed to fetch submissions"}
