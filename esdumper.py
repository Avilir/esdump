#!/usr/bin/env python3
"""
Dumping ALL data from the elastic-search server as json files and create an
archive file from all the files

"""

import os
import os.path
import tarfile
import argparse
import subprocess

from elasticsearch import Elasticsearch, exceptions as esexp


class ElasticSearch(object):
    """
    ElasticSearch Environment
    """

    def __init__(self, ip=None, port="9200"):
        """
        Initializer function

        """
        print("Initializing the Elastic-Search environment object")

        if ip is None:
            raise Exception("ES IP is not define")

        self.ip = ip
        self.port = port
        # Connect to the server
        self.con = self._es_connect()

    def _es_connect(self):
        """
        Create a connection to the ES

        Returns:
            Elasticsearch: elasticsearch connection object

        Raise:
            ConnectionError: if can not connect to the server

        """
        try:
            es = Elasticsearch([{"host": self.ip, "port": self.port}])
        except esexp.ConnectionError:
            print("Can not connect to ES server")
            raise
        return es

    def get_indices(self):
        """
        Getting list of all indices in the ES server.

        Returns:
            list : list of all indices defined in the ES server

        """
        results = []
        print("Getting all indices")
        for ind in self.con.indices.get_alias("*"):
            results.append(ind)
        return results


def run_command(cmd, **kwargs):
    """
    Running command on the OS and return the STDOUT & STDERR outputs
    in case of argument is not string or list, return error message

    Args:
        cmd (str): the command to execute


    Returns:
        list : all STDOUT / STDERR output as list of lines

    """

    command = cmd.split()

    for key in ["stdout", "stderr", "stdin"]:
        kwargs[key] = subprocess.PIPE

    print(f"Going to run {cmd} with timeout of 600 sec.")
    cp = subprocess.run(command, timeout=600, **kwargs)
    output = cp.stdout.decode()
    err = cp.stderr.decode()
    # exit code is not zero
    if cp.returncode:
        print(f"Command finished with non zero ({cp.returncode}) {err}")
        output += f"Error in command: {err}"

    output = output.split("\n")  # convert output to list
    output.pop()  # remove last empty element from the list
    return output


def main():
    dmp_cmd = "/elasticsearch-dump/elasticsearch-dump"
    base_path = "/tmp/results"
    res_file = "/tmp/full_results.tgz"

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--ip", action="store", help="The IP of the Internal ES")
    parser.add_argument("--port", action="store", default="9200", help="The ES port")
    args, unknown = parser.parse_known_args()
    if not args.ip:
        raise Exception("IP of ES did is define")

    es = ElasticSearch(ip=args.ip, port=args.port)
    indices = es.get_indices()

    base_url = f"http://{es.ip}:{es.port}"

    # Creating results directory
    run_command(f"mkdir -p {base_path}")

    # Dumping data for all indices
    for index in indices:
        print(f"Getting data for {index}....")
        file_name = f"{base_path}/{index}"
        url = f"{base_url}/{index}"
        run_command(
            f"{dmp_cmd} dump --file {file_name}.mapping.json --url {url} --type mapping"
        )
        run_command(
            f"{dmp_cmd} dump --file {file_name}.data.json --url {url} --type data"
        )

    # Create one tar file (compressed) with all result files
    with tarfile.open(res_file, "w:gz") as tar:
        tar.add(base_path, arcname=os.path.basename(base_path))

    print(f"ES dump is done. all data in the file : {res_file}")


if __name__ == "__main__":
    main()
