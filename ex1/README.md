# Computer Network experiment 1

## Requirement

In ex1, you are require to implement a connection with TCP and UDP, which is able to send simple text message and tranfer basic file.

## Check points

#### 1. Half-duplex Communication

The client will send any string input from the keyboard to the server, and the server will print the string on the screen after receiving it, and print the `client IP address` and `PORT`;

#### 2. Full-duplex Communication

Both client and server should have the ability to send and receive message from one another, and print the `IP address` and `PORT` as well.

#### 3. Multimedia streaming file Communication

Transmission of multimedia files: The client sends a video file to the server, which can be played on the server; during the sending process, it will "stop the network interface" (3 to 6 seconds) to check whether the file can be transmitted normally.

## Setup

Even though this is a simple project, you are recommended to setup with a independent conda virtual envirnment

```shell script
conda create -n py310 python=3.10

conda activate py310
```

Then use Pypi to download depend package

```shell script
pip install tqdm==4.64.1
```

## Usage

Run server with

```shell script
python server.py --TCP <True or False> --send_file <True or False> --filename <path of file to be sent> --receive_path <path to save sent file>
```

Run client with

```shell script
python client.py --TCP <True or False> --send_file <True or False> --filename <path of file to be sent> --receive_path <path to save sent file>
```

Or you can simply run with `python server.py` and `python client.py` and adjust parameters in [server.parse_args()](./server.py)


#### Hopefully you will like it.