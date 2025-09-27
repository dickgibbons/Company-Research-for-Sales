#!/usr/bin/env python3
"""
Agent #1: SEC Filing Retriever
Input: Stock ticker symbol
Output: Latest 10-K and 10-Q filings with full text content
"""

import requests
import json
import re
from datetime import datetime
from typing import Dict, List, Optional
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SECFilingRetriever:
    """Agent #1 - Retrieves latest 10-K and 10-Q filings for a given ticker"""

    def __init__(self):
        self.base_url = "https://data.sec.gov"
        self.session = requests.Session()
        # SEC requires User-Agent header with real contact info
        self.session.headers.update({
            'User-Agent': 'EPAM Business Intelligence System 1.0 (epam-intelligence@example.com)',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'application/json, text/plain, */*'
        })
        self.rate_limit_delay = 0.1  # 10 requests per second max

    def get_cik_from_ticker(self, ticker: str) -> Optional[str]:
        """Convert ticker symbol to CIK (Central Index Key)"""
        try:
            logger.info(f"🔍 Looking up CIK for ticker: {ticker}")

            # Use search endpoint instead
            search_url = f"{self.base_url}/api/xbrl/companyfacts/CIK{self._get_known_cik(ticker)}.json"

            # For testing, use known CIKs for common tickers
            known_ciks = {
                'AAPL': '0000320193',
                'MSFT': '0000789019',
                'GOOGL': '0001652044',
                'AMZN': '0001018724',
                'TSLA': '0001318605',
                'META': '0001326801',
                'NVDA': '0001045810',
                'STT': '0000093751',  # State Street Corporation
                'JPM': '0000019617',  # JPMorgan Chase
                'BAC': '0000070858',  # Bank of America
                'WFC': '0000072971',  # Wells Fargo
                'C': '0000831001',    # Citigroup
                'GS': '0000886982',   # Goldman Sachs
                'IBM': '0000051143',  # International Business Machines
                'ORCL': '0000077476', # Oracle Corporation
                'INTC': '0000050863', # Intel Corporation
                'CSCO': '0000858877'  # Cisco Systems
            }

            if ticker.upper() in known_ciks:
                cik = known_ciks[ticker.upper()]
                logger.info(f"✅ Found CIK: {cik} for {ticker}")
                return cik

            # Try dynamic lookup using SEC company tickers API
            logger.info(f"🔎 Attempting dynamic CIK lookup for {ticker}")

            # Use the SEC's company tickers JSON file
            tickers_url = "https://www.sec.gov/files/company_tickers.json"

            response = self.session.get(tickers_url, timeout=10)
            if response.status_code == 200:
                tickers_data = response.json()

                # Search through all entries
                for entry in tickers_data.values():
                    if isinstance(entry, dict) and entry.get('ticker', '').upper() == ticker.upper():
                        cik_int = entry.get('cik_str')
                        if cik_int:
                            # Pad CIK to 10 digits with leading zeros
                            cik = f"{cik_int:010d}"
                            logger.info(f"✅ Found CIK: {cik} for {ticker} (dynamic)")
                            return cik

            # If dynamic lookup fails, try a simple search approach
            logger.warning(f"⚠️ Dynamic lookup failed, trying search approach for {ticker}")

            # Alternative: try searching by company name if ticker is long enough to be a name
            if len(ticker) > 4:
                return self.search_company_by_name(ticker)

            logger.warning(f"❌ Could not find CIK for {ticker}")
            return None

        except Exception as e:
            logger.error(f"Error looking up CIK for {ticker}: {e}")
            return None

    def search_company_by_name(self, company_name: str) -> Optional[str]:
        """Search for company by name using SEC tickers data"""
        try:
            logger.info(f"🔍 Searching by company name: {company_name}")

            tickers_url = "https://www.sec.gov/files/company_tickers.json"
            response = self.session.get(tickers_url, timeout=10)

            if response.status_code == 200:
                tickers_data = response.json()

                search_terms = company_name.upper().split()

                for entry in tickers_data.values():
                    if isinstance(entry, dict):
                        company_title = entry.get('title', '').upper()

                        # Check if all search terms are in company title
                        if all(term in company_title for term in search_terms):
                            cik_int = entry.get('cik_str')
                            if cik_int:
                                cik = f"{cik_int:010d}"
                                ticker = entry.get('ticker', '')
                                logger.info(f"✅ Found CIK: {cik} for '{company_name}' (ticker: {ticker})")
                                return cik

            return None

        except Exception as e:
            logger.error(f"Error searching company by name: {e}")
            return None

    def _get_known_cik(self, ticker: str) -> str:
        """Get CIK for known tickers"""
        known_ciks = {
            'AAPL': '0000320193',
            'MSFT': '0000789019',
            'GOOGL': '0001652044',
            'AMZN': '0001018724',
            'TSLA': '0001318605',
            'META': '0001326801',
            'NVDA': '0001045810'
        }
        return known_ciks.get(ticker.upper(), '0000320193')

    def get_company_filings(self, cik: str) -> Optional[Dict]:
        """Get all filings for a company by CIK"""
        try:
            logger.info(f"📋 Fetching filings for CIK: {cik}")

            url = f"{self.base_url}/submissions/CIK{cik}.json"
            time.sleep(self.rate_limit_delay)

            response = self.session.get(url)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            logger.error(f"Error getting filings for CIK {cik}: {e}")
            return None

    def find_latest_filings(self, filings_data: Dict, form_types: List[str]) -> List[Dict]:
        """Find the latest 10-K and 10-Q filings"""
        try:
            recent_filings = filings_data.get('filings', {}).get('recent', {})

            if not recent_filings:
                logger.warning("No recent filings found")
                return []

            form_list = recent_filings.get('form', [])
            accession_list = recent_filings.get('accessionNumber', [])
            filing_date_list = recent_filings.get('filingDate', [])
            report_date_list = recent_filings.get('reportDate', [])

            found_filings = []
            found_types = set()

            # Look for the most recent 10-K and 10-Q
            for i, form_type in enumerate(form_list):
                if form_type in form_types and form_type not in found_types:
                    filing_info = {
                        'form_type': form_type,
                        'accession_number': accession_list[i],
                        'filing_date': filing_date_list[i],
                        'report_date': report_date_list[i],
                        'cik': filings_data.get('cik')
                    }
                    found_filings.append(filing_info)
                    found_types.add(form_type)
                    logger.info(f"✅ Found {form_type} filed on {filing_date_list[i]}")

                    # Stop when we have both 10-K and 10-Q
                    if len(found_types) == len(form_types):
                        break

            return found_filings

        except Exception as e:
            logger.error(f"Error finding latest filings: {e}")
            return []

    def get_filing_content(self, filing_info: Dict) -> Optional[str]:
        """Download the full text content of a filing"""
        try:
            cik = str(filing_info['cik']).zfill(10)
            accession = filing_info['accession_number'].replace('-', '')

            logger.info(f"📄 Downloading {filing_info['form_type']} content...")

            # Try multiple URL formats
            urls_to_try = [
                f"{self.base_url}/Archives/edgar/data/{int(cik)}/{accession}/{filing_info['accession_number']}.txt",
                f"{self.base_url}/Archives/edgar/data/{int(cik)}/{accession}/{filing_info['accession_number']}-index.html",
                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{filing_info['accession_number']}.txt"
            ]

            for url in urls_to_try:
                try:
                    time.sleep(self.rate_limit_delay)
                    logger.info(f"Trying URL: {url}")
                    response = self.session.get(url)

                    if response.status_code == 200:
                        content = response.text
                        logger.info(f"✅ Downloaded {filing_info['form_type']} ({len(content)} characters)")
                        return content

                except Exception as url_error:
                    logger.warning(f"URL failed: {url} - {url_error}")
                    continue

            # If all URLs fail, return filing metadata as a fallback
            logger.warning(f"Could not download content, returning metadata for {filing_info['form_type']}")
            return f"FILING METADATA:\nForm Type: {filing_info['form_type']}\nFiling Date: {filing_info['filing_date']}\nAccession Number: {filing_info['accession_number']}\n\nContent could not be downloaded but filing exists."

        except Exception as e:
            logger.error(f"Error downloading filing content: {e}")
            return None

    def extract_filing_text(self, raw_content: str) -> str:
        """Extract readable text from raw SEC filing"""
        try:
            # Remove HTML tags
            clean_text = re.sub(r'<[^>]+>', '', raw_content)

            # Remove excessive whitespace
            clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
            clean_text = re.sub(r' +', ' ', clean_text)

            return clean_text.strip()

        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return raw_content

    def process_ticker(self, ticker: str) -> Dict:
        """
        Main method: Process a ticker and return latest 10-K and 10-Q filings
        """
        logger.info(f"🚀 Agent #1 Processing ticker: {ticker}")

        result = {
            'agent': 'SEC Filing Retriever',
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'filings': {},
            'error': None
        }

        try:
            # Step 1: Get CIK from ticker
            cik = self.get_cik_from_ticker(ticker)
            if not cik:
                result['status'] = 'error'
                result['error'] = f'Ticker {ticker} not found'
                return result

            # Step 2: Get company filings
            filings_data = self.get_company_filings(cik)
            if not filings_data:
                result['status'] = 'error'
                result['error'] = 'Unable to retrieve filings data'
                return result

            # Step 3: Find latest 10-K and 10-Q
            latest_filings = self.find_latest_filings(filings_data, ['10-K', '10-Q'])

            if not latest_filings:
                result['status'] = 'warning'
                result['error'] = 'No 10-K or 10-Q filings found'
                return result

            # Step 4: Download filing content
            for filing in latest_filings:
                form_type = filing['form_type']

                # Get full content
                raw_content = self.get_filing_content(filing)
                if raw_content:
                    clean_content = self.extract_filing_text(raw_content)

                    result['filings'][form_type] = {
                        'form_type': form_type,
                        'filing_date': filing['filing_date'],
                        'report_date': filing['report_date'],
                        'accession_number': filing['accession_number'],
                        'content_length': len(clean_content),
                        'content': clean_content[:5000] + '...' if len(clean_content) > 5000 else clean_content,
                        'full_content': clean_content  # Store full content
                    }

                    logger.info(f"✅ Processed {form_type} - {len(clean_content)} characters")

            logger.info(f"🎉 Agent #1 completed successfully for {ticker}")

        except Exception as e:
            logger.error(f"Error processing ticker {ticker}: {e}")
            result['status'] = 'error'
            result['error'] = str(e)

        return result


def main():
    """Test the agent with a sample ticker"""
    import sys
    agent = SECFilingRetriever()

    # Get ticker from command line or use default
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

    print("🤖 Testing Agent #1: SEC Filing Retriever")
    print("=" * 50)

    result = agent.process_ticker(ticker)

    # Print summary
    print(f"\n📊 Results for {result['ticker']}:")
    print(f"Status: {result['status']}")

    if result['status'] == 'success':
        for form_type, filing in result['filings'].items():
            print(f"\n📋 {form_type} Filing:")
            print(f"  Filing Date: {filing['filing_date']}")
            print(f"  Report Date: {filing['report_date']}")
            print(f"  Content Length: {filing['content_length']:,} characters")
            print(f"  Preview: {filing['content'][:200]}...")
    else:
        print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()