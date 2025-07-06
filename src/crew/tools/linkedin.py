import requests
from crewai.tools import tool
import json
import time
import os
from typing import Dict, Any
from dotenv import load_dotenv
from apify_client import ApifyClient
from linkedin_api.clients.restli.client import RestliClient
from linkedin_api.clients.restli.client import RestliClient

# Load environment variables
load_dotenv()

# LinkedIn API access token
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')

# Apify configuration
APIFY_TOKEN = os.getenv('APIFY_TOKEN')

def get_linkedin_cookies():
    """
    Returns LinkedIn cookies for authenticated scraping via Apify.
    These cookies can be extracted from your browser and stored here or in environment variables.
    """
    return [
        {
            "domain": ".linkedin.com",
            "expirationDate": 1767199520,
            "hostOnly": False,
            "httpOnly": False,
            "name": "mbox",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "PC#ff1a126579d545ef996e1e4debbe4880.41_0#1767199520|session#457e76fd84fb417eb8c58bfbccd0959d#1751649380"
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1754113946.018943,
            "hostOnly": False,
            "httpOnly": False,
            "name": "lms_ads",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQGVr9xf_cNU0AAAAZfO2B2xNQacKdHmXpV1h_ir32orA6i_h_7cDlcld6SDbLjElisMRei12xMYffNbb7GTZoI9EkqWDUDA"
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1753504726.309129,
            "hostOnly": False,
            "httpOnly": False,
            "name": "_guid",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "089c2710-d924-4035-ad4c-cae5c5bee4e2"
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1783215476.760603,
            "hostOnly": False,
            "httpOnly": False,
            "name": "bcookie",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "\"v=2&baf59559-2d81-456e-8852-9b6f8efbbcaa\""
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1754113946.019016,
            "hostOnly": False,
            "httpOnly": False,
            "name": "lms_analytics",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQGVr9xf_cNU0AAAAZfO2B2xNQacKdHmXpV1h_ir32orA6i_h_7cDlcld6SDbLjElisMRei12xMYffNbb7GTZoI9EkqWDUDA"
        },
        {
            "domain": ".linkedin.com",
            "hostOnly": False,
            "httpOnly": True,
            "name": "fptctx2",
            "path": "/",
            "sameSite": None,
            "secure": True,
            "session": True,
            "storeId": None,
            "value": "taBcrIH61PuCVH7eNCyH0J9Fjk1kZEyRnBbpUW3FKs9yQiUw6cQ%252bCHQKH3IoZ6Y3Urvyxa8MWRdlgominv8jd9ABnyz8LaPXKcRor1VDhOO%252f3AJ2QqXoM0r37smgdMMRD4uQbB9mawrQd9qyOEDmSRZXT%252fEdsfVas%252f1qz9FQl6T35R2txOxuQ4eLJGH5qtdS962ug%252fJOTrX0LmsPo0iGzKQjdc%252bOUmZ7zGt%252bYEmBqNytZqpZfkwCArEvX6%252b9jZcoyRyGPruSYH7nBAVLqfBHdDg21VTv%252fQexo4jUxFAbexUDtN3vdt9ARAjfra2wAmip4%252fXN5Ml6AboUYdMBaBJwazeA1qTAHgv1Rm8pfYrFG78%253d"
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1782755662.253399,
            "hostOnly": False,
            "httpOnly": True,
            "name": "li_at",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQEDATrU0OEEoRolAAABlnWKWBkAAAGX4OAVck0AjSBBpwfWBsjbtweUADoxCHqpE-t-rNQT900Oflbrkmyx1Hb8U00keCItbOHHA3oQB5SiZOhaSCMcO_CFuNnaHspRJOQ12rnvZxvDV8JYvMv1vZgA"
        },
        {
            "domain": ".linkedin.com",
            "hostOnly": False,
            "httpOnly": False,
            "name": "lang",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": True,
            "storeId": None,
            "value": "v=2&lang=en-us"
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1751724187.115677,
            "hostOnly": False,
            "httpOnly": False,
            "name": "lidc",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "\"b=OB33:s=O:r=O:a=O:p=O:g=4485:u=1199:x=1:i=1751679480:t=1751724190:v=2:sig=AQGwqLzkqL-rPQLP1cKcZRdPMR_vTfvY\""
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1754113945.755416,
            "hostOnly": False,
            "httpOnly": False,
            "name": "AnalyticsSyncHistory",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQIqBd-N4JISJgAAAZfO2Bx4NrTgGWuikaLuqynZA1vq11GUmGap1CO2iPjIUaOdSzv0dVAbkxK4ZAku1X5n_w"
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1783182281.202499,
            "hostOnly": False,
            "httpOnly": True,
            "name": "bscookie",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "\"v=1&20240323030151294c905c-ca8c-48e6-8c06-58822212109bAQHTLXiG2JiNVEzZq3T7FUHIHc329Qam\""
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1777264727.296502,
            "hostOnly": False,
            "httpOnly": True,
            "name": "dfpfpt",
            "path": "/",
            "sameSite": None,
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "c8859c4121ad44c8965a40359708f7c3"
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1782755662.253599,
            "hostOnly": False,
            "httpOnly": False,
            "name": "JSESSIONID",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "\"ajax:2158373929648771278\""
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1777264723.11824,
            "hostOnly": False,
            "httpOnly": True,
            "name": "li_rm",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQE9LRj13htXngAAAY7d4cQm1NNMZR9LgVXujVuTdBtM2YoK33GF6G3djpEJzxye-GWqUe-h_8mXja3qbBsiU4pjh7uXtgm5v7M-aHb3oWCi1XDTcGkwxew0"
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1759455476.760445,
            "hostOnly": False,
            "httpOnly": False,
            "name": "li_sugr",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "512c2960-44a1-40c1-a356-d0192382859b"
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1767231472,
            "hostOnly": False,
            "httpOnly": False,
            "name": "li_theme",
            "path": "/",
            "sameSite": None,
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "light"
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1767231472,
            "hostOnly": False,
            "httpOnly": False,
            "name": "li_theme_set",
            "path": "/",
            "sameSite": None,
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "app"
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1782755662.25355,
            "hostOnly": False,
            "httpOnly": False,
            "name": "liap",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "true"
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1752889072,
            "hostOnly": False,
            "httpOnly": False,
            "name": "timezone",
            "path": "/",
            "sameSite": None,
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "Asia/Calcutta"
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1754271476,
            "hostOnly": False,
            "httpOnly": False,
            "name": "UserMatchHistory",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQLb0m-tI21x1gAAAZfYO61OX0LaQq0oByRDlEoppxtIFa7R3J8gftIRfLh7Xcz10foTMedegMrzxXCHP4zYIVd4m5yT4AH5PkwIuwK5a8mKs16amVrrFCbQY1E3uj_IhH2YG9daJNXbsKB98KaWI-YY6AkjdtAL1hlfwEqqU-1q72KZ9IlhDWRJ2hnKpNsvsIzj1F-JbqHF_WIwoOdO8kCiGit5B8mtNd_gUE_Vv9NVCOcSQ_G8_q1WHyhCVJFec1gdddXwk9U2nWd1zoaB5qhob4eFkwmwtMeACFv65ON9GtVV-C0bi3gw2ZgXsLlfQMa7wl3Q4Be9GYEu_4-yFrdREPZe0b8VfaLnaTM4_fAVA2tXWQ"
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1771697202.050426,
            "hostOnly": False,
            "httpOnly": False,
            "name": "visit",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "v=1&M"
        }
    ]

