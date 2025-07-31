import requests
import os
from pathlib import Path


def download_sec_10k(cik: str, accession: str, company: str, year: int, save_dir: str = "data/sec"):
    """Download the 10-K filing for a given CIK and accession number from SEC EDGAR. If the accession fails, try to fetch the latest 10-K for that CIK/year."""
    os.makedirs(save_dir, exist_ok=True)
    base_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/"
    filing_url = f"{base_url}{accession.replace('-', '')}/{accession}-index.html"
    resp = requests.get(filing_url, headers={"User-Agent": "genai-risk-analyst-demo"})
    if resp.status_code == 200:
        out_path = Path(save_dir) / f"{company.lower()}_10k_{year}.html"
        out_path.write_text(resp.text)
        print(f"Downloaded {company} 10-K for {year} to {out_path}")
        return str(out_path)
    else:
        print(f"Failed to download: {filing_url}")
        # Try to find the latest 10-K accession for this CIK/year
        search_url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
        try:
            sresp = requests.get(search_url, headers={"User-Agent": "genai-risk-analyst-demo"})
            if sresp.status_code == 200:
                data = sresp.json()
                filings = data.get("filings", {}).get("recent", {})
                forms = filings.get("form", [])
                accessions = filings.get("accessionNumber", [])
                filing_dates = filings.get("filingDate", [])
                for form, acc, fdate in zip(forms, accessions, filing_dates):
                    if form == "10-K" and fdate.startswith(str(year)):
                        fallback_acc = acc
                        fallback_url = f"{base_url}{fallback_acc.replace('-', '')}/{fallback_acc}-index.html"
                        fresp = requests.get(fallback_url, headers={"User-Agent": "genai-risk-analyst-demo"})
                        if fresp.status_code == 200:
                            out_path = Path(save_dir) / f"{company.lower()}_10k_{year}.html"
                            out_path.write_text(fresp.text)
                            print(f"[Fallback] Downloaded {company} 10-K for {year} to {out_path}")
                            return str(out_path)
                        else:
                            print(f"[Fallback] Failed to download: {fallback_url}")
                        break
            else:
                print(f"[Fallback] Failed to fetch SEC JSON for {cik}")
        except Exception as e:
            print(f"[Fallback] Exception: {e}")
        return None

if __name__ == "__main__":
    filings = [
        # (CIK, Accession, Company, Year)
        ("0000320193", "0000320193-23-000106", "Apple", 2023),
        ("0000789019", "0000789019-23-000036", "Microsoft", 2023),
        ("0001652044", "0001652044-24-000019", "Alphabet", 2023),
        ("0000051143", "0000051143-24-000007", "IBM", 2023),
        ("0001018724", "0001018724-24-000004", "Amazon", 2023),
        ("0000320187", "0000320187-24-000009", "CocaCola", 2023),
        ("0000200406", "0000200406-24-000022", "ProcterGamble", 2023),
        ("0000078003", "0000078003-24-000009", "ExxonMobil", 2023),
        ("0000021344", "0000021344-24-000015", "Ford", 2023),
        ("0001090872", "0001090872-24-000012", "Tesla", 2023),
    ]
    for cik, accession, company, year in filings:
        download_sec_10k(cik, accession, company, year)
