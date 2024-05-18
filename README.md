## What is this?

A LSB Replacement Steganography and Steganalysis browser program.

Encode a message into a `png` file, by inputting a ending key, message, and desired bits to use on RGB of the image.

Decode any `png` file. You will need to know the RGB bits used to encode, and the ending key.

> ⚠️ This was hacked together in one day for a small university coursework. The codebase is messy and many things are hard-coded. You have been warned.

Theres a live hosted demo [here](https://stenographic.servebeer.com/).

> ⚠️ DO NOT upload any sensitive photos there. Thats kinda about it. Also, its hosted on a VM with really bad specifications, so some picture processing might take some time.

## Development Setup

> Both deployment setup have been tested on Debian 12. No guarantees it will work on other operating systems...

### Client

1. Install [NodeJS v20.13.1](https://nodejs.org/en).
2. `cd steganography-client`
3. `npm install`
4. `npm run debug`
5. Visit your webpage at `localhost:4321` _(or whatever was listed on the console)_

> If you need to run as production instead, use `npm run build`, then `npm run preview`.

### API

1. Install [Python v3.12.3](https://www.python.org/)
2. `cd steganography-api`
3. _(Optional)_ Create a python virtual enviornment, then activate it; `python3 -m venv venv` > `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python3 app.py`
6. Your API endpoint is now running at `localhost:8080` _(or whatever was listed on the console)_

> It is running as debug, opened to all hosts, if you need to, just edit the `app.run(debug=DEBUG_ENABLED, port=8080, host='0.0.0.0')` respectively.
> 
> Quick and dirty documentation on API Routes on [here](https://github.com/wqyeo/LSB-Steganography/blob/main/steganography-api/README.md).
