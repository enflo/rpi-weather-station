# rpi-weather-station
RPI weather station

## Environment Variables

The following environment variables can be set in a `.env` file in the project root:

### General Configuration
- `ENVIRONMENT`: Set to "development" or "production" (default: "development")
- `LOOP_TIME`: Time in seconds between sensor readings (default: 1)

### API Configuration
- `API_ENABLE`: Enable/disable API integration (default: False)
- `API_METHOD`: HTTP method for API requests (default: "POST")
- `API_HOST`: API host URL (default: "localhost")
- `API_HEADER_TOKEN`: API header token for authentication (default: None)
- `API_URL_TOKEN`: API URL token (default: "")

### MQTT Configuration
- `MQTT_ENABLE`: Enable/disable MQTT integration (default: False)
- `MQTT_HOST`: MQTT broker host (default: "localhost")
- `MQTT_PORT`: MQTT broker port (default: 1883)
- `MQTT_TOPIC`: MQTT topic to publish to (default: "topic")
- `MQTT_USER`: MQTT username (default: "user")
- `MQTT_PASSWORD`: MQTT password (default: "password")

### SQS Configuration
- `SQS_ENABLE`: Enable/disable SQS integration (default: False)
- `SQS_URL`: SQS URL (default: "http://localhost:9324")
- `SQS_ACCESS_KEY`: SQS access key (default: "access_key")
- `SQS_SECRET_KEY`: SQS secret key (default: "secret_key")
- `SQS_QUEUE_NAME`: SQS queue name (default: "queue_name")
- `SQS_REGION`: SQS region (default: "fr-par")

### PostgreSQL Configuration
- `POSTGRES_ENABLE`: Enable/disable PostgreSQL integration (default: False)
- `POSTGRES_USER`: PostgreSQL username (default: "postgres")
- `POSTGRES_PASSWORD`: PostgreSQL password (default: "postgres")
- `POSTGRES_HOST`: PostgreSQL host (default: "localhost")
- `POSTGRES_PORT`: PostgreSQL port (default: "5432")
- `POSTGRES_DBNAME`: PostgreSQL database name (default: "postgres")
- `POSTGRES_TABLE`: PostgreSQL table name for storing data (default: "weather_data")
