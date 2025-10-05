import requests
from functools import lru_cache

CAT_API_BREEDS_URL = "https://api.thecatapi.com/v1/breeds"

class CatAPIError(Exception):
    pass

@lru_cache(maxsize=1)
def get_all_breeds():
    """
    Fetches the list of all cat breeds from TheCatAPI.
    Caches the result in memory to reduce API calls.
    Returns list of breed names in lowercase.
    Raises CatAPIError if API call fails.
    """
    try:
        response = requests.get(CAT_API_BREEDS_URL, timeout=5)
        response.raise_for_status()
        breeds = [b.get("name", "").lower() for b in response.json()]
        return breeds
    except Exception as e:
        raise CatAPIError(f"Could not fetch cat breeds: {str(e)}") from e
