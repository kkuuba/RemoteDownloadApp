## RemoteDownloadApp
**RemoteDownloadApp** - this simple web tool give possibility to download files on target device. In additions it allows to control all download stream parameters by web application interface.
## Content
- [Requirements](#requirements)
- [Features](#features)
- [Installation and Usage](#installation-and-usage)
- [Dependencies](#dependencies)
- [Author](#author)
- [License](#license)

## Requirements
### Server
* Python 3.6+
* Linux or Windows
* all packaged defined in requirements.txt

### Client
* Any web browser
## Features
- [x] Simple and elegant interface with link validation
- [x] Multiprocessing with all download tasks
- [x] Converting and downloading files from youtube links in mp3 format 

## Installation and Usage
### Server
To start server -> clone repo and run cmd 'python3 -m RemoteDownloadApp.web_app.main'. In long term use you can add bash script to crontab or schedule task in order to run web app wen server device is booting. In case access to web app outside local network NAT forwarding on your gateway is needed.
### Client
Enter this address in web browser: '{ip address of server device}:5555'. After that you should see app interface.
## Dependencies
### Server
* All libraries defined in file 'requirements.txt'
### Client
* Access to any web browser
## Authors
* https://github.com/kkuuba

## License
RemoteDownloadApp is released under the MIT license. See LICENSE for details.