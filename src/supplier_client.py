#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""供应链平台供应商侧最小调用客户端。"""
import hashlib
import json
import time
import urllib.parse
import urllib.request

BASE_URL = "https://open.17usoft.com/supply/v2"
SANDBOX_URL = "https://open-sandbox.17usoft.com/supply/v2"
PAGE_SIZE = 200
TIMEOUT = 10


def sign(params, secret):
    items = sorted((k, v) for k, v in params.items() if v not in (None, ""))
    raw = "&".join("%s=%s" % (k, v) for k, v in items) + "&secret=" + secret
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class SupplierClient(object):
    def __init__(self, app_key, app_secret, sandbox=False):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base = SANDBOX_URL if sandbox else BASE_URL

    def _get(self, path, params):
        params = dict(params)
        params["ts"] = int(time.time())
        headers = {
            "X-App-Key": self.app_key,
            "X-Timestamp": str(params["ts"]),
            "X-Sign": sign(params, self.app_secret),
        }
        url = "%s%s?%s" % (self.base, path, urllib.parse.urlencode(params))
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.load(r)

    def pull_orders(self, date, page=1):
        body = self._get("/orders", {"date": date, "page": page, "size": PAGE_SIZE})
        return body.get("data", [])

    def ship(self, order_no, carrier, tracking_no):
        payload = {"carrier": carrier, "tracking_no": tracking_no,
                   "shipped_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        params = {"order_no": order_no, "body": json.dumps(payload)}
        params["ts"] = int(time.time())
        url = "%s/orders/%s/shipment" % (self.base, order_no)
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                     headers={"X-App-Key": self.app_key,
                                              "X-Sign": sign(params, self.app_secret),
                                              "Content-Type": "application/json"},
                                     method="POST")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.load(r)
