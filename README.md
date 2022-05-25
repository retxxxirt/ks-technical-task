Google sheets link -
[click](https://docs.google.com/spreadsheets/d/1DL2pLSwZLe3BQtXMjjbXPbtIHiAxVU1HZH3mOETu49Q/edit)

### Prerequisites

To access google sheets, place `service_account.json` file in `./data` folder.
[Here described](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account) how
to generate this file. That account must have viewer access to target table. You can grant viewer
access via link or invite this account by email (`client_email` field in json file).

Also, you need to create a telegram bot. You can do that with
[@BotFather](https://t.me/BotFather)'s help.

### Settings

You must specify following environment variables before running scripts or servers:

- `DATABASE_DSN` - database connection url
- `GOOGLE_SHEET_KEY` - google sheet key (between `/d/` and `/edit` in url)
- `TELEGRAM_BOT_TOKEN` - telegram bot token
- `REACT_APP_BACKEND_HOST` - backend server host
- `REACT_APP_BACKEND_PORT`- backend server port

### Docker usage

Specify valid `x-environment-variables` and `x-service-account-volumes` in
`compose.yaml`.

    docker compose up

### Installation

    pip install -r requirements.txt
    cd app/webapp/frontend/
    npm i

### Usage

<sup>don't forget `export PYTHONPATH=.` in project root folder before running scripts</sup>

#### Refresher script

Syncs data from google sheets with database. Requires `DATABASE_DSN`, `GOOGLE_SHEET_KEY`
environment variables and `service_account.json` file.

    python scripts/refresh.py

#### Notifier script

Notifies via telegram bot about today's and overdue orders. Requires `DATABASE_DSN` and
`TELEGRAM_BOT_TOKEN` environment variables.

    python scripts/notify.py

#### Polling script

Starts bot polling to save all contacted users as notifications recipients.
Requires `DATABASE_DSN` and `TELEGRAM_BOT_TOKEN` environment variables.

    python scripts/polling.py

#### Backend dev server

Allows to receive all database orders as json. Requires `DATABASE_DSN` environment variable.

    FLASK_APP=app/webapp/backend flask run

#### Frontend dev server

SPA with actual orders data. Requires `REACT_APP_BACKEND_HOST` and `REACT_APP_BACKEND_PORT`
environment variables.

    cd app/webapp/frontend
    npm start