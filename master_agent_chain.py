#!/usr/bin/env python3
"""
Master Agent Chain: Complete EPAM Business Intelligence System
Chains all three agents for comprehensive company analysis:
Agent #1: SEC Filing Retriever → Agent #2: Strategic Opportunity Analyzer → Agent #3: Social & News Intelligence
"""

import json
import sys
import os
import importlib.util
from datetime import datetime
from typing import Dict, List
import pandas as pd

# Import all three agents
def import_agent(agent_name: str, file_path: str):
    """Dynamic import of agent modules"""
    spec = importlib.util.spec_from_file_location(agent_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import agents
agent1_module = import_agent("agent1", "/Users/dickgibbons/agent_1_sec_filing_retriever.py")
agent2_module = import_agent("agent2", "/Users/dickgibbons/agent_2_strategic_opportunity_analyzer.py")
agent3_module = import_agent("agent3", "/Users/dickgibbons/agent_3_social_news_intelligence.py")

SECFilingRetriever = agent1_module.SECFilingRetriever
StrategicOpportunityAnalyzer = agent2_module.StrategicOpportunityAnalyzer
SocialNewsIntelligence = agent3_module.SocialNewsIntelligence

class MasterEPAMIntelligenceChain:
    """Complete EPAM business intelligence analysis chain"""

    def __init__(self, grok_api_key: str = None, perplexity_api_key: str = None):
        print("🚀 Initializing Master EPAM Intelligence Chain")
        print("=" * 70)

        self.agent1 = SECFilingRetriever()
        self.agent2 = StrategicOpportunityAnalyzer()
        self.agent3 = SocialNewsIntelligence(grok_api_key, perplexity_api_key)

        # Company name mapping for better Agent #3 results
        self.company_names = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'TSLA': 'Tesla Inc.',
            'META': 'Meta Platforms Inc.',
            'NVDA': 'NVIDIA Corporation'
        }

    def analyze_company_complete(self, ticker: str) -> Dict:
        """
        Run complete analysis: SEC filings → Strategic analysis → Social/News intelligence
        """
        print(f"🎯 STARTING COMPLETE ANALYSIS FOR {ticker}")
        print("=" * 70)

        company_name = self.company_names.get(ticker.upper(), f"{ticker} Corporation")

        master_result = {
            'analysis_type': 'Complete EPAM Business Intelligence',
            'ticker': ticker.upper(),
            'company_name': company_name,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'agent_1_result': {},
            'agent_2_result': {},
            'agent_3_result': {},
            'executive_summary': '',
            'consolidated_opportunities': [],
            'intelligence_dashboard': {},
            'error': None
        }

        try:
            # AGENT #1: SEC Filing Retrieval
            print("🤖 STEP 1: SEC Filing Intelligence...")
            print("-" * 50)
            agent1_result = self.agent1.process_ticker(ticker)
            master_result['agent_1_result'] = agent1_result

            if agent1_result['status'] != 'success':
                print(f"⚠️  Agent #1 Warning: {agent1_result.get('error', 'Unknown issue')}")
                # Continue anyway - other agents can still provide value

            filings_found = len(agent1_result.get('filings', {}))
            print(f"✅ Agent #1 Complete: {filings_found} SEC filings retrieved")

            # AGENT #2: Strategic Opportunity Analysis
            print("\n🤖 STEP 2: Strategic Opportunity Analysis...")
            print("-" * 50)
            agent2_result = self.agent2.process_filing_analysis(agent1_result)
            master_result['agent_2_result'] = agent2_result

            opportunities_found = agent2_result.get('total_opportunities', 0)
            high_priority = agent2_result.get('high_priority_count', 0)
            print(f"✅ Agent #2 Complete: {opportunities_found} opportunities ({high_priority} high priority)")

            # AGENT #3: Social & News Intelligence
            print("\n🤖 STEP 3: Social & News Intelligence...")
            print("-" * 50)

            company_data = {
                'ticker': ticker.upper(),
                'company_name': company_name
            }

            agent3_result = self.agent3.process_social_news_intelligence(company_data)
            master_result['agent_3_result'] = agent3_result

            twitter_mentions = len(agent3_result.get('twitter_intelligence', []))
            executive_sources = len(agent3_result.get('executive_intelligence', []))
            print(f"✅ Agent #3 Complete: {twitter_mentions} social mentions, {executive_sources} executive sources")

            # CONSOLIDATION: Create unified business intelligence
            print("\n📊 CONSOLIDATING BUSINESS INTELLIGENCE...")
            print("-" * 50)

            master_result['consolidated_opportunities'] = self._consolidate_opportunities(
                agent2_result, agent3_result
            )

            master_result['intelligence_dashboard'] = self._create_intelligence_dashboard(
                agent1_result, agent2_result, agent3_result
            )

            master_result['executive_summary'] = self._generate_master_executive_summary(
                ticker, company_name, agent1_result, agent2_result, agent3_result
            )

            print("🎉 MASTER ANALYSIS COMPLETE!")

        except Exception as e:
            print(f"❌ Master chain error: {e}")
            master_result['status'] = 'error'
            master_result['error'] = str(e)

        return master_result

    def _consolidate_opportunities(self, agent2_result: Dict, agent3_result: Dict) -> List[Dict]:
        """Consolidate opportunities from strategic analysis and social intelligence"""
        try:
            consolidated = []

            # Get strategic opportunities from Agent #2
            strategic_opportunities = agent2_result.get('opportunities', [])

            for opp in strategic_opportunities:
                # Find supporting evidence from Agent #3
                social_evidence = self._find_supporting_evidence(
                    opp['opportunity_area'],
                    agent3_result.get('twitter_intelligence', []) +
                    agent3_result.get('executive_intelligence', [])
                )

                consolidated_opp = {
                    'opportunity_area': opp['opportunity_area'],
                    'epam_services': opp['epam_services'],
                    'sec_confidence': opp['confidence_score'],
                    'priority_level': opp['priority_level'],
                    'sec_evidence': opp['key_indicators'],
                    'social_evidence': social_evidence,
                    'total_evidence_sources': len(opp['key_indicators']) + len(social_evidence),
                    'overall_confidence': self._calculate_overall_confidence(
                        opp['confidence_score'], len(social_evidence)
                    )
                }

                consolidated.append(consolidated_opp)

            # Sort by overall confidence
            consolidated.sort(key=lambda x: x['overall_confidence'], reverse=True)
            return consolidated

        except Exception as e:
            print(f"Error consolidating opportunities: {e}")
            return []

    def _find_supporting_evidence(self, opportunity_area: str, social_data: List[Dict]) -> List[str]:
        """Find social/news evidence supporting an opportunity area"""
        evidence = []
        area_keywords = {
            'Digital Transformation': ['digital', 'transformation', 'modernization'],
            'Technology Modernization': ['modernization', 'upgrade', 'legacy', 'cloud'],
            'Data Analytics': ['data', 'analytics', 'AI', 'machine learning'],
            'Customer Experience': ['customer', 'experience', 'user'],
            'Operational Efficiency': ['efficiency', 'automation', 'process']
        }

        keywords = area_keywords.get(opportunity_area, [])

        for item in social_data:
            content = str(item.get('summary', '')) + str(item.get('key_insights', ''))
            content_lower = content.lower()

            for keyword in keywords:
                if keyword in content_lower:
                    source = item.get('source', item.get('author', 'Social Media'))
                    evidence.append(f"{source}: {keyword} mentioned")
                    break

        return list(set(evidence))[:3]  # Top 3 unique evidence sources

    def _calculate_overall_confidence(self, sec_confidence: float, social_evidence_count: int) -> float:
        """Calculate overall confidence combining SEC and social evidence"""
        # Base confidence from SEC analysis
        base_confidence = sec_confidence

        # Boost from social evidence
        social_boost = min(social_evidence_count * 0.1, 0.3)  # Max 30% boost

        return min(base_confidence + social_boost, 1.0)

    def _create_intelligence_dashboard(self, agent1_result: Dict, agent2_result: Dict, agent3_result: Dict) -> Dict:
        """Create consolidated intelligence dashboard"""
        try:
            dashboard = {
                'filing_intelligence': {
                    'filings_analyzed': list(agent1_result.get('filings', {}).keys()),
                    'most_recent_filing': self._get_most_recent_filing(agent1_result.get('filings', {}))
                },
                'strategic_intelligence': {
                    'total_opportunities': agent2_result.get('total_opportunities', 0),
                    'high_priority_opportunities': agent2_result.get('high_priority_count', 0),
                    'top_opportunity': agent2_result.get('opportunities', [{}])[0].get('opportunity_area', 'None') if agent2_result.get('opportunities') else 'None'
                },
                'social_intelligence': {
                    'twitter_mentions': len(agent3_result.get('twitter_intelligence', [])),
                    'executive_sources': len(agent3_result.get('executive_intelligence', [])),
                    'high_relevance_count': agent3_result.get('summary_stats', {}).get('high_relevance_count', 0)
                },
                'overall_assessment': {
                    'engagement_readiness': self._assess_engagement_readiness(agent1_result, agent2_result, agent3_result),
                    'recommended_next_steps': self._get_recommended_next_steps(agent2_result, agent3_result)
                }
            }

            return dashboard

        except Exception as e:
            print(f"Error creating dashboard: {e}")
            return {}

    def _get_most_recent_filing(self, filings: Dict) -> str:
        """Get the most recent filing date"""
        if not filings:
            return 'None'

        most_recent = None
        most_recent_date = None

        for form_type, filing in filings.items():
            filing_date = filing.get('filing_date')
            if filing_date:
                if not most_recent_date or filing_date > most_recent_date:
                    most_recent_date = filing_date
                    most_recent = f"{form_type}: {filing_date}"

        return most_recent or 'None'

    def _assess_engagement_readiness(self, agent1_result: Dict, agent2_result: Dict, agent3_result: Dict) -> str:
        """Assess overall readiness for EPAM engagement"""
        # Score based on available intelligence
        score = 0

        # SEC filing availability
        if agent1_result.get('status') == 'success' and agent1_result.get('filings'):
            score += 3

        # Strategic opportunities
        high_priority = agent2_result.get('high_priority_count', 0)
        if high_priority >= 2:
            score += 3
        elif high_priority >= 1:
            score += 2

        # Social intelligence
        high_relevance = agent3_result.get('summary_stats', {}).get('high_relevance_count', 0)
        if high_relevance >= 3:
            score += 2
        elif high_relevance >= 1:
            score += 1

        # Determine readiness level
        if score >= 7:
            return "HIGH - Multiple strong indicators for engagement"
        elif score >= 4:
            return "MEDIUM - Good foundation for targeted outreach"
        else:
            return "LOW - Limited intelligence, requires more research"

    def _get_recommended_next_steps(self, agent2_result: Dict, agent3_result: Dict) -> List[str]:
        """Generate recommended next steps based on analysis"""
        steps = []

        # Based on strategic opportunities
        opportunities = agent2_result.get('opportunities', [])
        if opportunities:
            top_opp = opportunities[0]
            steps.append(f"Develop {top_opp['opportunity_area']} proposal focusing on {top_opp['epam_services']}")

        # Based on social intelligence
        high_relevance = agent3_result.get('summary_stats', {}).get('high_relevance_count', 0)
        if high_relevance > 0:
            steps.append("Schedule discovery call to discuss recent strategic initiatives mentioned in executive communications")

        # General recommendations
        if len(steps) < 2:
            steps.extend([
                "Prepare targeted case studies aligned with identified opportunities",
                "Monitor for RFP announcements in priority opportunity areas"
            ])

        return steps[:3]  # Top 3 recommendations

    def _generate_master_executive_summary(self, ticker: str, company_name: str,
                                         agent1_result: Dict, agent2_result: Dict, agent3_result: Dict) -> str:
        """Generate comprehensive executive summary"""
        try:
            summary = f"""
🎯 EPAM MASTER BUSINESS INTELLIGENCE REPORT
{'=' * 80}

🏢 TARGET COMPANY: {company_name} ({ticker})
📅 ANALYSIS DATE: {datetime.now().strftime('%Y-%m-%d')}
🤖 INTELLIGENCE SOURCES: SEC Filings + Strategic Analysis + Social/News Monitoring

📊 EXECUTIVE SUMMARY:
"""

            # SEC Intelligence
            filings = agent1_result.get('filings', {})
            if filings:
                recent_filing = self._get_most_recent_filing(filings)
                summary += f"• SEC Filings: {len(filings)} documents analyzed ({recent_filing})\n"

            # Strategic Opportunities
            total_opps = agent2_result.get('total_opportunities', 0)
            high_priority = agent2_result.get('high_priority_count', 0)
            summary += f"• Strategic Opportunities: {total_opps} identified ({high_priority} high priority)\n"

            # Social Intelligence
            twitter_mentions = len(agent3_result.get('twitter_intelligence', []))
            executive_sources = len(agent3_result.get('executive_intelligence', []))
            summary += f"• Market Intelligence: {twitter_mentions} social mentions, {executive_sources} executive sources\n"

            # Top Opportunities
            summary += "\n🔥 TOP EPAM OPPORTUNITIES:\n"
            opportunities = agent2_result.get('opportunities', [])
            for i, opp in enumerate(opportunities[:3], 1):
                summary += f"{i}. {opp['opportunity_area']} - {opp['epam_services']} (Confidence: {opp['confidence_score']})\n"

            # Intelligence Highlights
            summary += "\n📈 KEY INTELLIGENCE HIGHLIGHTS:\n"

            # Recent executive mentions
            exec_intel = agent3_result.get('executive_intelligence', [])
            if exec_intel:
                recent_exec = exec_intel[0]
                summary += f"• Recent Executive Focus: {recent_exec.get('title', 'Strategic initiatives')} ({recent_exec.get('date', 'Recent')})\n"

            # Social momentum
            twitter_intel = agent3_result.get('twitter_intelligence', [])
            if twitter_intel:
                summary += f"• Social Momentum: Active discussion of strategic initiatives on social platforms\n"

            # Assessment
            dashboard = self._create_intelligence_dashboard(agent1_result, agent2_result, agent3_result)
            readiness = dashboard.get('overall_assessment', {}).get('engagement_readiness', 'Unknown')
            summary += f"\n🎯 ENGAGEMENT READINESS: {readiness}\n"

            # Next Steps
            next_steps = dashboard.get('overall_assessment', {}).get('recommended_next_steps', [])
            summary += "\n💼 RECOMMENDED NEXT STEPS:\n"
            for i, step in enumerate(next_steps, 1):
                summary += f"{i}. {step}\n"

            summary += f"\n{'=' * 80}"

            return summary

        except Exception as e:
            return f"Error generating master summary: {e}"

    def save_complete_analysis(self, result: Dict, ticker: str):
        """Save complete analysis to multiple formats"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # JSON format
        json_filename = f"epam_master_analysis_{ticker}_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(result, f, indent=2, default=str)

        # Executive summary text
        summary_filename = f"epam_executive_summary_{ticker}_{timestamp}.txt"
        with open(summary_filename, 'w') as f:
            f.write(result['executive_summary'])

        print(f"\n💾 Analysis saved:")
        print(f"   📄 Complete Data: {json_filename}")
        print(f"   📋 Executive Summary: {summary_filename}")

        return json_filename, summary_filename


def main():
    """Run the complete master analysis chain"""
    print("🎯 EPAM MASTER BUSINESS INTELLIGENCE SYSTEM")
    print("=" * 80)

    # Get ticker from command line
    if len(sys.argv) < 2:
        print("Usage: python master_agent_chain.py <TICKER> [GROK_API_KEY] [PERPLEXITY_API_KEY]")
        print("Example: python master_agent_chain.py NVDA")
        sys.exit(1)

    ticker = sys.argv[1].upper()

    # Optional API keys
    grok_key = sys.argv[2] if len(sys.argv) > 2 else None
    perplexity_key = sys.argv[3] if len(sys.argv) > 3 else None

    # Initialize master chain
    master_chain = MasterEPAMIntelligenceChain(grok_key, perplexity_key)

    # Run complete analysis
    result = master_chain.analyze_company_complete(ticker)

    # Display executive summary
    print("\n" + "=" * 80)
    print("📋 EXECUTIVE SUMMARY")
    print("=" * 80)
    print(result['executive_summary'])

    # Save results
    master_chain.save_complete_analysis(result, ticker)


if __name__ == "__main__":
    main()