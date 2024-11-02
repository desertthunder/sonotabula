# Data Analysis & Computation

## Data Model

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

## Analysis

Analysis in the context of the application isn't a true analysis of the data. It
is a persisted record of related objects and the data they contain. The `Analysis`
object stores the association between track features and the track itself, as well
as the overarching context of the collection (i.e., album, playlist, etc.).

## Computations

A `Computation` object is related to its `Analysis` object. It stores calculations
and statistics about the audio features of a collection's tracks. A collection can
be a single track, album, or playlist.

### Averages

Danceability
Energy
Loudness
Speechiness
Acousticness
Instrumentalness
Liveness
Valence
Tempo
Duration

### Max & Min

- All of the above, with particular importance given to:
    - Tempo (fastest & slowest)
    - Valence (happiest & saddest)
    - Duration (longest & shortest)

### Counts

Minor Key i.e., mode = 0
Major: mode = 1

## Challenges
