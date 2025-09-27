#!/usr/bin/env python3
"""
Agent #2: Strategic Opportunity Analyzer
Input: SEC filing content from Agent #1
Output: Strategic priorities and EPAM consulting opportunities
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StrategicOpportunityAnalyzer:
    """Agent #2 - Analyzes SEC filings for EPAM consulting opportunities"""

    def __init__(self):
        self.strategic_keywords = {
            'digital_transformation': [
                'digital transformation', 'digitalization', 'digital initiatives',
                'digital strategy', 'digital platform', 'digital capabilities',
                'modernizing', 'modernization', 'digitize', 'digital experience'
            ],
            'technology_modernization': [
                'legacy systems', 'technology upgrade', 'infrastructure modernization',
                'system integration', 'technology transformation', 'migrate',
                'cloud adoption', 'cloud migration', 'cloud transformation',
                'software development', 'application modernization'
            ],
            'data_analytics': [
                'data analytics', 'big data', 'data science', 'machine learning',
                'artificial intelligence', 'AI', 'predictive analytics',
                'data-driven', 'business intelligence', 'data platform'
            ],
            'customer_experience': [
                'customer experience', 'user experience', 'customer journey',
                'omnichannel', 'personalization', 'customer engagement',
                'digital channels', 'customer satisfaction', 'user interface'
            ],
            'operational_efficiency': [
                'operational efficiency', 'process automation', 'streamline operations',
                'cost reduction', 'productivity', 'efficiency gains',
                'automation', 'optimize operations', 'process improvement'
            ],
            'innovation_investment': [
                'innovation', 'R&D investment', 'research and development',
                'new technologies', 'emerging technologies', 'pilot programs',
                'innovation initiatives', 'technology investment'
            ],
            'market_expansion': [
                'market expansion', 'new markets', 'geographic expansion',
                'international expansion', 'growth strategy', 'market penetration',
                'new business lines', 'strategic partnerships'
            ],
            'cybersecurity': [
                'cybersecurity', 'data security', 'information security',
                'cyber threats', 'security measures', 'data protection',
                'compliance', 'risk management', 'security infrastructure'
            ]
        }

        self.epam_services_mapping = {
            'digital_transformation': 'Digital Platform Engineering, Consulting Services',
            'technology_modernization': 'Software Engineering, Cloud & DevOps',
            'data_analytics': 'Data & Analytics, AI/ML Services',
            'customer_experience': 'Product Design, Digital Experience',
            'operational_efficiency': 'Process Automation, Consulting Services',
            'innovation_investment': 'Innovation Labs, Emerging Technology Services',
            'market_expansion': 'Digital Strategy, Market Entry Consulting',
            'cybersecurity': 'Security Services, Compliance Solutions'
        }

        self.section_indicators = {
            'md_a': [
                "management's discussion and analysis",
                "management discussion and analysis",
                "md&a", "mda",
                "results of operations",
                "liquidity and capital resources"
            ],
            'business_segments': [
                "business segments",
                "segment information",
                "operating segments",
                "reportable segments",
                "segment performance",
                "segment results"
            ],
            'strategy': [
                "business strategy",
                "strategic initiatives",
                "strategic priorities",
                "strategic plan",
                "corporate strategy"
            ],
            'risk_factors': [
                "risk factors",
                "principal risks",
                "key risks",
                "business risks"
            ]
        }

    def extract_filing_sections(self, filing_content: str) -> Dict[str, str]:
        """Extract key sections from SEC filing content"""
        try:
            logger.info("🔍 Extracting key sections from filing...")

            sections = {}

            # Convert to lowercase for matching
            content_lower = filing_content.lower()

            for section_name, indicators in self.section_indicators.items():
                section_content = ""

                for indicator in indicators:
                    # Find section start
                    pattern = rf'\b{re.escape(indicator)}\b.*?(?=\n|$)'
                    matches = list(re.finditer(pattern, content_lower, re.IGNORECASE | re.MULTILINE))

                    if matches:
                        # Get the position of the first match
                        start_pos = matches[0].start()

                        # Extract content (next 5000 characters as a reasonable section size)
                        section_end = min(start_pos + 5000, len(filing_content))
                        section_text = filing_content[start_pos:section_end]

                        if len(section_text) > len(section_content):
                            section_content = section_text

                if section_content:
                    sections[section_name] = section_content
                    logger.info(f"✅ Extracted {section_name} section ({len(section_content)} chars)")

            # If no specific sections found, use the entire content in chunks
            if not sections:
                logger.warning("No specific sections identified, using full content")
                sections['full_content'] = filing_content[:10000]  # First 10k chars

            return sections

        except Exception as e:
            logger.error(f"Error extracting sections: {e}")
            return {'full_content': filing_content[:5000]}

    def analyze_strategic_priorities(self, sections: Dict[str, str]) -> Dict[str, List[Dict]]:
        """Analyze text for strategic priorities and opportunities"""
        try:
            logger.info("🎯 Analyzing strategic priorities...")

            opportunities = {}

            # Combine all sections for analysis
            all_text = " ".join(sections.values()).lower()

            for category, keywords in self.strategic_keywords.items():
                matches = []

                for keyword in keywords:
                    # Find keyword mentions with context
                    pattern = rf'.{{0,100}}\b{re.escape(keyword)}\b.{{0,100}}'
                    keyword_matches = re.findall(pattern, all_text, re.IGNORECASE)

                    for match in keyword_matches:
                        # Clean up the match
                        clean_match = match.strip()
                        if len(clean_match) > 50:  # Only include substantial matches
                            matches.append({
                                'keyword': keyword,
                                'context': clean_match,
                                'confidence': self._calculate_confidence(clean_match, keyword)
                            })

                if matches:
                    # Sort by confidence and take top matches
                    matches.sort(key=lambda x: x['confidence'], reverse=True)
                    opportunities[category] = matches[:3]  # Top 3 matches per category

            logger.info(f"✅ Identified opportunities in {len(opportunities)} categories")
            return opportunities

        except Exception as e:
            logger.error(f"Error analyzing strategic priorities: {e}")
            return {}

    def _calculate_confidence(self, context: str, keyword: str) -> float:
        """Calculate confidence score for a strategic priority match"""
        confidence = 0.5  # Base confidence

        # Boost confidence for certain action words
        action_words = ['invest', 'focus', 'prioritize', 'expand', 'develop', 'implement', 'launch', 'accelerate']
        for word in action_words:
            if word in context.lower():
                confidence += 0.1

        # Boost confidence for future-oriented language
        future_words = ['will', 'plan', 'expect', 'intend', 'strategy', 'initiative', 'project']
        for word in future_words:
            if word in context.lower():
                confidence += 0.1

        # Boost confidence for financial context
        financial_words = ['invest', 'spending', 'budget', 'capital', 'revenue', 'growth']
        for word in financial_words:
            if word in context.lower():
                confidence += 0.1

        return min(confidence, 1.0)

    def map_to_epam_opportunities(self, strategic_priorities: Dict) -> List[Dict]:
        """Map strategic priorities to specific EPAM service opportunities"""
        try:
            logger.info("🎯 Mapping to EPAM opportunities...")

            epam_opportunities = []

            for category, matches in strategic_priorities.items():
                if not matches:
                    continue

                epam_services = self.epam_services_mapping.get(category, 'General Consulting')

                # Calculate overall category confidence
                avg_confidence = sum(match['confidence'] for match in matches) / len(matches)

                opportunity = {
                    'opportunity_area': category.replace('_', ' ').title(),
                    'epam_services': epam_services,
                    'confidence_score': round(avg_confidence, 2),
                    'evidence_count': len(matches),
                    'key_indicators': [match['keyword'] for match in matches],
                    'context_examples': [match['context'][:200] + '...' if len(match['context']) > 200
                                       else match['context'] for match in matches[:2]],
                    'priority_level': self._determine_priority_level(avg_confidence, len(matches))
                }

                epam_opportunities.append(opportunity)

            # Sort by confidence and evidence count
            epam_opportunities.sort(key=lambda x: (x['confidence_score'], x['evidence_count']), reverse=True)

            logger.info(f"✅ Mapped {len(epam_opportunities)} EPAM opportunities")
            return epam_opportunities

        except Exception as e:
            logger.error(f"Error mapping EPAM opportunities: {e}")
            return []

    def _determine_priority_level(self, confidence: float, evidence_count: int) -> str:
        """Determine priority level based on confidence and evidence"""
        if confidence >= 0.8 and evidence_count >= 2:
            return "HIGH"
        elif confidence >= 0.6 and evidence_count >= 1:
            return "MEDIUM"
        else:
            return "LOW"

    def generate_executive_summary(self, opportunities: List[Dict], ticker: str) -> str:
        """Generate executive summary for business development"""
        try:
            high_priority = [opp for opp in opportunities if opp['priority_level'] == 'HIGH']
            medium_priority = [opp for opp in opportunities if opp['priority_level'] == 'MEDIUM']

            summary = f"""
🎯 EPAM CONSULTING OPPORTUNITY ANALYSIS - {ticker}
{'=' * 60}

📊 EXECUTIVE SUMMARY:
• {len(opportunities)} strategic opportunity areas identified
• {len(high_priority)} HIGH priority opportunities
• {len(medium_priority)} MEDIUM priority opportunities

🔥 TOP OPPORTUNITIES:
"""

            for i, opp in enumerate(opportunities[:3], 1):
                summary += f"""
{i}. {opp['opportunity_area']} [{opp['priority_level']} Priority]
   → EPAM Services: {opp['epam_services']}
   → Confidence: {opp['confidence_score']}/1.0
   → Evidence: {opp['evidence_count']} indicators found
"""

            summary += f"""
💼 RECOMMENDED ACTIONS:
1. Schedule discovery call to discuss {opportunities[0]['opportunity_area']} initiatives
2. Prepare case studies relevant to their strategic priorities
3. Develop proposal focusing on highest-confidence opportunities

📈 BUSINESS CONTEXT:
Based on SEC filing analysis, this company is actively investing in areas
where EPAM has proven expertise and successful delivery track record.
"""

            return summary

        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Error generating executive summary"

    def process_filing_analysis(self, agent1_output: Dict) -> Dict:
        """
        Main method: Process SEC filing content and identify EPAM opportunities
        """
        logger.info("🚀 Agent #2 Processing SEC filing analysis...")

        result = {
            'agent': 'Strategic Opportunity Analyzer',
            'ticker': agent1_output.get('ticker', 'UNKNOWN'),
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'opportunities': [],
            'executive_summary': '',
            'total_opportunities': 0,
            'high_priority_count': 0,
            'error': None
        }

        try:
            # Check if Agent 1 was successful
            if agent1_output.get('status') != 'success':
                result['status'] = 'error'
                result['error'] = 'Agent 1 failed to retrieve filings'
                return result

            filings = agent1_output.get('filings', {})
            if not filings:
                result['status'] = 'error'
                result['error'] = 'No filing content available'
                return result

            # Analyze both 10-K and 10-Q if available
            all_content = ""
            for form_type, filing_data in filings.items():
                content = filing_data.get('full_content', '') or filing_data.get('content', '')
                if content:
                    all_content += f"\n\n=== {form_type} CONTENT ===\n\n" + content

            if not all_content:
                result['status'] = 'warning'
                result['error'] = 'No substantial content found in filings'
                return result

            # Step 1: Extract key sections
            sections = self.extract_filing_sections(all_content)

            # Step 2: Analyze strategic priorities
            strategic_priorities = self.analyze_strategic_priorities(sections)

            # Step 3: Map to EPAM opportunities
            opportunities = self.map_to_epam_opportunities(strategic_priorities)

            # Step 4: Generate executive summary
            executive_summary = self.generate_executive_summary(opportunities, result['ticker'])

            # Populate results
            result['opportunities'] = opportunities
            result['executive_summary'] = executive_summary
            result['total_opportunities'] = len(opportunities)
            result['high_priority_count'] = len([opp for opp in opportunities if opp['priority_level'] == 'HIGH'])

            logger.info(f"🎉 Agent #2 completed successfully for {result['ticker']}")

        except Exception as e:
            logger.error(f"Error processing filing analysis: {e}")
            result['status'] = 'error'
            result['error'] = str(e)

        return result


