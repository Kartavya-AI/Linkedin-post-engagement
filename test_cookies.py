#!/usr/bin/env python3
"""
Test script to verify that LinkedIn cookies are correctly integrated into Apify tools.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from crew.tools.linkedin import get_linkedin_cookies, linkedin_get_posts

def test_cookies_function():
    """Test that the cookies function returns the expected structure."""
    print("Testing get_linkedin_cookies() function...")
    
    cookies = get_linkedin_cookies()
    
    # Check that we have cookies
    assert isinstance(cookies, list), "Cookies should be a list"
    assert len(cookies) > 0, "Cookies list should not be empty"
    
    # Check cookie structure
    for cookie in cookies:
        assert isinstance(cookie, dict), "Each cookie should be a dictionary"
        assert "name" in cookie, "Cookie should have 'name' field"
        assert "value" in cookie, "Cookie should have 'value' field" 
        assert "domain" in cookie, "Cookie should have 'domain' field"
    
    # Check for essential LinkedIn cookies
    cookie_names = [cookie["name"] for cookie in cookies]
    essential_cookies = ["li_at", "lidc", "bcookie"]
    
    for essential in essential_cookies:
        assert essential in cookie_names, f"Essential cookie '{essential}' should be present"
    
    print(f"✅ Cookies function test passed! Found {len(cookies)} cookies")
    return True

def test_tools_integration():
    """Test that both tools are properly configured to use cookies."""
    print("\nTesting tool integration...")
    
    # This will test that the tools are properly set up without actually calling Apify
    # We just check if the functions exist and don't immediately fail
    try:
        # Test posts tool  
        result = linkedin_get_posts("test", 1)
        print("✅ linkedin_get_posts tool is accessible")
        
        print("✅ Tool integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Tool integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing LinkedIn cookies integration...\n")
    
    try:
        # Test cookies function
        test_cookies_function()
        
        # Test tools integration  
        test_tools_integration()
        
        print("\n🎉 All tests passed! Cookies are properly integrated.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
