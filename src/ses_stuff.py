#!/usr/bin/env python

import boto3
import os

MESSAGE_BUCKET = os.environ.get("MESSAGE_BUCKET")
INCOMING_PREFIX = os.environ.get("INCOMING_PREFIX")
FORWARD_TO = os.environ.get("FORWARD_TO")

HEADER_LINE_LENGTH = 990

ses = boto3.client("ses")
s3 = boto3.client("s3")

def get_email_body(message_id):
    return boto3.client("s3").get_object(Bucket=MESSAGE_BUCKET,Key=INCOMING_PREFIX + message_id)["Body"]

def strip_headers(message_body):
    buff = message_body.read(amt=4)
    while True:
        if buff.endswith("\n\n".encode("utf-8")):
            breaker = "\n"
            break
        elif buff.endswith("\r\n\r\n".encode("utf-8")):
            breaker = "\r\n"
            break
        else:
            buff = buff[1:] + message_body.read(amt=1)
    return breaker

def process_headers(headers, forward_from, forward_to):
    hdict = {h["name"]:h["value"] for h in headers}
    new_headers = []
    keys_seen = []
    for header in headers:
        keys_seen.append(header["name"])
        if header["name"] == "From":
            header["value"] = "{} <{}>".format(header["value"].replace('<', 'at ').replace('>', ''), forward_from)
        elif header["name"] == "To":
            header["value"] = forward_to
        elif header["name"] in ["Return-Path","Sender","Message-ID","DKIM-Signature"]:
            # Strip these headers
            continue
        new_headers.append(header)
    if "Reply-To" not in keys_seen:
        new_headers.append({"name":"Reply-To","value":hdict["From"]})
    if "From" not in keys_seen:
        new_headers.append({"name":"From","value":"{} <{}>".format("unknown", forward_from)})
    if "To" not in keys_seen:
        new_headers.append({"name":"To","value":forward_to})
    return new_headers

def format_header_line(name, value):
    indentlen = len(name) + 2
    indent = indentlen * " "
    line = name + ": " + value
    lines = []
    while len(line) > HEADER_LINE_LENGTH:
        index = line[:HEADER_LINE_LENGTH].rfind(" ")
        startindex = index + 1
        if index < indentlen:
            index = HEADER_LINE_LENGTH
            startindex = HEADER_LINE_LENGTH
        lines.append(line[:index])
        line = indent + line[startindex:]
    lines.append(line)
    return lines

def format_header_lines(headers):
    lines = []
    for header in headers:
        lines.extend(format_header_line(header["name"], header["value"]))
    return lines

def process_ses_record(ses_record):
    mail = ses_record["mail"]
    receipt = ses_record["receipt"]
    headers = process_headers(mail["headers"], receipt["recipients"][0], FORWARD_TO)
    header_lines = format_header_lines(headers)
    body = get_email_body(mail["messageId"])
    breaker = strip_headers(body)
    new_body = breaker.join(header_lines + ["",""]).encode("utf-8") + body.read()
    ses.send_raw_email(
        RawMessage={
            'Data': new_body
        }
    )
