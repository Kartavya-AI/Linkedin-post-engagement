#!/usr/bin/env python
import sys
from linkedin_crew import LinkedinCrew

def run():
    """
    Run the LinkedIn automation crew.
    
    Before running this script:
    1. Obtain your LinkedIn access token 
    2. Add it to your .env file as LINKEDIN_ACCESS_TOKEN=your_token_here
    3. Run this script
    """
    
    print("🔗 LinkedIn Automation Crew")
    print("=" * 50)
    
    # Get search query from user
    search_query = input("\n🔍 Enter your search query for LinkedIn prospecting: ").strip()
    
    if not search_query:
        print("❌ Search query is required.")
        sys.exit(1)
    
    print(f"\n🚀 Starting LinkedIn automation with search query: '{search_query}'")
    print("📋 This will:")
    print("   1. Transform your query into customer-focused search strategies")
    print("   2. Discover relevant LinkedIn prospects")
    print("   3. Analyze prospect content and engagement opportunities")
    print("   4. Generate engagement strategy and suggested comments")
    
    # Initialize and run the crew
    try:
        crew = LinkedinCrew()
        
        inputs = {
            'search_query': search_query
        }
        
        print(f"\n⏳ Running LinkedIn automation crew...")
        result = crew.crew().kickoff(inputs=inputs)
        
        print(f"\n✅ LinkedIn automation completed!")
        print(f"\n📊 Results:")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error running crew: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()
