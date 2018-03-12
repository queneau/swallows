import urllib.request
from bs4 import BeautifulSoup
import datetime
import slackweb
import os

html = urllib.request.urlopen("https://www.yakult-swallows.co.jp/")
soup = BeautifulSoup(html, "html.parser")
div = soup.find_all("div", class_ = "list list-arrows list-entry")[0]
urls = div.find_all("a", class_ = "item item-avatar")

root = "https://www.yakult-swallows.co.jp"
today = datetime.date.today()

message = ""

for url in urls:
    tstr = url.find("time").get("datetime")[:-6]
    yourdate = datetime.datetime.strptime(tstr, "%Y-%m-%dT%H:%M:%S").date()
    if today == yourdate:
        message += url.find("h2").string + "\n"
        message += root + url.get("href") + "\n\n"

slack = slackweb.Slack(url=os.getenv("SLACK_URL", ""))
slack.notify(text=message)
