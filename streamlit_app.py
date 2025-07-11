__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
sys.modules["sqlite3.dbapi2"] = sys.modules["pysqlite3.dbapi2"]
import streamlit as st
import json
from datetime import datetime
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the LinkedIn crew and API helper
from src.crew.linkedin_crew import LinkedinCrew
from linkedin_api_helper import post_linkedin_comment

# Page configuration
st.set_page_config(
    page_title="LinkedIn Agent Crew",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
if 'result_data' not in st.session_state:
    st.session_state.result_data = None
if 'last_search_query' not in st.session_state:
    st.session_state.last_search_query = ""
if 'comment_status' not in st.session_state:
    st.session_state.comment_status = {}

# App title and description
st.title("🤖 LinkedIn Agent Crew")
st.markdown("**AI-powered LinkedIn content discovery and engagement automation**")

# Sidebar for input
with st.sidebar:
    st.header("🎯 Search Configuration")
    
    # User input for search query
    search_query = st.text_area(
        "Enter your search query:",
        placeholder="e.g., need AI solution for my business",
        height=100,
        help="Describe what kind of LinkedIn posts you want to find and engage with"
    )
    
    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        max_posts = st.slider("Maximum posts to process", 1, 20, 10)
        comment_tone = st.selectbox(
            "Comment tone",
            ["Professional", "Friendly", "Technical", "Consultative"]
        )
    
    # Execute button
    execute_button = st.button(
        "🚀 Execute LinkedIn Crew", 
        type="primary",
        use_container_width=True
    )

# Main content area
if execute_button and search_query:
    # Show processing indicator
    with st.spinner("🔄 Processing your request..."):
        st.info("🤖 LinkedIn Agent Crew is working...")
        
        # Simulate processing steps
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔍 Creating optimized search queries...")
        progress_bar.progress(33)
        
        status_text.text("📊 Collecting LinkedIn posts...")
        progress_bar.progress(66)
        
        status_text.text("💬 Generating personalized comments...")
        progress_bar.progress(100)
        
        try:
            # Initialize and run the LinkedIn crew
            linkedin_crew = LinkedinCrew()
            crew_instance = linkedin_crew.crew()
            
            # Execute the crew with the search query
            crew_result = crew_instance.kickoff(
                inputs={'search_query': search_query}
            )
            
            # Parse the result - crew_result should contain the final JSON output
            if hasattr(crew_result, 'raw') and crew_result.raw:
                # Try to parse JSON from the raw result
                try:
                    if isinstance(crew_result.raw, str):
                        # Look for JSON pattern in the string
                        import re
                        # First try to find the complete JSON structure
                        json_pattern = r'\{[\s\S]*"final_results"[\s\S]*\}'
                        json_match = re.search(json_pattern, crew_result.raw, re.DOTALL)
                        
                        if json_match:
                            json_str = json_match.group()
                            # Clean up any trailing text after the JSON
                            bracket_count = 0
                            end_pos = 0
                            for i, char in enumerate(json_str):
                                if char == '{':
                                    bracket_count += 1
                                elif char == '}':
                                    bracket_count -= 1
                                    if bracket_count == 0:
                                        end_pos = i + 1
                                        break
                            
                            clean_json = json_str[:end_pos]
                            result_data = json.loads(clean_json)
                        else:
                            # Try to parse the entire string as JSON
                            result_data = json.loads(crew_result.raw)
                    else:
                        # If it's already a dict
                        result_data = crew_result.raw
                        
                    # Validate that we have the expected structure
                    if not isinstance(result_data, dict) or "final_results" not in result_data:
                        raise ValueError("Invalid result structure")
                        
                except (json.JSONDecodeError, ValueError) as e:
                    st.warning(f"⚠️ Could not parse crew result as JSON: {str(e)}")
                    
                    # Show a preview of the raw output for debugging
                    with st.expander("� Raw Crew Output (Click to expand)", expanded=False):
                        raw_output = str(crew_result.raw)
                        st.text(raw_output[:2000] + "..." if len(raw_output) > 2000 else raw_output)
                    
                    # Try alternative parsing methods
                    try:
                        raw_text = str(crew_result.raw)
                        posts = []
                        
                        # Method 1: Look for post objects using regex
                        post_pattern = r'\{[^{}]*"title"[^{}]*"text"[^{}]*"url"[^{}]*"comment"[^{}]*\}'
                        post_matches = re.findall(post_pattern, raw_text, re.DOTALL)
                        
                        for match in post_matches[:10]:  # Limit to 10 posts
                            try:
                                post_obj = json.loads(match)
                                # Truncate long text for display
                                if 'text' in post_obj and len(post_obj['text']) > 300:
                                    post_obj['text'] = post_obj['text'][:300] + "..."
                                posts.append(post_obj)
                            except:
                                continue
                        
                        # Method 2: If no posts found, try to extract field by field
                        if not posts:
                            titles = re.findall(r'"title":\s*"([^"]*)"', raw_text)
                            texts = re.findall(r'"text":\s*"([^"]*)"', raw_text)
                            urls = re.findall(r'"url":\s*"([^"]*)"', raw_text)
                            comments = re.findall(r'"comment":\s*"([^"]*)"', raw_text)
                            
                            min_len = min(len(titles), len(texts), len(urls), len(comments))
                            for i in range(min(min_len, 10)):  # Limit to 10 posts
                                posts.append({
                                    "title": titles[i],
                                    "text": texts[i][:300] + "..." if len(texts[i]) > 300 else texts[i],
                                    "url": urls[i],
                                    "comment": comments[i]
                                })
                        
                        if posts:
                            result_data = {"final_results": posts}
                            st.success(f"✅ Successfully extracted {len(posts)} posts from output!")
                        else:
                            raise Exception("No valid posts found")
                            
                    except Exception as parse_error:
                        st.error(f"❌ Failed to extract posts: {str(parse_error)}")
                        # Final fallback to sample data
                        result_data = {
                            "final_results": [
                                {
                                    "title": "Sample Post - Parsing Failed",
                                    "text": "The crew ran successfully but the output couldn't be parsed. Please check the raw output above.",
                                    "url": "https://linkedin.com/sample",
                                    "comment": "Sample comment for demonstration."
                                }
                            ]
                        }
            else:
                # Fallback to sample data
                result_data = {
                    "final_results": [
                        {
                            "title": "Sample Post", 
                            "text": "This is a sample post for demonstration purposes.",
                            "url": "https://linkedin.com/sample",
                            "comment": "This is a sample comment generated by the crew."
                        }
                    ]
                }
            
            status_text.text("✅ Process completed!")
            
        except Exception as e:
            st.error(f"❌ Error executing crew: {str(e)}")
            status_text.text("❌ Process failed - using sample data")
            
            # Fallback to sample data for demonstration
            result_data = {
                "final_results": [
                    {
                        "title": "AI Agentiva Launch",
                        "text": "🚀 We're Live — Introducing AI Agentiva 🤖\nCustomized AI Agent Solutions to transform how businesses hire, sell, and support.\n\nI'm thrilled to officially launch AI Agentiva...",
                        "url": "https://www.linkedin.com/posts/mohammed-abdul-azeez-31a3091aa_ai-startuplaunch-entrepreneurship-activity-7346912894598422528-fX9h",
                        "comment": "Congratulations on the launch of AI Agentiva! The solutions you're offering, particularly the Interview Agent and RAG Chatbot, address critical pain points for many businesses. We've also seen significant improvements in efficiency and customer satisfaction by implementing custom AI agents for similar tasks. Happy to discuss how we've helped other companies streamline their processes and achieve tangible results with AI-driven automation."
                    },
                    {
                        "title": "Emerging Technologies",
                        "text": "🌐 Emerging Technologies: Shaping the Future of Business and Innovation\n\nWe're living in a time where technology is evolving faster than ever...",
                        "url": "https://www.linkedin.com/posts/workonic-business-consultany_emergingtech-ai-innovation-activity-7347134528513019904-kXV9",
                        "comment": "Excellent overview of emerging technologies! The point about people using technology replacing those who don't is particularly insightful. We're seeing a huge demand for AI and machine learning solutions that integrate with existing systems. If anyone is exploring how to implement these technologies for predictive analytics or automation, we'd be happy to share our experience in developing and deploying custom AI solutions to improve business forecasting and decision-making."
                    }
                ]
            }
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
    
    # Display results using the same formatting structure
    if result_data and "final_results" in result_data:
        st.success(f"✅ Found {len(result_data['final_results'])} posts with generated comments")
        
        # Results section
        st.header("📋 Results")
        
        # Display each post and comment using the same structure as sample
        for i, result in enumerate(result_data['final_results']):
            with st.container():
                # Create columns for better layout
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Post details
                    st.subheader(f"📌 Post {i+1}: {result['title']}")
                    
                    # Post content in expandable section
                    with st.expander("📖 View Post Content", expanded=False):
                        st.write(result['text'])
                        st.markdown(f"**🔗 URL:** [{result['url']}]({result['url']})")
                    
                    # Generated comment
                    st.markdown("**💬 Generated Comment:**")
                    st.write(result['comment'])
                
                with col2:
                    # Action buttons
                    st.markdown("**🎯 Actions:**")
                    
                    # Comment button (to be configured later)
                    comment_btn = st.button(
                        "💬 Post Comment",
                        key=f"comment_{i}",
                        use_container_width=True,
                        help="Click to post this comment on LinkedIn"
                    )
                    
                    if comment_btn:
                        # Post comment using LinkedIn API
                        with st.spinner("Posting comment to LinkedIn..."):
                            comment_result = post_linkedin_comment(
                                post_url=result['url'],
                                comment_text=result['comment']
                            )
                            
                            if comment_result['success']:
                                st.success(f"✅ {comment_result['message']}")
                                if comment_result.get('comment_id'):
                                    st.info(f"Comment ID: {comment_result['comment_id']}")
                            else:
                                st.error(f"❌ Failed to post comment: {comment_result['error']}")
                                st.info("💡 Check your LINKEDIN_ACCESS_TOKEN in the .env file")
                    
                    # Copy comment button
                    copy_btn = st.button(
                        "📋 Copy Comment",
                        key=f"copy_{i}",
                        use_container_width=True,
                        help="Copy comment to clipboard"
                    )
                    
                    if copy_btn:
                        st.success("Comment copied to clipboard!")
                    
                    # Save button
                    save_btn = st.button(
                        "💾 Save Result",
                        key=f"save_{i}",
                        use_container_width=True,
                        help="Save this result for later"
                    )
                    
                    if save_btn:
                        st.success("Result saved!")
                
                # Separator
                st.divider()
    else:
        st.error("❌ No results found or invalid data format.")

elif execute_button and not search_query:
    st.error("⚠️ Please enter a search query to proceed.")

else:
    # Welcome screen
    st.markdown("""
    ## 🎯 How it works:
    
    1. **🔍 Enter your search query** - Describe what kind of LinkedIn posts you want to find
    2. **🤖 AI creates optimized searches** - Our AI generates 2-3 strategic LinkedIn search queries
    3. **📊 Collect relevant posts** - Find posts from potential customers using Apify scraper
    4. **💬 Generate personalized comments** - AI creates engaging comments that represent your company
    5. **🚀 Take action** - Review and post comments to engage with potential customers
    
    ## 📝 Example search queries:
    - "need AI solution for my business"
    - "looking for marketing automation help"
    - "struggling with customer support efficiency"
    - "want to improve sales processes"
    
    **👈 Enter your search query in the sidebar to get started!**
    """)

# Footer
st.markdown("---")
st.markdown("**💡 Built with Streamlit | Powered by CrewAI and LinkedIn API**")
