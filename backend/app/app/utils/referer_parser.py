"""
This module is copied from
https://github.com/snowplow-referer-parser/python-referer-parser
(last updated 5 years ago)

It's copied so we can use a newer version of the referer config

The new data is part of another repo and updated more frequently:

https://github.com/snowplow/referer-parser
"""


import os
import json

from urllib.parse import urlparse, parse_qsl


def load_referers(json_file):
    referers_dict = {}
    with open(json_file) as json_content:
        for medium, conf_list in json.load(json_content).items():
            for referer_name, config in conf_list.items():
                params = None
                if "parameters" in config:
                    params = list(map(str.lower, config["parameters"]))
                for domain in config["domains"]:
                    referers_dict[domain] = {"name": referer_name, "medium": medium}
                    if params is not None:
                        referers_dict[domain]["params"] = params
    return referers_dict


JSON_FILE = os.path.join(os.path.dirname(__file__), "data", "referers.json")
REFERERS = load_referers(JSON_FILE)


class Referer(object):
    def __init__(self, ref_url, curr_url=None, referers=REFERERS):
        self.known = False
        self.referer = None
        self.medium = "unknown"
        self.search_parameter = None
        self.search_term = None
        self.referers = referers

        ref_uri = urlparse(ref_url)
        ref_host = ref_uri.hostname
        self.known = ref_uri.scheme in {"http", "https"} and ref_host is not None
        self.uri = ref_uri

        if not self.known:
            return

        if curr_url:
            curr_uri = urlparse(curr_url)
            curr_host = curr_uri.hostname
            if curr_host == ref_host:
                self.medium = "internal"
                return

        referer = self._lookup_referer(ref_host, ref_uri.path, True)
        if not referer:
            referer = self._lookup_referer(ref_host, ref_uri.path, False)
            if not referer:
                self.medium = "unknown"
                return

        self.referer = referer["name"]
        self.medium = referer["medium"]

        if referer["medium"] == "search":
            if "params" not in referer or not referer["params"]:
                return
            for param, val in parse_qsl(ref_uri.query):
                if param.lower() in referer["params"]:
                    self.search_parameter = param
                    self.search_term = val

    def _lookup_referer(self, ref_host, ref_path, include_path):
        referer = None
        try:
            if include_path:
                referer = self.referers[ref_host + ref_path]
            else:
                referer = self.referers[ref_host]
        except KeyError:
            if include_path:
                path_parts = ref_path.split("/")
                if len(path_parts) > 1:
                    try:
                        referer = self.referers[ref_host + "/" + path_parts[1]]
                    except KeyError:
                        pass
        if not referer:
            try:
                idx = ref_host.index(".")
                return self._lookup_referer(ref_host[idx + 1 :], ref_path, include_path)
            except ValueError:
                return None
        else:
            return referer
