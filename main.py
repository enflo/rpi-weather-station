from src.air_quality import AirQualityMonitor


if __name__ == "__main__":
    air_quality = AirQualityMonitor().get_measurement()
    print(air_quality)
