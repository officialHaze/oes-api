from rest_framework.response import Response
from rest_framework.decorators import api_view
from collections import deque
from bs4 import BeautifulSoup
from urllib3.exceptions import LocationParseError
import re
import urllib.parse
import requests
import requests.exceptions


@api_view(["POST"])
def scrap_email(req, *args, **kwargs):
    url = req.data.get("url")
    scan_type = req.data.get("scan_type")
    if not url.startswith("http"):
        return Response(
            {
                "detail": "You have to specify what protocol the address follows, http or https? Example:https://example.com"
            },
            status=400,
        )
    urls = deque([url])

    scrapped_urls = []
    emails = []

    count = 0
    if scan_type == "keep it chill":
        max_count = 50
    elif scan_type == "amp it up":
        max_count = 100
    elif scan_type == "do a full deep scan":
        max_count = 200
    try:
        while True:
            count += 1
            if count == max_count or len(urls) == 0:
                break
            url_to_scan = urls.popleft()
            scrapped_urls.append(url_to_scan)

            # split the url
            parts = urllib.parse.urlsplit(url_to_scan)
            base_url = "{scheme}://{netloc}".format(
                scheme=parts.scheme, netloc=parts.netloc
            )

            path = (
                url_to_scan[: url_to_scan.rfind("/") + 1]
                if "/" in parts.path
                else url_to_scan
            )

            print(f"processing ----> {url_to_scan}")

            try:
                response = requests.get(url_to_scan)
            except (
                requests.exceptions.MissingSchema,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                LocationParseError,
            ):
                print(f"processing failed ----> {url_to_scan}")
                continue

            # search the entire response string with regex validator for valid email addresses and save them
            found_emails = re.findall(
                r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I
            )
            for mail in found_emails:
                emails.append(mail)

            soup = BeautifulSoup(response.text, features="html.parser")

            for anchor in soup.find_all("a"):
                link = anchor.attrs["href"] if "href" in anchor.attrs else ""
                if link.startswith("/"):
                    link = base_url + link
                elif not link.startswith("http"):
                    link = path + link
                if link not in urls and link not in scrapped_urls:
                    urls.append(link)
    except:
        return Response({"status": "error occured!"}, status=500)

    return Response({"emails": emails}, status=200)
