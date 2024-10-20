# Data Analysis

From the `audio-features` endpoint at Spotify, we return the following schema
of data:

```python
class TrackFeatures(BaseModel):
    """Track features for analysis."""

    id: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int # Modality - 0 for minor, 1 for major
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    time_signature: int
```

The `id` field is the `spotify_id` of the track.

An ongoing question is what fields are relevant to the user and how we can
use these attributes to provide value to the user as it pertains to
organizing their music.

Note: the pydantic models are used to clean and validate data before it is
saved to the database.

See [computation](./computation.md) for more information on how the data will be
analyzed and presented.
