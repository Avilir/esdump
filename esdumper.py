#!/usr/bin/env python3
"""
Deploying en Elasticsearch server for collecting logs from ripsaw benchmarks

"""
import os
import logging
import tempfile
import urllib
import urllib.error
import base64
import signal
import subprocess
import time

from elasticsearch import Elasticsearch, exceptions as esexp

log = logging.getLogger(__name__)


class ElasticSearch(object):
    """
    ElasticSearch Environment
    """

    def __init__(self, ip, port):
        """
        Initializer function

        """
        log.info("Initializing the Elastic-Search environment object")

        self.ip = ip
        self.port = port
        # Connect to the server
        self.con = self._es_connect()

    def _es_connect(self):
        """
        Create a connection to the ES via the localhost port-fwd

        Returns:
            Elasticsearch: elasticsearch connection object

        Raise:
            ConnectionError: if can not connect to the server

        """
        try:
            es = Elasticsearch([{"host": self.ip, "port": self.port}])
        except esexp.ConnectionError:
            log.error("Can not connect to ES server in the LocalServer")
            raise
        return es

    def get_indices(self):
        """
        Getting list of all indices in the ES server - all created by the test,
        the installation of the ES was without any indexes pre-installed.

        Returns:
            list : list of all indices defined in the ES server

        """
        results = []
        log.info("Getting all indices")
        for ind in self.con.indices.get_alias("*"):
            results.append(ind)
        return results

    def _copy(self, es):
        """
        Copy All data from the internal ES server to the main ES

        Args:
            es (obj): elasticsearch object which connected to the main ES

        """

        query = {"size": 1000, "query": {"match_all": {}}}
        for ind in self.get_indices():
            log.info(f"Reading {ind} from internal ES server")
            try:
                result = self.con.search(index=ind, body=query)
            except esexp.NotFoundError:
                log.warning(f"{ind} Not found in the Internal ES.")
                continue

            log.debug(f"The results from internal ES for {ind} are :{result}")
            log.info(f"Writing {ind} into main ES server")
            for doc in result["hits"]["hits"]:
                log.debug(f"Going to write : {doc}")
                es.index(index=ind, doc_type="_doc", body=doc["_source"])

if __name__ == "__main__":
    es = ElasticSearch(ip="10.0.144.152", port="9200")
    print(es.get_indices())

