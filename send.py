import sys
import logging
import datetime
import time
import os

from azure.eventhub import EventHubClient, Sender, EventData

logger = logging.getLogger("azure")

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@brewdata.servicebus.windows.net.servicebus.windows.net/eventhub"
# "amqps://brewdata.servicebus.windows.net.servicebus.windows.net/brewpi-event-hub"
# SAS policy and key are not required if they are encoded in the URL

ADDRESS = "amqps://brewdata.servicebus.windows.net.servicebus.windows.net/brewpi-event-hub"
USER = "RootManageSharedAccessPolicy"
KEY = "QWFhcpuEc4MN0A0qvWYUSXzfBL/Mpm+6Ka+HUNSHHHc="

try:
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")

    # Create Event Hubs client
    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    sender = client.add_sender(partition="0")
    client.run()
    try:
        start_time = time.time()
        for i in range(100):
            print("Sending message: {}".format(i))
            message = "Message {}".format(i)
            sender.send(EventData(message))
    except:
        raise
    finally:
        end_time = time.time()
        client.stop()
        run_time = end_time - start_time
        logger.info("Runtime: {} seconds".format(run_time))

except KeyboardInterrupt:
    pass