import requests
import os
from pathlib import Path


def download_latest_sec_10k(cik: str, company: str, save_dir: str = "data/sec"):
    """Download the latest available 10-K filing for a given CIK from SEC EDGAR."""
    os.makedirs(save_dir, exist_ok=True)
    headers = {"User-Agent": "Chankey Pathak (chankey007@gmail.com)"}
    cik_padded = cik.zfill(10)
    json_url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    resp = requests.get(json_url, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to fetch SEC JSON for {company} ({cik})")
        return None
    data = resp.json()
    filings = data.get("filings", {}).get("recent", {})
    forms = filings.get("form", [])
    accessions = filings.get("accessionNumber", [])
    filing_dates = filings.get("filingDate", [])
    primary_docs = filings.get("primaryDocument", [])
    descriptions = filings.get("primaryDocDescription", [""] * len(forms))
    # Find the latest 10-K
    for i, (form, acc, date, doc, desc) in enumerate(
        zip(forms, accessions, filing_dates, primary_docs, descriptions)
    ):
        if form == "10-K":
            # Print if this filing mentions litigation risk in its description
            if "litigation" in desc.lower() or "legal" in desc.lower() or "risk" in desc.lower():
                print(f"[TestCase] {company} {date} {desc}")
            acc_nodash = acc.replace("-", "")
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_nodash}/{doc}"
            doc_resp = requests.get(doc_url, headers=headers)
            if doc_resp.status_code == 200:
                out_path = Path(save_dir) / f"{company.lower()}_10k_{date[:4]}.htm"
                out_path.write_text(doc_resp.text)
                print(f"Downloaded {company} 10-K for {date[:4]} to {out_path}")
                return str(out_path)
            else:
                print(f"Failed to download: {doc_url}")
            break
    print(f"No 10-K found for {company}")
    return None


if __name__ == "__main__":
    filings = [
        # (CIK, Company)
        ("0000320193", "Apple"),
        ("0000789019", "Microsoft"),
        ("0001652044", "Alphabet"),
        ("0000051143", "IBM"),
        ("0001018724", "Amazon"),
        ("0000320187", "CocaCola"),
        ("0000200406", "ProcterGamble"),
        ("0000078003", "ExxonMobil"),
        ("0000021344", "Ford"),
        ("0001090872", "Tesla"),
        ("0001067983", "Meta"),
        ("0000789019", "Nvidia"),
        ("0000909832", "PepsiCo"),
        ("0000078003", "Chevron"),
        ("0000310158", "JohnsonJohnson"),
    ]
    for cik, company in filings:
        download_latest_sec_10k(cik, company)
