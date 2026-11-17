"""Small helper to log in to an APIC and run GET queries."""
import os
import sys

import requests
import urllib3


class Apic:
    def __init__(self, url=None, user=None, password=None, verify=None):
        self.url = (url or os.environ.get("APIC_URL", "")).rstrip("/")
        self.user = user or os.environ.get("APIC_USER")
        self.password = password or os.environ.get("APIC_PASS")
        if verify is None:
            verify = os.environ.get("APIC_VERIFY_SSL", "true").lower() != "false"
        self.verify = verify
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if not (self.url and self.user and self.password):
            sys.exit("Set APIC_URL, APIC_USER and APIC_PASS environment variables first.")
        self.s = requests.Session()
        self.login()

    def login(self):
        body = {"aaaUser": {"attributes": {"name": self.user, "pwd": self.password}}}
        r = self.s.post(f"{self.url}/api/aaaLogin.json", json=body, verify=self.verify, timeout=30)
        if r.status_code != 200:
            sys.exit(f"Login failed ({r.status_code}): {r.text[:200]}")

    def get(self, path):
        """GET an API path like '/api/class/fvTenant.json?...' and return the imdata list."""
        r = self.s.get(f"{self.url}{path}", verify=self.verify, timeout=60)
        if r.status_code == 403:  # token expired -> log in again once
            self.login()
            r = self.s.get(f"{self.url}{path}", verify=self.verify, timeout=60)
        r.raise_for_status()
        return r.json().get("imdata", [])


def attrs(mo):
    """Return the attributes dict of a managed object, whatever its class."""
    return next(iter(mo.values()))["attributes"]


def children(mo):
    return next(iter(mo.values())).get("children", [])
