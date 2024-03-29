# ifttt-sunset

This script calls the Maker event API of ifttt at sunset time.

## Install

```
poetry install
```

## Usage

It's better to call it using a job scheduler such as CRON.

Replace the `api_key_string` with your Maker event API key.

```
# If you call a `sunset` event to the Maker event API at sunset time.
./ifttt-sunset.py -lat 35.677730 -lng 139.754813 -e sunset -k api_key_string

# If you call a `sunset` event to the Maker event API 30 minutes before sunset time.
./ifttt-sunset.py -lat 35.677730 -lng 139.754813 -e sunset -k api_key_string -a -30
```

## Help

```
./ifttt-sunset.py -h
```
