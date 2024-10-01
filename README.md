# Spotify Dashboard

A spotify stats dashboard and playlist organizer built with Django + DRF,
Postgres, React & Tailwind.

## Back-end

This is a Django application that uses REST framework for serializing and
deserializing objects.

## Front-end

This dashboard is built using React & Tailwind.

## Documentation

### Authentication

**Sign-up**: Client side route at `/signup`

- The sign-up button sends an empty `POST` request to the server at `/api/signup/`
    - The server redirects the user to the Spotify Authorization page.
    - The user logs in to spotify and authorizes the application.
        - In local development, the redirect uri is `http://localhost:8000/api/spotify_cb`
    - With the authorization code, the server requests an access token from Spotify.
    - Then the server creates a new user with the access token and refresh token,
    and the user's spotify id and email address.

**Login**: Client side route at `/login`

- The login button sends an empty `PUT` request to the server at `/api/login/`
- Upon receiving the authorization code, the server requests an access token
from Spotify and fetches the user's information from the API. It users the
user's spotify id and email address to find the user in the database.
- After the user logs in, the user is redirected to the dashboard with a JWT token.
    - Client side route at `/dashboard?token=<JWT_TOKEN>`
    - The JWT token is stored in the browser's local storage.
    - The token is used to authenticate the user for all requests to the server
    with `simple-jwt`.
