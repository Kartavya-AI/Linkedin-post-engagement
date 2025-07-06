import requests
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def post_linkedin_comment(post_url, comment_text, access_token=None):
    """
    Post a comment on a LinkedIn post using LinkedIn API with existing access token
    
    Args:
        post_url (str): The LinkedIn post URL
        comment_text (str): The comment text to post
        access_token (str): LinkedIn access token (optional, will use from env if not provided)
    
    Returns:
        dict: Response containing success status and details
    """
    
    if not access_token:
        access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    if not access_token:
        return {
            "success": False,
            "error": "LinkedIn access token not found in environment variables"
        }
    
    try:
        # Extract post URN from URL
        # LinkedIn post URLs are typically like:
        # https://www.linkedin.com/posts/username_activity-123456789-abcd
        if "/posts/" in post_url and "activity-" in post_url:
            # Extract activity ID from URL
            activity_id = post_url.split("activity-")[-1].split("-")[0]
            post_urn = f"urn:li:activity:{activity_id}"
        else:
            return {
                "success": False,
                "error": "Invalid LinkedIn post URL format. Expected format: .../posts/...activity-123456789-..."
            }
        
        # LinkedIn API endpoint for creating comments
        # Use the correct social actions endpoint
        comment_url = f"https://api.linkedin.com/v2/socialActions/{post_urn}/comments"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # Comment payload using current user as actor
        comment_data = {
            "actor": "urn:li:person:~",  # Current authenticated user
            "message": {
                "text": comment_text
            }
        }
        
        # Make the API request
        response = requests.post(comment_url, json=comment_data, headers=headers)
        
        if response.status_code == 201:
            return {
                "success": True,
                "message": "Comment posted successfully to LinkedIn!",
                "comment_id": response.headers.get("x-restli-id"),
                "status_code": response.status_code,
                "post_url": post_url
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "error": "Access token is invalid or expired. Please check your LINKEDIN_ACCESS_TOKEN in .env file.",
                "status_code": response.status_code
            }
        elif response.status_code == 403:
            return {
                "success": False,
                "error": "Insufficient permissions. Your access token may not have comment permissions.",
                "status_code": response.status_code
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "error": "Post not found or no longer available.",
                "status_code": response.status_code
            }
        else:
            return {
                "success": False,
                "error": f"Failed to post comment. LinkedIn API returned status: {response.status_code}",
                "response_text": response.text[:300] if response.text else "No response text",
                "status_code": response.status_code
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Network error while connecting to LinkedIn API: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

