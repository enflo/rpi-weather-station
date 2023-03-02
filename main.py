from src.air_quality import AirQuality


if __name__ == "__main__":
    air_quality = AirQuality().get_measurement()
    print(air_quality)