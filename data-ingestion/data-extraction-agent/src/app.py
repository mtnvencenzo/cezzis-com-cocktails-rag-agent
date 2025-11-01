import atexit
import signal
import sys
from types import FrameType
from typing import Optional

# from app_settings import settings
from confluent_kafka import Consumer, KafkaError

from app_settings import settings

consumer: Consumer | None = None
shutdown_requested = False

def signal_handler(signum: int, _frame: Optional[FrameType]) -> None:
    """Handle shutdown signals gracefully.

    Args:
        signum (int): The signal number.
        _frame (Optional[FrameType]): The current stack frame (unused).
    """
    global shutdown_requested
    print(f"\nShutdown signal received ({signum}), exiting gracefully...")
    shutdown_requested = True

def main() -> None:
    """Main function to run the Kafka consumer."""
    global shutdown_requested

    # In main(), before the loop:
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting Kafka consumer")

    # Initialize the kafka consumer to read messages from 'cocktails-topic'
    # Registering atexit handler to ensure proper cleanup on exit
    print("Creating Kafka consumer")

    try:
        global consumer

        consumer = Consumer(
            {
                "bootstrap.servers": settings.bootstrap_servers,
                "group.id": settings.consumer_group,
                "auto.offset.reset": "earliest",
            }
        )

    except Exception as e:
        print(f"Error creating Kafka consumer: {e}")
        sys.exit(1)

    try:
        print(f"Subscribing to '{settings.topic_name}'")

        consumer.subscribe([settings.topic_name])

    except Exception as e:
        print(f"Error subscribing to topic: {e}")
        sys.exit(1)

    print("Polling for messages...")

    # Loop until the app is being shutdown
    while not shutdown_requested:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        elif msg.error():
            error = msg.error()
            if error is not None and error.code() == KafkaError._PARTITION_EOF:
                print(
                    "End of partition reached {0}/{1}".format(
                        msg.topic(), msg.partition()
                    )
                )
            else:
                print("Consumer error: {}".format(error))
            continue

        else:
            value = msg.value()

            if value is not None:
                print("Received message: {}".format(value.decode("utf-8")))
            else:
                print("Received message with no value")


def cleanup() -> None:
    """Cleanup function to close the Kafka consumer."""
    print("Performing cleanup before exit.")
    global consumer
    
    if consumer is not None:
        try:
            consumer.commit()
        except Exception as e:
            print(f"Error committing offsets: {e}")

        consumer.close()

if __name__ == "__main__":
    atexit.register(cleanup)
    main()
