import requests
import json
import time

# Token mungkin sudah expired
BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpjWWtab1BUMF95dTQyYkRhSHVGRyJ9.eyJodHRwOi8vc2Vlay9jbGFpbXMvbWZhX2Vucm9sbGVkIjpmYWxzZSwiaHR0cDovL3NlZWsvY2xhaW1zL2lkZW50aXR5X2lkIjoiYXV0aDB8NmEyYTA2NDQyMGVhNTk4YzIzNGZmM2ZiIiwiaHR0cDovL3NlZWsvY2xhaW1zL3Byb2R1Y3RzIjpbInNlZWsiXSwiaHR0cDovL3NlZWsvY2xhaW1zL2NvdW50cnkiOiJJRCIsImh0dHA6Ly9zZWVrL2NsYWltcy9icmFuZCI6ImpvYnN0cmVldCIsImh0dHA6Ly9zZWVrL2NsYWltcy9leHBlcmllbmNlIjoiY2FuZGlkYXRlIiwiaHR0cDovL3NlZWsvY2xhaW1zL3VzZXJfaWQiOiI1OTczOTIzMjUiLCJpc3MiOiJodHRwczovL2xvZ2luLnNlZWsuY29tLyIsInN1YiI6ImF1dGgwfDZhMmEwNjQ0MjBlYTU5OGMyMzRmZjNmYiIsImF1ZCI6WyJodHRwczovL3NlZWsvYXBpL2NhbmRpZGF0ZSIsImh0dHBzOi8vc2Vla2Fuei5vbmxpbmVhdXRoLnByb2Qub3V0ZnJhLnh5ei91c2VyaW5mbyJdLCJpYXQiOjE3ODExNDMwNTcsImV4cCI6MTc4MTE0NjY1Nywic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBvZmZsaW5lX2FjY2VzcyIsImF6cCI6IjhPVmhwdnRhSTluNVFWRVFLM1g1eWZzbUNicnJMWGZFIn0.CNL9RvPAUiOxvL0Fjg521HOnoR_WP5t3hdOV3vB_mf1iu8NIs2yAXH6FQOLd7_NichQ7jucBzEU1IChx1sJ8s1Obw9l7gcRRWIN-KSWet8BHMKG2OnzLhEaqiJ5ZjoMKU3jmnEJGKyHxWi7wd1H1rmivDv7ES0sCodGYYlwWAMGLoRzPLmm28NDnaGAOwRE09tacubu-9ic-_Fm8GDgsUyGhUNz-JINuvmCu2RVsMsRagqF5e2bHgM2xyLFU7PkCxS9p0ZPwrH_IgGNDVy1lCfK6FJ2pp6RRghlFPTA6F5HPnnTHeERoKtE_VHAJBFm0MNWSXE1BywIlPQKK_IyxNg"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Origin": "https://id.jobstreet.com",
    "Referer": "https://id.jobstreet.com/id/IT-jobs/in-Indonesia",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "seek-request-brand": "jobstreet",
    "seek-request-country": "ID",
    "x-seek-site": "chalice",
    "x-custom-features": "application/features.seek.all+json",
}

GRAPHQL_QUERY = """
query JobSearchV6($params: JobSearchV6QueryInput!) {
  jobSearchV6(params: $params) {
    data {
      advertiser { id description __typename }
      bulletPoints
      classifications {
        classification { id description __typename }
        subclassification { id description __typename }
        __typename
      }
      companyName
      currencyLabel
      displayType
      id
      isFeatured
      listingDate { dateTimeUtc __typename }
      locations {
        countryCode
        label
        seoHierarchy { contextualName __typename }
        __typename
      }
      salaryLabel
      teaser
      title
      workArrangements { displayText __typename }
      workTypes
      __typename
    }
    totalCount
    __typename
  }
}
"""

KEYWORDS = [
    "Software Engineer",
    "Data Analyst",
    "Web Developer",
    "Backend Developer",
    "Frontend Developer",
    "Network Engineer",
    "IT Support",
    "Cybersecurity",
    "DevOps",
    "Machine Learning",
    "Data Engineer",
    "Mobile Developer",
    "Database Administrator",
    "System Analyst",
    "Cloud Engineer",
]
LOCATION = "Indonesia"
MAX_PAGES_PER_KEYWORD = 4


def scrape_keyword(keyword, location, max_pages):
    jobs = []
    url = "https://id.jobstreet.com/graphql"

    for page in range(1, max_pages + 1):
        payload = {
            "operationName": "JobSearchV6",
            "query": GRAPHQL_QUERY,
            "variables": {
                "params": {
                    "channel": "web",
                    "keywords": keyword,
                    "where": location,
                    "page": page,
                    "pageSize": 30,
                    "siteKey": "ID",
                    "locale": "id-ID",
                    "source": "FE_SERP",
                }
            }
        }

        try:
            r = requests.post(url, headers=HEADERS, json=payload, timeout=15)

            if r.status_code == 401:
                print("  [!] Token expired! Update BEARER_TOKEN dulu.")
                return jobs, True

            if r.status_code != 200:
                print(f"  [!] Error {r.status_code}: {r.text[:200]}")
                break

            resp = r.json()

            if "errors" in resp:
                print(f"  [!] GraphQL error: {resp['errors'][0]['message']}")
                break

            page_jobs = resp.get("data", {}).get("jobSearchV6", {}).get("data", [])
            total     = resp.get("data", {}).get("jobSearchV6", {}).get("totalCount", 0)

            if not page_jobs:
                break

            jobs.extend(page_jobs)
            print(f"    Page {page}: +{len(page_jobs)} | subtotal: {len(jobs)} / {total}")

            if len(jobs) >= total:
                break

            time.sleep(1.2)

        except Exception as e:
            print(f"  [!] Exception: {e}")
            break

    return jobs, False


# main
all_jobs = []
seen_ids = set()
stop = False

for kw in KEYWORDS:
    if stop:
        break
    print(f"\n[*] Keyword: '{kw}'")
    kw_jobs, stop = scrape_keyword(kw, LOCATION, MAX_PAGES_PER_KEYWORD)

    before = len(all_jobs)
    for j in kw_jobs:
        if j["id"] not in seen_ids:
            seen_ids.add(j["id"])
            all_jobs.append(j)

    added = len(all_jobs) - before
    print(f"  => +{added} unique (dibuang duplikat: {len(kw_jobs) - added})")
    time.sleep(2)

print(f"\n{'='*50}")
print(f"[+] TOTAL UNIQUE JOBS: {len(all_jobs)}")

if all_jobs:
    with open("jobstreet_jobs_final.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)
    print("[+] Disimpan ke: jobstreet_jobs_final.json")
    print("\n[Preview] 3 jobs pertama:")
    for j in all_jobs[:3]:
        loc = j.get('locations', [{}])[0].get('label', 'N/A')
        print(f"  - {j.get('title')} @ {j.get('companyName')} | {loc} | {j.get('salaryLabel', 'N/A')}")
else:
    print("[-] Tidak ada data.")


