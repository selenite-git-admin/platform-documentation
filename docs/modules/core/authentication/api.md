# Authentication – API

### Token
**Method**: `POST`  
**Path**: `/auth/token`  
**Purpose**: Exchange code or client credentials for tokens

**Request**
```json
{
  "grant_type": "authorization_code",
  "code": "..."
}
```

**Response**
```json
{
  "access_token": "...",
  "expires_in": 3600
}
```

