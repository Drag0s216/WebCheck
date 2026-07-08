import hashlib, time, re, sys, requests
from datetime import datetime


def normalize(content: str) -> str:
    return re.sub(r'[0-9a-f]{10,}', 'X', content)

PUSHBULLET_API_KEY = ""

def send_pushbullet(title: str, body: str):
    try:
        requests.post(
            "https://api.pushbullet.com/v2/pushes",
            headers={"Access-Token": PUSHBULLET_API_KEY},
            json={"type": "note", "title": title, "body": body},
            timeout=10
        )


    except requests.RequestException as e:
        print(f"  [Pushbullet error] {e}")



def is_login_page(content: str) -> bool:
    return "loginform" in content or "login/index.php" in content


def fetch_page(url: str) -> str | None:
    try:
        headers = headers = {
    "User-Agent": "Mozilla/5.0 (compatible; ChangeMonitor/1.0)",
    "Cookie": ""
}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"  [ERROR] Could not fetch page: {e}")
        return None


def get_hash(content: str) -> str:
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def monitor(url: str, interval: int = 60, show_diff_output: bool = True):
    print(f"\n\n\x1b[92m WebCheck Monitor\n\x1b[93m ")
    print(f"  URL      : {url}")
    print(f"  Interval : every {interval} second(s)")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("  Fetching initial snapshot...")
    initial_content = fetch_page(url)
    if initial_content is None:
        print("  Could not load the page. Check the URL and try again.")
        sys.exit(1)

    last_content = initial_content
    last_hash = get_hash(normalize(initial_content))
    print(f"  Snapshot taken. Hash: {last_hash[:8]}...\n")

    check_count = 0

    while True:
        time.sleep(interval)
        check_count += 1
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Check #{check_count} ... ", end="", flush=True)

        content = fetch_page(url)
        if content is None:
            print("skipped (fetch failed).")
            continue

        current_hash = get_hash(normalize(content))

        if current_hash != last_hash:
            if is_login_page(content):
                print("\x1b[91m ⚠️  Session expired! Log in again and update your cookie.")
                send_pushbullet("⚠️ Session Expired", f"Your session on {url} has expired. Log in again and update your cookie.")
                raise SystemExit
            else:
                print("\x1b[92m ✅ CHANGE DETECTED!")
                send_pushbullet("✅ Page Changed!", f"A change was detected on {url}")
                if show_diff_output:
                    show_diff(last_content, content)
                last_content = content
                last_hash = current_hash
                raise SystemExit


if __name__ == "__main__":
    DEFAULT_URL = ""
    CHECK_INTERVAL = 120
    SHOW_DIFF = False

    target_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    try:
        monitor(target_url, interval=CHECK_INTERVAL, show_diff_output=SHOW_DIFF)
    except KeyboardInterrupt:
        print("\n\n\x1b[91m   Monitoring stopped.\x1b[97m")