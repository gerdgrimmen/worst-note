# worst Note

Minimal Note Taking API with web front end

## Description

This is Project is build on: https://github.com/gerdgrimmen/worst-rest-api-example


A minimal note taking frontend included in an rest api server

### Dependencies

For the Service

* import json
* import os
* from http.server import HTTPServer, BaseHTTPRequestHandler
* from urllib.parse import urlparse, parse_qs

For building a container image

* docker build/podman build

### Installing

* Downloading/Copying the script

### Executing program

just run the command "python ./main.py"

```
python ./main.py
```
To use the API just take the examples from the ./curls.sh.

### Building conainer image

You need docker/podman or comparable software installed to build the container file yourself.

```
chmod +x container_build.sh
./conainer_build.sh 
```

### Running conainer

This is a podman example use your equivalent if you run a different software solution 
```
podman run -d --name worsty -p 5000:5000 worst/worst-note:0.2.1
```

## Authors

Contributors names and contact info

ex. Gerd Grimmen (F.KU)

## Version History
* 0.2.2
    * fix requesting images
* 0.2.1
    * fix missmatch in stored keys per object int/str
* 0.2
    * Added Support for pictures
    * Endpoint /images takes an image and saves it
      * bugfix: initial_persistence_setup() would not return a value when api_data.json file non-existent
* 0.1
    * Nothing here to see

## License

The Unlicense. Feel free to use or change it how you need.

## Acknowledgments

* https://github.com/ynsrc/python-simple-rest-api/tree/main