@tool("linkedin_get_profile")
def linkedin_get_profile() -> Dict[str, Any]:
    """
    Get LinkedIn profile information using RestliClient with access token from environment.
    
    Returns:
        Dict[str, Any]: Profile information
    """
    
    if not LINKEDIN_ACCESS_TOKEN:
        return {
            "success": False,
            "error": "LinkedIn access token not found in environment variables",
            "valid_token": False
        }
    
    try:
        # Initialize RestliClient
        restli_client = RestliClient()
        
        # Get profile data using RestliClient
        response = restli_client.get(
            resource_path="/userinfo",
            access_token=LINKEDIN_ACCESS_TOKEN
        )
        
        if response:
            return {
                "success": True,
                "profile": response,
                "valid_token": True
            }
        else:
            return {
                "success": False,
                "error": "Failed to get profile data",
                "valid_token": False
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error getting profile: {str(e)}",
            "valid_token": False
        }



@tool("linkedin_get_posts")
def linkedin_get_posts(search_queries: str, limit: int = 10) -> Dict[str, Any]:
    """
    Get LinkedIn posts using Apify scraper with search queries.
    
    Args:
        search_queries (str): Search queries to find relevant posts
        limit (int): Number of posts to return (default: 10)
    
    Returns:
        Dict[str, Any]: Posts data from Apify scraper
    """
    
    if not APIFY_TOKEN:
        return {
            "success": False,
            "error": "Apify token not found in environment variables",
            "results": [],
            "count": 0
        }
    
    try:
        # Initialize the ApifyClient with your API token
        client = ApifyClient(APIFY_TOKEN)

        # Prepare the Actor input
        run_input = {
            "urls": [
                f"https://www.linkedin.com/search/results/content/?datePosted=%22past-24h%22&keywords={search_queries}&origin=FACETED_SEARCH",
            ],
            "deepScrape": True,
            "rawData": False,
            "minDelay": 2,
            "maxDelay": 8,
            "limitPerSource": limit,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyCountry": "US",
            },
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "cookie": get_linkedin_cookies()
        }

        # Run the Actor and wait for it to finish
        run = client.actor("kfiWbq3boy3dWKbiL").call(run_input=run_input)

        # Fetch and print Actor results from the run's dataset (if there are any)
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append({
                "title": item.get("title", ""),
                "text": item.get("text", ""),
                "url": item.get("url", ""),
                "author": item.get("author", ""),
                "date": item.get("date", ""),
            })
        return {
            "success": True,
            "search_queries": search_queries,
            "results": results,
            "count": len(results),
            "limit": limit,
            "source": "apify_scraper"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error running Apify scraper: {str(e)}",
            "results": [],
            "count": 0
        }


