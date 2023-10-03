ECHO OFF
SET your-client-id=%1
SET your-client-secret=%2
SHIFT
SHIFT
CURL -X POST "https://accounts.spotify.com/api/token" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=client_credentials&client_id=%your-client-id%&client_secret=%your-client-secret%"
PAUSE
