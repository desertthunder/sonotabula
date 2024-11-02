# Authentication Flow

Spotify's API implements the OAuth2 delegated authority flow. When the user
grants the application access, they're brought back to the app and the token is
stored and then encoded as a JWT. The JWT is stored in the React app's state.

## Implementation

### **Sign-up**: Client side route at `/signup`

- The sign-up button sends an empty `POST` request to the server at `/api/signup/`
    - The server redirects the user to the Spotify Authorization page.
    - The user logs in to spotify and authorizes the application.
        - In local development, the redirect uri is `http://localhost:8000/api/spotify_cb`
    - With the authorization code, the server requests an access token from Spotify.
    - Then the server creates a new user with the access token and refresh token,
    and the user's spotify id and email address.

### **Login**: Client side route at `/login`

- The login button sends an empty `PUT` request to the server at `/api/login/`
- Upon receiving the authorization code, the server requests an access token
from Spotify and fetches the user's information from the API. It users the
user's spotify id and email address to find the user in the database.
- After the user logs in, the user is redirected to the dashboard with a JWT token.
    - Client side route at `/dashboard?token=<JWT_TOKEN>`
    - The JWT token is stored in the browser's local storage.
    - The token is used to authenticate the user for all requests to the server
    with `simple-jwt`.

## Profile Endpoints

### Example - Current User (`/me`)

```json
{
  "country": "string",
  "display_name": "string",
  "email": "string",
  "explicit_content": {
    "filter_enabled": false,
    "filter_locked": false
  },
  "external_urls": {
    "spotify": "string"
  },
  "followers": {
    "href": "string",
    "total": 0
  },
  "href": "string",
  "id": "string",
  "images": [
    {
      "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228",
      "height": 300,
      "width": 300
    }
  ],
  "product": "string",
  "type": "string",
  "uri": "string"
}
```
