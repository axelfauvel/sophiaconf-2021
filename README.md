# conf_af_tv_sophia_2021

# How to use it ?

## prerequisites
You'll need a `mosquitto` and `redis` up and running

## web server
Install dependencies in `requirements.txt` and run `gunicorn -b 0.0.0.0:8080 app:app` from frontend folder

## backend
Install dependencies in `requirements.txt` and run `python consumer.py`

## load code to m5stick
You need to have `ampy` and `picocom` installed
You need to know which port your m5stick uses, something like `/dev/tty.usbserial-6152A0EFA8`

Then you need to fill `config.py` with proper configuration

Once it's done, upload `config.py` and `main.py` to your m5stick using `ampy`

`ampy -p /dev/tty.usbserial-6152A0EFA8 --baud 115200 put main.py /flash/main.py`

`ampy -p /dev/tty.usbserial-6152A0EFA8 --baud 115200 put boot.py /flash/boot.py`
