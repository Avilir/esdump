# esdump
Elasticsearch dumper

This is a tool to dump all data from elastic-search server to files.
each index is dumping to 2 files, one is for the mapping info, and one is for the data.

the tool is base on the shinexia/elasticsearch-dump project at github.

you can use it by running the script as stand-alone :

for stand alone run you will need to do some steps :

* install golang  : `yum install -y golang`
* install python3 : `yum install -y python3`
* install the elasticsearch module : `pip3 install elasticsearch`  
* clone the elasticsearch repo and create the dumpper: 
  
  ```
  # git clone https://github.com/shinexia/elasticsearch-dump.git
  # cd elasticsearch-dump
  # go build
  # chmod +x elasticsearch-dump
  ```
* clone this repo 
* now you can run the script :

  ```
  ./esdumper.py --ip <es ip/name> [--port <es port>]

    --ip : the IP or the DNS name of the elastic-search server
    --port : the port of the elastic-search server
     if omited the default port (9200) will be used
  ```
at the end the script will display the name of the .tgz file with all outputs

or by using a container.

the container can be pulled from Dockerhub, or created by using this repo and run :
```
# docker build .
```

and the run the script command within the container.
after the script is finished, you need to pull the results file from it.
