import asyncio
import json
import datetime
import random

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

EVENT_HUB_CONNECTION_STR = "[EVENT_HUB_CONNECTION_STR]"
EVENT_HUB_NAME = "[EVENT_HUB_NAME]"

async def run():

    while True:
        # await asyncio.sleep(1)
        # Create a producer client to send messages to the event hub.
        # Specify a connection string to your event hubs namespace and
        # the event hub name.
        producer = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
        )
        async with producer:
            # Create a batch.
            event_data_batch = await producer.create_batch()
            
            sample_data = {
                "id": random.randint(0, 2),
                "timestamp": str(datetime.datetime.utcnow()),
                "value01": random.randint(1,5),
                "value02": random.randint(70, 100),
                "value03": random.randint(70, 100),
            }
            
            s = json.dumps(sample_data, ensure_ascii=False)
            # Add events to the batch.
            event_data_batch.add(EventData(s))

            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)
            print("Sending Data:", s)
# End of Function

loop = asyncio.get_event_loop()

try:
    print("-- Start --")
    asyncio.run(run())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("-- Close --")
    loop.close()
