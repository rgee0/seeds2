seeds2
=======

> A Python application for live tweeting photos - in this case a germinating broad bean - from a Raspberry Pi.  This is fork of the original [seeds2 project by Alex Ellis](https://github.com/alexellis/seeds2).  The main difference is the addition of a timelapse option which will retain locally the tweeted images, thus enabling production of a timelapse video when the activity that you're capturing completes.  Here's an example on [YouTube](https://www.youtube.com/watch?v=TNVrAaHmI_A)

[![InternetOfPulses Timelapse on YouTube](https://img.youtube.com/vi/TNVrAaHmI_A/0.jpg)](https://www.youtube.com/watch?v=TNVrAaHmI_A "InternetOfPulses Timelapse on YouTube")

* [Example Tweet](https://twitter.com/rgee0T/status/881163025276915715)

### Installation

* Install dependencies

```
$ sudo apt-get -y install python3-pip libopenjp2-7 libopenjp2-7-dev libopenjp2-tools
$ sudo pip3 install -r requirements.txt
```

* Get the Roboto font from:

```
$ curl -sSL https://github.com/googlefonts/roboto/releases/download/v2.138/roboto-unhinted.zip -o roboto.zip
```

* Extract it

```
$ unzip roboto.zip -d roboto
```

### Configuration

Most configuration can be achieved without altering the python code via `config.py`.

* Update your access keys

Now add your Twitter keys into the config.py file:

```json
"twitter": {
                "enabled": True,
                "message" : "Internet of seeds #InternetOfSeeds",
                "ckey": "",
                "csecret": "",
                "akey": "",
                "asecret": ""
            },
```

> For testing without Tweeting you can set `enabled` to `False` in the `twitter` section of `config.py`.

* The default mode of operation is for timelapse to be disabled - images are deleted once tweeted.  To enable timelapse set `timelapse` to `True` in `config.py`.  This will create a series of timestamped images in the `images` directory which can later be combined to create a video.  Its also possible to run in timelapse mode without Tweeting, just set twitter `enabled` to `False` and `timelapse` to `True` in `config.py`.

>Tip: If capturing over a long period of time make sure you have sufficient disk space.

### Running

__Interactively:__
Run once using `python3 main.py`

__Scheduled:__
Use `cron` and this entry:

```cron
*/10 08-20 * * * /home/pi/seeds2/seed-it.sh
```

This results in one image/tweet every 10 minutes between 8am and 8:50pm.
