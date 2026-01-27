# Gmail Puller

Automatisches Abrufen von Gmail E-Mails jede Minute mit Docker.

Automatically check Gmail for new emails every minute using Docker.

## 🇩🇪 Deutsch

### Beschreibung

Dieses Projekt prüft automatisch jede Minute (konfigurierbar) auf neue E-Mails in Ihrem Gmail-Konto. Es läuft in einem Docker-Container und zeigt neue ungelesene E-Mails in den Logs an.

### Voraussetzungen

- Docker und Docker Compose installiert
- Ein Google Cloud Projekt mit aktivierter Gmail API
- OAuth 2.0 Credentials von Google

### Einrichtung

#### 1. Google Cloud Projekt erstellen

1. Gehen Sie zu [Google Cloud Console](https://console.cloud.google.com/)
2. Erstellen Sie ein neues Projekt oder wählen Sie ein bestehendes aus
3. Aktivieren Sie die Gmail API:
   - Navigieren Sie zu "APIs & Services" → "Library"
   - Suchen Sie nach "Gmail API" und aktivieren Sie sie

#### 2. OAuth 2.0 Credentials erstellen

1. Gehen Sie zu "APIs & Services" → "Credentials"
2. Klicken Sie auf "Create Credentials" → "OAuth client ID"
3. Wählen Sie "Desktop app" als Application type
4. Geben Sie einen Namen ein (z.B. "Gmail Puller")
5. Klicken Sie auf "Create"
6. Laden Sie die Credentials-Datei herunter
7. Benennen Sie die Datei in `credentials.json` um und legen Sie sie im Projektverzeichnis ab

#### 3. Konfiguration

1. Kopieren Sie die `.env.example` zu `.env`:
   ```bash
   cp .env.example .env
   ```

2. Passen Sie die `.env` Datei an (optional):
   ```env
   CHECK_INTERVAL=60          # Prüfintervall in Sekunden (60 = 1 Minute)
   GMAIL_LABELS=INBOX         # Welche Labels geprüft werden sollen
   MAX_MESSAGES=10            # Maximale Anzahl der Nachrichten pro Prüfung
   LOG_LEVEL=INFO            # Log-Level (DEBUG, INFO, WARNING, ERROR)
   ```

3. Stellen Sie sicher, dass `credentials.json` im Projektverzeichnis liegt

#### 4. Erste Authentifizierung

Beim ersten Start müssen Sie sich mit Ihrem Google-Konto authentifizieren:

```bash
# Ohne Docker (für erste Authentifizierung)
pip install -r requirements.txt
python gmail_puller.py
```

Es öffnet sich ein Browser-Fenster. Melden Sie sich an und gewähren Sie die Berechtigungen. Die Datei `token.json` wird automatisch erstellt und für zukünftige Authentifizierungen verwendet.

#### 5. Mit Docker starten

```bash
# Container bauen und starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down
```

### Verwendung

Nach dem Start prüft der Container automatisch jede Minute auf neue E-Mails und zeigt diese in den Logs an:

```bash
docker-compose logs -f gmail-puller
```

Sie sehen Ausgaben wie:
```
gmail-puller  | 2024-01-27 12:00:00 - INFO - Found 2 unread message(s)
gmail-puller  | 2024-01-27 12:00:00 - INFO -   - From: sender@example.com
gmail-puller  | 2024-01-27 12:00:00 - INFO -     Subject: Test Email
gmail-puller  | 2024-01-27 12:00:00 - INFO -     Date: Mon, 27 Jan 2024 12:00:00 +0000
```

### Fehlerbehebung

**Problem:** "credentials.json not found"
- Lösung: Stellen Sie sicher, dass die `credentials.json` Datei im Projektverzeichnis liegt

**Problem:** "Access denied" oder OAuth-Fehler
- Lösung: Löschen Sie `token.json` und authentifizieren Sie sich erneut

**Problem:** Container startet nicht
- Lösung: Prüfen Sie die Logs mit `docker-compose logs`

---

## 🇬🇧 English

### Description

This project automatically checks for new emails in your Gmail account every minute (configurable). It runs in a Docker container and displays new unread emails in the logs.

### Prerequisites

- Docker and Docker Compose installed
- A Google Cloud project with Gmail API enabled
- OAuth 2.0 credentials from Google

### Setup

#### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Gmail API" and enable it

#### 2. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Select "Desktop app" as application type
4. Enter a name (e.g., "Gmail Puller")
5. Click "Create"
6. Download the credentials file
7. Rename the file to `credentials.json` and place it in the project directory

#### 3. Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Adjust the `.env` file (optional):
   ```env
   CHECK_INTERVAL=60          # Check interval in seconds (60 = 1 minute)
   GMAIL_LABELS=INBOX         # Which labels to check
   MAX_MESSAGES=10            # Maximum number of messages per check
   LOG_LEVEL=INFO            # Log level (DEBUG, INFO, WARNING, ERROR)
   ```

3. Ensure `credentials.json` is in the project directory

#### 4. Initial Authentication

On first run, you need to authenticate with your Google account:

```bash
# Without Docker (for initial authentication)
pip install -r requirements.txt
python gmail_puller.py
```

A browser window will open. Sign in and grant the permissions. The `token.json` file will be created automatically and used for future authentications.

#### 5. Start with Docker

```bash
# Build and start container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

### Usage

After starting, the container automatically checks for new emails every minute and displays them in the logs:

```bash
docker-compose logs -f gmail-puller
```

You'll see output like:
```
gmail-puller  | 2024-01-27 12:00:00 - INFO - Found 2 unread message(s)
gmail-puller  | 2024-01-27 12:00:00 - INFO -   - From: sender@example.com
gmail-puller  | 2024-01-27 12:00:00 - INFO -     Subject: Test Email
gmail-puller  | 2024-01-27 12:00:00 - INFO -     Date: Mon, 27 Jan 2024 12:00:00 +0000
```

### Troubleshooting

**Problem:** "credentials.json not found"
- Solution: Ensure the `credentials.json` file is in the project directory

**Problem:** "Access denied" or OAuth errors
- Solution: Delete `token.json` and re-authenticate

**Problem:** Container won't start
- Solution: Check the logs with `docker-compose logs`

---

## 📋 Features

- ✅ Automatic email checking every minute (configurable)
- ✅ Docker containerized for easy deployment
- ✅ OAuth 2.0 authentication with Gmail API
- ✅ Configurable via .env file
- ✅ Detailed logging of new emails
- ✅ Persistent authentication (token.json)
- ✅ Automatic token refresh

## 🔒 Security

- OAuth 2.0 authentication (no password storage)
- Read-only access to Gmail
- Credentials stored locally, never shared
- `.gitignore` configured to exclude sensitive files

## 📝 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