@tool("linkedin_share_post")
def linkedin_share_post(post_text: str, visibility: str = "PUBLIC") -> Dict[str, Any]:
    """
    Share a post on LinkedIn.
    
    Args:
        post_text (str): Text content of the post
        visibility (str): Post visibility - "PUBLIC" or "CONNECTIONS" (default: "PUBLIC")
    
    Returns:
        Dict[str, Any]: Response containing post sharing status
    """
    
    if not LINKEDIN_ACCESS_TOKEN:
        return {
            "success": False,
            "error": "LinkedIn access token not found in environment variables",
            "post_id": None
        }
    
    share_url = "https://api.linkedin.com/v2/shares"
    
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    share_data = {
        "owner": "urn:li:person:~",
        "text": {
            "text": post_text
        },
        "distribution": {
            "linkedInDistributionTarget": {
                "visibleToGuest": visibility == "PUBLIC"
            }
        }
    }
    
    try:
        response = requests.post(share_url, json=share_data, headers=headers)
        
        if response.status_code == 201:
            post_data = response.json()
            
            return {
                "success": True,
                "message": "Post shared successfully",
                "post_id": post_data.get("id"),
                "post_text": post_text,
                "visibility": visibility
            }
        
        elif response.status_code == 401:
            return {
                "success": False,
                "error": "Access token expired or invalid",
                "post_id": None
            }
        
        elif response.status_code == 403:
            return {
                "success": False,
                "error": "Insufficient permissions to share posts",
                "post_id": None
            }
        
        else:
            return {
                "success": False,
                "error": f"Failed to share post. Status: {response.status_code}",
                "response": response.text[:200],
                "post_id": None
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Error sharing post: {str(e)}",
            "post_id": None
        }

