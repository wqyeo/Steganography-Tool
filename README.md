## What is this?

A Steganography Web Application.

**Supported Files**
- PNG
- WAV

Theres a live hosted demo [here](https://stenographic.servebeer.com/).

> ⚠️ DO NOT upload any sensitive photos there. Thats kinda about it. Also, its hosted on a VM with really bad specifications, so processing a larger file might take some time.

## Development Setup

> Both deployment setup have been tested on Debian 12. No guarantees it will work on other operating systems...

1. Install [Docker Engine](https://docs.docker.com/engine/install/) with Docker Compose
2. Create a enviornment variable file. `touch .env`.
3. Fill in the enviornment variable file based on the example file, `.env.example`.
4. `docker-compose -f docker-compose-debug up`
5. Visit your webpage at `localhost:4321`.
6. Your API endpoint should be running at `localhost:8000`

### Perform Database Migrations

The database for the API endpoint will be empty initally:

1. Give execution access to `migration-helpers.sh`.
2. Run `migration-helpers.sh`

In the event that the script does not work (no output, error messages), consider running the commands in the shell script manually.

> ⚠️ This was hacked together for a small university coursework. The codebase is messy and many things are hard-coded.<br>You have been warned.
