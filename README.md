#WebCheck

A small monitoring script that watches a university portal page and sends a push notification the moment grades are posted, instead of manually refreshing the page every hour during exam season.


How It Works

Fetches a target page on the university's virtual campus (using a saved session cookie, since the page requires login).
Takes a hash of the page content and compares it on every check to detect changes.
Normalizes the content before hashing (stripping out long hex-like strings, e.g. session tokens or dynamic IDs) so the script doesn't get false positives from content that changes on every load but isn't actually a real update.
If a change is detected, it sends a push notification via the Pushbullet API.
If the page content matches a login form instead of the expected page, it recognizes the session has expired and notifies me to log in again and refresh the cookie - instead of silently failing or spamming false "change detected" alerts.


Tech Stack


Python 3, (requests, hashlib, time, re, sys)
Pushbullet API for push notifications


Why This Exists

Grades on the university portal get posted with no notification system of its own. Checking manually meant refreshing the page over and over during exam season. This runs in the background and only pings me when something actually changes.


Known Limitations

Relies on a manually copied session cookie, which expires periodically - the script detects this (login-page match) and notifies me to refresh it, but doesn't refresh it automatically. This may also not work on most sites since the cookies are no longer shown as a security measure.

Relies on a manually copied session cookie, which expires periodically - the script detects this (login-page match) and notifies me to refresh it, but doesn't refresh it automatically. This may also not work on most sites since the cookies are no longer shown as a security measure.