def main():
    """Test Agent #2 with sample data"""
    # Simulate Agent #1 output for testing
    sample_agent1_output = {
        'agent': 'SEC Filing Retriever',
        'ticker': 'TEST',
        'status': 'success',
        'filings': {
            '10-K': {
                'form_type': '10-K',
                'filing_date': '2024-11-01',
                'content': """
                MANAGEMENT'S DISCUSSION AND ANALYSIS

                Our strategy focuses on digital transformation initiatives to modernize our technology infrastructure.
                We plan to invest significantly in cloud migration and data analytics capabilities to improve
                operational efficiency and enhance customer experience. We are prioritizing automation and
                artificial intelligence to streamline operations and reduce costs.

                Key strategic initiatives include:
                1. Legacy systems modernization project
                2. Customer experience platform development
                3. Data analytics and machine learning implementation
                4. Cybersecurity infrastructure enhancement

                We expect these investments to drive growth and improve our competitive position.
                """
            }
        }
    }

    print("🤖 Testing Agent #2: Strategic Opportunity Analyzer")
    print("=" * 60)

    agent = StrategicOpportunityAnalyzer()
    result = agent.process_filing_analysis(sample_agent1_output)

    # Print results
    print(f"\n📊 Analysis Results:")
    print(f"Status: {result['status']}")
    print(f"Total Opportunities: {result['total_opportunities']}")
    print(f"High Priority: {result['high_priority_count']}")

    if result['opportunities']:
        print(f"\n🎯 Top Opportunities:")
        for i, opp in enumerate(result['opportunities'][:3], 1):
            print(f"{i}. {opp['opportunity_area']} [{opp['priority_level']}]")
            print(f"   EPAM Services: {opp['epam_services']}")
            print(f"   Confidence: {opp['confidence_score']}")

    print(f"\n{result['executive_summary']}")


if __name__ == "__main__":
    main()