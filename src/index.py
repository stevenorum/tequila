import boto3
import json
import traceback

import ses_stuff

RECORD_HANDLERS = {
    "aws:ses":ses_stuff.process_ses_record
}

def handler(event, context):
    for record in event["Records"]:
        try:
            evt_src = record["eventSource"] # e.g., aws:ses
            src = evt_src.split(":")[-1] # e.g., ses
            RECORD_HANDLERS[evt_src](record[src])
        except:
            traceback.print_exc()
