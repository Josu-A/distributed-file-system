<div id="#top"></div>

# Distributed File System

<details>
    <summary>Table of Contents</summary>
    <ol>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#installation">Installation</a>
            <ol>
                <li><a href="#remote-machine">Remote machine</a>
                <li><a href="#client">Client</a>
            </ol>
        </li>
        <li><a href="#usage">Usage</a>
            <ol>
                <li><a href="#usage-remote-machine">Remote machine</a>
                <li><a href="#usage-client">Client</a>
            </ol>
        </li>
        <li><a href="#test-cases-used-to-evaluate">Test cases used to evaluate</a></li>
    </ol>
</details>

## Introduction

This project implements a distributed file system that allows the user to sync a local folder with a remote one, granting the ability to make an always up-to-date backup seamlessly.

<p align="right">(<a href="#top">go to top</a>)</p>

## Features

- File creation, deletion, and modification
- Directory creation and deletion
- Data consistency and reliability
- File size limits

<p align="right">(<a href="#top">go to top</a>)</p>

## Installation

To install and set up the distributed file system, follow these steps:

<p align="right">(<a href="#top">go to top</a>)</p>

### <span id="installation-remote-machine"></span> Remote machine

1. Clone the repository:
    ```console
    $ git clone https://github.com/Josu-A/distributed-file-system
    $ cd distributed-file-system
    ```

2. Set the port the server will be running at by modifying the `SERVER_PORT` variable inside the `szasar.py` utility file:
    ```python
    SERVER_PORT = 6012
    ```

3. Change the directory that will store the uploaded files by modifying the `FILES_PATH` inside the `serv_fich.py` file.
    ```python
    FILES_PATH = "server_files/"
    ```

<p align="right">(<a href="#top">go to top</a>)</p>

### <span id="installation-client"></span> Client

1. Clone the repository:
    ```console
    $ git clone https://github.com/Josu-A/distributed-file-system
    $ cd distributed-file-system
    ```

2. Install the required dependencies:
    ```console
    $ pip install -r requirements.txt
    ```

3. Set the port used by the server which was previously set by changing the `SERVER_PORT` variable inside the `szasar.py` utility file:
    ```python
    SERVER_PORT = 6012
    ```

4. Set the port the watchdog server will be running at by modifying the `WATCHDOG_PORT` variable inside the `szasar.py` utility file:
    ```python
    WATCHDOG_PORT = 6013
    ```

5. Set the address that the remote server is located by modifying the `SERVER_FILES` variable inside the `cli_fich.py` file.
    ```python
    SERVER_FILES = 'localhost'
    ```

6. Change the directory to be tracked by modifying the `CLIENT_FILES_PATH` inside the `szasar.py` file.
    ```python
    CLIENT_FILES_PATH = "server_files/"
    ```

<p align="right">(<a href="#top">go to top</a>)</p>

## Usage

To start the distributed file system, run the following command on each node:

<p align="right">(<a href="#top">go to top</a>)</p>

### <span id="usage-remote-machine"></span> Remote server

Run the server:

```console
$ python serv_fich.py
```

<p align="right">(<a href="#top">go to top</a>)</p>

### <span id="usage-client"></span> Client

Run the watchdog local server:

```console
$ python serv_wd.py
```

And then, run the client:

```console
$ python cli_fich.py
```

<p align="right">(<a href="#top">go to top</a>)</p>

## Test cases used to evaluate

```console
$ touch f1
$ cp /etc/passwd .
$ head passwd >f2
$ echo "Hello" >>f2
$ nano f2 # + add some text + save the file (without exiting) + .......... + add some more text + exit nano saving the last changes to the file
$ rm f1
$ mv f2 f3
$ touch passwd
$ mkdir dir1
$ rmdir dir1 # (assuming dir1 is empty)
```

<p align="right">(<a href="#top">go to top</a>)</p>