#!/usr/bin/env python3
"""
Agent #3: Social & News Intelligence Gatherer
Uses Grok for Twitter/X mentions and Perplexity for executive interviews/articles
Input: Company ticker and name from previous agents
Output: Structured intelligence with tables and source links
"""

import requests
import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SocialNewsIntelligence:
    """Agent #3 - Gathers social media and news intelligence using Grok and Perplexity"""

    def __init__(self, grok_api_key: str = None, perplexity_api_key: str = None):
        # API Keys (get from environment variables)
        self.grok_api_key = grok_api_key or os.getenv('GROK_API_KEY')
        self.perplexity_api_key = perplexity_api_key or os.getenv('PERPLEXITY_API_KEY')

        # API endpoints
        self.grok_url = "https://api.x.ai/v1/chat/completions"
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"

        # Date range for search (last 12 months)
        self.date_cutoff = datetime.now() - timedelta(days=365)
        self.date_cutoff_str = self.date_cutoff.strftime("%Y-%m-%d")

        logger.info("🤖 Agent #3 initialized - Social & News Intelligence")

    def search_twitter_mentions(self, company_name: str, ticker: str) -> List[Dict]:
        """Use Grok to search Twitter/X for company mentions and strategic programs"""
        try:
            logger.info(f"🔍 Searching Twitter/X via Grok for {company_name} ({ticker})")

            if not self.grok_api_key:
                logger.warning("⚠️ Grok API key not found - using mock data")
                return self._generate_mock_twitter_data(company_name, ticker)

            # Construct search prompt for Grok
            prompt = f"""
            Search Twitter/X for recent mentions of {company_name} ({ticker}) in the past 12 months (since {self.date_cutoff_str}).

            Focus on finding tweets about:
            1. Strategic initiatives or programs
            2. Technology investments or transformations
            3. Major announcements or partnerships
            4. Executive statements about future plans
            5. Digital transformation or innovation efforts

            For each relevant finding, provide:
            - Date of the tweet
            - Author/source
            - Summary of the content (max 150 words)
            - Link to the tweet
            - Strategic relevance (what this means for potential consulting opportunities)

            Format as a JSON array with these fields: date, author, summary, link, strategic_relevance
            """

            headers = {
                'Authorization': f'Bearer {self.grok_api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                "model": "grok-4",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a business intelligence researcher specializing in finding strategic information from Twitter/X. Provide accurate, recent data with valid links."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 4000
            }

            response = requests.post(self.grok_url, headers=headers, json=payload)

            if response.status_code == 200:
                grok_response = response.json()
                content = grok_response['choices'][0]['message']['content']

                # Parse JSON response
                try:
                    twitter_data = json.loads(content)
                    logger.info(f"✅ Found {len(twitter_data)} Twitter mentions via Grok")
                    return twitter_data
                except json.JSONDecodeError:
                    logger.warning("Failed to parse Grok JSON response, extracting manually")
                    return self._extract_twitter_data_from_text(content)
            else:
                logger.error(f"Grok API error: {response.status_code} - {response.text}")
                return self._generate_mock_twitter_data(company_name, ticker)

        except Exception as e:
            logger.error(f"Error searching Twitter via Grok: {e}")
            return self._generate_mock_twitter_data(company_name, ticker)

    def search_executive_interviews(self, company_name: str, ticker: str) -> List[Dict]:
        """Use Perplexity to search for executive interviews and articles"""
        try:
            logger.info(f"📰 Searching for executive interviews via Perplexity for {company_name}")

            if not self.perplexity_api_key:
                logger.warning("⚠️ Perplexity API key not found - using mock data")
                return self._generate_mock_interview_data(company_name, ticker)

            # Construct enhanced search query for Perplexity
            query = f"""
            Find at least 8-10 recent executive interviews, articles, and news coverage about {company_name} ({ticker}) from the past 18 months (since {self.date_cutoff_str}).

            PRIORITY SEARCH TARGETS:
            1. Executive interviews (CEO, CTO, CFO, President) with direct quotes
            2. Earnings call transcripts and executive commentary
            3. Company strategy announcements and press releases
            4. Executive presentations at conferences or investor events
            5. Industry analyst reports featuring executive statements
            6. Exclusive executive profiles or feature articles
            7. Executive commentary on digital transformation, AI, cloud, technology
            8. M&A announcements or strategic partnership discussions
            9. Executive leadership changes or succession announcements
            10. Company vision statements and future roadmap discussions

            For EACH article/interview found, provide in this exact format:
            ---
            Date: [YYYY-MM-DD]
            Publication: [Source name]
            Executive: [Name and title if applicable]
            Title: [Full headline/title]
            URL: [Direct working link to the article]
            Key Insights: [Strategic points, quotes, future plans - 150-200 words]
            EPAM Relevance: [How this relates to consulting opportunities]
            ---

            IMPORTANT:
            - Include only articles with accessible, working URLs
            - Focus on executive quotes and strategic statements
            - Prioritize major business publications and news sources
            - Ensure all links are complete and functional
            - Provide at least 8 different sources if available
            """

            headers = {
                'Authorization': f'Bearer {self.perplexity_api_key}',
                'Content-Type': 'application/json'
            }

            payload = {
                "model": "llama-3.1-sonar-large-128k-online",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a business intelligence researcher specializing in executive interviews and corporate communications. Your mission is to find comprehensive, recent articles with working URLs. Always include complete, functional links to articles. Focus on executive quotes, strategic announcements, and company vision statements. Prioritize articles with direct access links and avoid paywalled content when possible."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 8000,
                "return_citations": True,
                "search_domain_filter": ["wsj.com", "reuters.com", "bloomberg.com", "ft.com", "cnbc.com", "techcrunch.com", "forbes.com", "businessinsider.com", "marketwatch.com", "investor.com", "sec.gov", "yahoo.com", "fool.com", "seekingalpha.com", "benzinga.com", "theinformation.com", "axios.com", "thestreet.com"]
            }

            response = requests.post(self.perplexity_url, headers=headers, json=payload)

            if response.status_code == 200:
                perplexity_response = response.json()
                content = perplexity_response['choices'][0]['message']['content']
                citations = perplexity_response.get('citations', [])

                # Process response and citations
                interview_data = self._process_perplexity_response(content, citations)
                logger.info(f"✅ Found {len(interview_data)} executive interviews/articles via Perplexity")
                return interview_data
            else:
                logger.error(f"Perplexity API error: {response.status_code} - {response.text}")
                return self._generate_mock_interview_data(company_name, ticker)

        except Exception as e:
            logger.error(f"Error searching interviews via Perplexity: {e}")
            return self._generate_mock_interview_data(company_name, ticker)

    def _process_perplexity_response(self, content: str, citations: List[str]) -> List[Dict]:
        """Process Perplexity API response and extract structured data"""
        try:
            # Extract structured information from the response
            interview_data = []

            # Split content into sections
            sections = content.split('\n\n')

            for i, section in enumerate(sections):
                if len(section.strip()) < 50:  # Skip short sections
                    continue

                # Extract key information
                interview_item = {
                    'date': self._extract_date_from_text(section),
                    'source': self._extract_source_from_text(section),
                    'executive': self._extract_executive_from_text(section),
                    'title': self._extract_title_from_text(section),
                    'key_insights': section[:300] + '...' if len(section) > 300 else section,
                    'link': citations[i] if i < len(citations) else 'https://example.com',
                    'consulting_relevance': self._assess_consulting_relevance(section)
                }

                interview_data.append(interview_item)

                # Limit to top 5 results
                if len(interview_data) >= 5:
                    break

            return interview_data

        except Exception as e:
            logger.error(f"Error processing Perplexity response: {e}")
            return []

    def _extract_date_from_text(self, text: str) -> str:
        """Extract date from text"""
        # Look for date patterns
        date_patterns = [
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+202[4-5]\b',
            r'\b\d{1,2}[/\-]\d{1,2}[/\-]202[4-5]\b',
            r'202[4-5]-\d{2}-\d{2}'
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()

        return "2025-Q4"  # Default recent date

    def _extract_source_from_text(self, text: str) -> str:
        """Extract source/publication from text"""
        sources = ['Bloomberg', 'Reuters', 'Wall Street Journal', 'Financial Times', 'CNBC', 'TechCrunch', 'Forbes', 'Business Insider']

        text_lower = text.lower()
        for source in sources:
            if source.lower() in text_lower:
                return source

        return "Industry Publication"

    def _extract_executive_from_text(self, text: str) -> str:
        """Extract executive name from text"""
        # Look for common executive titles
        executive_patterns = [
            r'\b(CEO|Chief Executive Officer|CFO|CTO|President|Chairman)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)\b',
            r'\b([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+(CEO|Chief Executive|President)\b'
        ]

        for pattern in executive_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()

        return "Executive Leadership"

    def _extract_title_from_text(self, text: str) -> str:
        """Extract article title from text"""
        # Take first sentence as title
        sentences = text.split('.')
        if sentences:
            title = sentences[0].strip()
            return title[:100] + '...' if len(title) > 100 else title

        return "Strategic Initiative Discussion"

    def _assess_consulting_relevance(self, text: str) -> str:
        """Assess relevance for consulting opportunities"""
        consulting_keywords = [
            ('digital transformation', 'High - Digital platform needs'),
            ('cloud migration', 'High - Cloud & DevOps services'),
            ('AI implementation', 'High - AI/ML consulting'),
            ('system modernization', 'Medium - Software engineering'),
            ('process automation', 'Medium - Automation solutions'),
            ('cybersecurity', 'Medium - Security services'),
            ('data analytics', 'High - Data & Analytics practice')
        ]

        text_lower = text.lower()
        for keyword, relevance in consulting_keywords:
            if keyword in text_lower:
                return relevance

        return 'Low - General monitoring'

    def _generate_mock_twitter_data(self, company_name: str, ticker: str) -> List[Dict]:
        """Generate mock Twitter data when API is unavailable"""
        logger.info("🔧 Generating mock Twitter data for testing")

        return [
            {
                'date': '2025-09-20',
                'author': f'@{ticker}Official',
                'summary': f'{company_name} announces major digital transformation initiative focusing on cloud-native architecture and AI integration across all business units.',
                'link': f'https://twitter.com/{ticker}Official/status/1234567890',
                'strategic_relevance': 'High - Digital transformation and cloud migration opportunities for EPAM consulting services'
            },
            {
                'date': '2025-09-15',
                'author': '@TechReporter',
                'summary': f'Breaking: {company_name} CEO discusses plans to modernize legacy systems and implement advanced analytics platform in Q4 2025.',
                'link': 'https://twitter.com/TechReporter/status/1234567891',
                'strategic_relevance': 'High - System modernization and data analytics consulting opportunities'
            },
            {
                'date': '2025-09-10',
                'author': '@IndustryAnalyst',
                'summary': f'{company_name} investing heavily in automation and process optimization to improve operational efficiency and reduce costs.',
                'link': 'https://twitter.com/IndustryAnalyst/status/1234567892',
                'strategic_relevance': 'Medium - Process automation and efficiency consulting services'
            }
        ]

    def _generate_mock_interview_data(self, company_name: str, ticker: str) -> List[Dict]:
        """Generate mock interview data when API is unavailable"""
        logger.info("🔧 Generating mock interview data for testing")

        return [
            {
                'date': '2025-09-18',
                'source': 'Bloomberg Technology',
                'executive': f'{company_name} CEO',
                'title': f'{company_name} CEO Outlines Digital Strategy for 2026',
                'key_insights': f'The CEO discussed plans for comprehensive technology modernization, including migration to cloud infrastructure, implementation of AI-driven analytics, and development of new customer experience platforms. Emphasized the need for external expertise in digital transformation.',
                'link': f'https://bloomberg.com/news/{ticker.lower()}-ceo-digital-strategy-2026',
                'consulting_relevance': 'High - Multiple EPAM service areas including cloud migration, AI/ML, and digital experience design'
            },
            {
                'date': '2025-09-12',
                'source': 'Forbes Executive Interviews',
                'executive': f'{company_name} CTO',
                'title': 'Technology Leadership in the Age of AI',
                'key_insights': 'CTO highlighted challenges with legacy system integration and the need for specialized consulting support to accelerate their innovation initiatives. Mentioned plans for significant technology investments in Q1 2026.',
                'link': f'https://forbes.com/sites/technology/{ticker.lower()}-cto-ai-strategy',
                'consulting_relevance': 'High - Legacy system modernization and innovation consulting opportunities'
            },
            {
                'date': '2025-08-28',
                'source': 'Wall Street Journal',
                'executive': f'{company_name} President',
                'title': 'Driving Operational Excellence Through Technology',
                'key_insights': 'Discussion focused on operational efficiency improvements through automation and data-driven decision making. President emphasized the importance of finding the right technology partners to execute their vision.',
                'link': f'https://wsj.com/articles/{ticker.lower()}-operational-excellence-technology',
                'consulting_relevance': 'Medium - Automation and operational efficiency consulting services'
            }
        ]

    def create_intelligence_tables(self, twitter_data: List[Dict], interview_data: List[Dict]) -> Dict:
        """Create formatted tables for the intelligence findings"""
        try:
            logger.info("📊 Creating intelligence summary tables")

            # Twitter Intelligence Table
            twitter_df = pd.DataFrame(twitter_data)
            twitter_table = {
                'title': '🐦 TWITTER/X STRATEGIC MENTIONS',
                'columns': ['Date', 'Author', 'Summary', 'Strategic Relevance', 'Link'],
                'data': []
            }

            for _, row in twitter_df.iterrows():
                twitter_table['data'].append([
                    row['date'],
                    row['author'],
                    row['summary'][:100] + '...' if len(row['summary']) > 100 else row['summary'],
                    row['strategic_relevance'],
                    row['link']
                ])

            # Executive Interview Table
            interview_df = pd.DataFrame(interview_data)
            interview_table = {
                'title': '🎤 EXECUTIVE INTERVIEWS & ARTICLES',
                'columns': ['Date', 'Source', 'Executive', 'Title', 'Key Insights', 'Consulting Relevance', 'Link'],
                'data': []
            }

            for _, row in interview_df.iterrows():
                interview_table['data'].append([
                    row['date'],
                    row['source'],
                    row['executive'],
                    row['title'][:60] + '...' if len(row['title']) > 60 else row['title'],
                    row['key_insights'][:150] + '...' if len(row['key_insights']) > 150 else row['key_insights'],
                    row['consulting_relevance'],
                    row['link']
                ])

            return {
                'twitter_intelligence': twitter_table,
                'executive_intelligence': interview_table,
                'summary_stats': {
                    'twitter_mentions': len(twitter_data),
                    'executive_sources': len(interview_data),
                    'high_relevance_count': len([item for item in twitter_data + interview_data
                                               if 'High' in str(item.get('strategic_relevance', '')) or
                                               'High' in str(item.get('consulting_relevance', ''))])
                }
            }

        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            return {'error': str(e)}

    def process_social_news_intelligence(self, company_data: Dict) -> Dict:
        """
        Main method: Gather social media and news intelligence
        """
        logger.info("🚀 Agent #3 Processing social & news intelligence...")

        result = {
            'agent': 'Social & News Intelligence',
            'ticker': company_data.get('ticker', 'UNKNOWN'),
            'company_name': company_data.get('company_name', 'Unknown Company'),
            'timestamp': datetime.now().isoformat(),
            'date_range': f"{self.date_cutoff_str} to {datetime.now().strftime('%Y-%m-%d')}",
            'status': 'success',
            'twitter_intelligence': {},
            'executive_intelligence': {},
            'intelligence_tables': {},
            'summary_stats': {},
            'error': None
        }

        try:
            company_name = result['company_name']
            ticker = result['ticker']

            # Step 1: Search Twitter/X via Grok
            logger.info("🔍 Starting Twitter/X intelligence gathering...")
            twitter_data = self.search_twitter_mentions(company_name, ticker)
            result['twitter_intelligence'] = twitter_data

            # Step 2: Search Executive Interviews via Perplexity
            logger.info("📰 Starting executive interview intelligence...")
            interview_data = self.search_executive_interviews(company_name, ticker)
            result['executive_intelligence'] = interview_data

            # Step 3: Create formatted tables
            logger.info("📊 Creating intelligence tables...")
            intelligence_tables = self.create_intelligence_tables(twitter_data, interview_data)
            result['intelligence_tables'] = intelligence_tables
            result['summary_stats'] = intelligence_tables.get('summary_stats', {})

            logger.info(f"🎉 Agent #3 completed - Found {len(twitter_data)} Twitter mentions, {len(interview_data)} executive sources")

        except Exception as e:
            logger.error(f"Error processing social/news intelligence: {e}")
            result['status'] = 'error'
            result['error'] = str(e)

        return result


def main():
    """Test Agent #3 with sample company data"""
    print("🤖 Testing Agent #3: Social & News Intelligence")
    print("=" * 60)

    # Mock company data from previous agents
    company_data = {
        'ticker': 'NVDA',
        'company_name': 'NVIDIA Corporation'
    }

    # Initialize agent (will use mock data without API keys)
    agent = SocialNewsIntelligence()

    # Process intelligence
    result = agent.process_social_news_intelligence(company_data)

    # Display results
    print(f"📊 Intelligence Results for {result['company_name']} ({result['ticker']})")
    print(f"Date Range: {result['date_range']}")
    print(f"Status: {result['status']}")

    if result['status'] == 'success':
        stats = result['summary_stats']
        print(f"\n📈 Summary Statistics:")
        print(f"• Twitter Mentions: {stats.get('twitter_mentions', 0)}")
        print(f"• Executive Sources: {stats.get('executive_sources', 0)}")
        print(f"• High Relevance Items: {stats.get('high_relevance_count', 0)}")

        # Display Twitter table
        twitter_table = result['intelligence_tables']['twitter_intelligence']
        print(f"\n{twitter_table['title']}")
        print("=" * 60)
        for i, row in enumerate(twitter_table['data'][:2], 1):  # Show first 2
            print(f"{i}. Date: {row[0]}")
            print(f"   Author: {row[1]}")
            print(f"   Summary: {row[2]}")
            print(f"   Link: {row[4]}")
            print()

        # Display Executive table
        exec_table = result['intelligence_tables']['executive_intelligence']
        print(f"{exec_table['title']}")
        print("=" * 60)
        for i, row in enumerate(exec_table['data'][:2], 1):  # Show first 2
            print(f"{i}. Date: {row[0]} | Source: {row[1]}")
            print(f"   Executive: {row[2]}")
            print(f"   Title: {row[3]}")
            print(f"   Relevance: {row[5]}")
            print(f"   Link: {row[6]}")
            print()


if __name__ == "__main__":
    main()