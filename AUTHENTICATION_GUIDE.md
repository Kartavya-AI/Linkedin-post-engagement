# LinkedIn Authentication Setup

This guide explains how to set up and use the LinkedIn authentication system with Streamlit UI.

## Overview

The authentication process has been separated from the CrewAI workflow:
1. **Streamlit Auth App**: Handles LinkedIn OAuth authentication
2. **CrewAI Crew**: Uses the access token for LinkedIn API operations

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the project root with your LinkedIn API credentials:

```env
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:8501
GEMINI_API_KEY=your_gemini_api_key
```

**Note**: The `LINKEDIN_REDIRECT_URI` should match exactly what you configure in your LinkedIn Developer App.

### 2. LinkedIn App Configuration

**Important**: The redirect URI must match exactly in your LinkedIn Developer App.

In your LinkedIn Developer App settings:

- Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
- Select your application
- Navigate to the **"Auth"** tab
- Under **"Redirect URLs"**, add: `http://localhost:8501`
- Ensure the following permissions are enabled:
  - `r_liteprofile` (Read basic profile)
  - `r_emailaddress` (Read email address)
  - `w_member_social` (Share content)
- Save your changes

**Common Redirect URI Options:**
- `http://localhost:8501` (Streamlit default)
- `http://localhost:8000/callback` (Alternative)
- `http://127.0.0.1:8501` (Localhost alternative)

Choose one and use it consistently in both your LinkedIn app and `.env` file.

### 3. Install Dependencies

```bash
# Install Streamlit dependencies
pip install -r requirements-auth.txt

# Install CrewAI dependencies (if not already installed)
pip install -r requirements.txt
```

## Usage Instructions

### Step 1: Run the Authentication App

```bash
cd src/crew
streamlit run auth_app.py
```

This will open the Streamlit authentication app at `http://localhost:8501`

### Step 2: Complete LinkedIn Authentication

1. Click **"Generate LinkedIn Auth URL"** in the Streamlit app
2. Click the authorization link to go to LinkedIn
3. Complete the LinkedIn OAuth flow
4. You'll be redirected back to the Streamlit app
5. **Copy the access token** displayed in the app

### Step 3: Run the CrewAI Workflow

```bash
cd src/crew
python main.py
```

When prompted:
1. **Paste the access token** from the Streamlit app
2. **Enter your search query** for LinkedIn prospecting

## Process Flow

```
1. Streamlit App (auth_app.py)
   ↓
2. LinkedIn OAuth Authentication
   ↓
3. Access Token Generated
   ↓
4. Copy Token to CrewAI
   ↓
5. Run LinkedIn Automation (main.py)
```

## Features

### Authentication App Features
- ✅ OAuth2 authorization URL generation
- ✅ Automatic token exchange
- ✅ Profile verification
- ✅ Token display and copy functionality
- ✅ Clean, user-friendly interface

### CrewAI Workflow Features
- ✅ Customer-focused search strategy generation
- ✅ LinkedIn people and content discovery
- ✅ Engagement strategy development
- ✅ Professional comment suggestions
- ✅ Comprehensive reporting

## Troubleshooting

### Common Issues

1. **"The redirect_uri does not match the registered value"**
   - Check that your LinkedIn app redirect URL exactly matches your `.env` file
   - Common mismatches: `http` vs `https`, `localhost` vs `127.0.0.1`, missing/extra ports
   - Solution: Use the manual code entry option in the Streamlit app

2. **"LinkedIn Client ID not found"**
   - Ensure your `.env` file has the correct `LINKEDIN_CLIENT_ID`

3. **"Failed to get access token"**
   - Verify your `LINKEDIN_CLIENT_SECRET` is correct
   - Check that the authorization code hasn't expired (use it quickly)

4. **"Insufficient permissions"**
   - Ensure your LinkedIn app has the required scopes enabled
   - Re-authenticate if permissions were recently changed

5. **Streamlit not accessible**
   - Make sure Streamlit is running on the correct port
   - Try using `127.0.0.1:8501` instead of `localhost:8501`

### Manual Code Entry Workaround

If the automatic redirect doesn't work:

1. In the Streamlit app, expand **"Troubleshooting - Manual Code Entry"**
2. Copy the authorization URL and open it manually in your browser
3. Complete the LinkedIn authorization
4. From the redirect URL, copy the `code` parameter
5. Paste it into the "Authorization Code" field in the Streamlit app
6. Click "Exchange Code for Token"

### Security Notes

- ✅ Access tokens are not stored permanently
- ✅ OAuth state parameter prevents CSRF attacks
- ✅ Tokens are only passed between local applications
- ⚠️ Do not share access tokens publicly
- ⚠️ Tokens expire and need to be refreshed periodically

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    LinkedIn      │    │    CrewAI       │
│   Auth App      │◄──►│      API         │    │     Crew        │
│  (auth_app.py)  │    │   (OAuth2)       │    │  (main.py)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                                               ▲
         │            Access Token                       │
         └───────────────────────────────────────────────┘
```

This separation ensures:
- Clean authentication flow
- Secure token handling
- Modular architecture
- Easy debugging and maintenance
