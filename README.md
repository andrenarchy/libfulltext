# libfulltext
[![Build Status](https://travis-ci.org/andrenarchy/libfulltext.svg?branch=master)](https://travis-ci.org/andrenarchy/libfulltext)
[![Licence: GPL v3](https://img.shields.io/github/license/andrenarchy/libfulltext.svg)](LICENSE)

libfulltext is a python suite to aid with bulk-downloading open-access papers.
Our aim is to allow to quickly determine a list of open-access papers
from *all* journals and download their full text.

# Setup

Before you can get going you need to install the required python packages
(see [`requirements.txt`](requirements.txt))
and [setup the configuration](#configuration) with
the required API keys for the publishers.

## Configuration
For some publishers (like Elsevier) we absolutely require
an API key. See [getting your API keys](#getting-your-api-keys) for details.

For now the simplest is to replicate and adapt the example configuration
at `~/.config/libfulltext/config.yaml`:
```yaml
publishers:
  elsevier:
    apikey: "your_elsevier_api_key_here"
```

### Getting your API keys
- Elsevier:
    1. Get an [Elsevier developer account][elsevier-api]
    2. Log in and create an API key.

## 34c3 hacking pad
This project started from a workshop at [34c3][34c3].
Some information, ideas and resources are not yet transfered
related to this project you can find on the
[34c3 open science workshop][pad] pad.


[pad]:           https://hackmd.io/CYMwRgjApgxgbBAtMMtEBYCGwlgEzAAciYcwA7BJuoeiAMyZA===
[elsevier-api]:  https://dev.elsevier.com/user/registration
[34c3]:          https://events.ccc.de/congress/2017/wiki/index.php/Main_Page
