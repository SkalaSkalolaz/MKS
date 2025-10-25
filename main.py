import sys
import requests
from datetime import datetime
from typing import List, Tuple
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

API_PASS_URL = "http://api.open-notify.org/iss-pass.json"
API_NOW_URL = "http://api.open-notify.org/iss-now.json"


class ISSDataError(Exception):
    """Custom exception for ISS data retrieval errors."""
    pass


def get_iss_position_now() -> Tuple[float, float]:
    """
    Get current ISS position from the Open Notify API.

    :return: Tuple with latitude and longitude of the ISS
    :raises ISSDataError: If data could not be retrieved
    """
    try:
        response = requests.get(API_NOW_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        position = data["iss_position"]
        return float(position["latitude"]), float(position["longitude"])
    except (requests.RequestException, KeyError, ValueError) as e:
        raise ISSDataError(f"Failed to retrieve ISS position: {e}") from e


def get_iss_passes(lat: float, lon: float, n: int = 5) -> List[datetime]:
    """
    Get upcoming ISS passes for a given latitude and longitude.

    :param lat: Latitude of location
    :param lon: Longitude of location
    :param n: Number of passes to retrieve
    :return: List of datetimes when ISS will pass
    :raises ISSDataError: If data could not be retrieved
    """
    params = {"lat": lat, "lon": lon, "n": n}
    try:
        response = requests.get(API_PASS_URL, params=params, timeout=10)
        if response.status_code == 404:
            raise ISSDataError("ISS pass data not found. Check coordinates or API availability.")
        response.raise_for_status()
        data = response.json()
        if "response" not in data:
            raise ISSDataError("Unexpected API response format.")
        passes = [datetime.utcfromtimestamp(p["risetime"]) for p in data["response"]]
        return passes
    except (requests.RequestException, KeyError, ValueError) as e:
        raise ISSDataError(f"Failed to retrieve ISS passes: {e}") from e


def plot_iss_position(lat: float, lon: float) -> None:
    """
    Plot current ISS position on the world map.

    :param lat: Latitude of ISS
    :param lon: Longitude of ISS
    """
    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()
    ax.coastlines()
    ax.plot(lon, lat, marker="o", color="red", markersize=8, transform=ccrs.Geodetic())
    plt.title("Current ISS Position")
    plt.show()


def main() -> None:
    """
    Main function to run ISS tracker.
    """
    try:
        iss_lat, iss_lon = get_iss_position_now()
        print(f"Current ISS Position: Latitude {iss_lat}, Longitude {iss_lon}")

        passes = []
        try:
            passes = get_iss_passes(iss_lat, iss_lon)
            print("Upcoming ISS Passes UTC:")
            for p in passes:
                print(p.strftime("%Y-%m-%d %H:%M:%S"))
        except ISSDataError as pe:
            print(pe)
            print("Unable to get passes, proceeding with current position only.")

        plot_iss_position(iss_lat, iss_lon)

    except ISSDataError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()