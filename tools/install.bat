@echo off
rem ===========================================================================
rem  NIGHTCRAWLER v37 - gefuehrte Installation fuer Windows
rem
rem    tools\install.bat            gefuehrt, erklaert jeden Schritt
rem    tools\install.bat /express   nur Pflichtfragen
rem    tools\install.bat /auto      keine Fragen (Passwoerter werden erzeugt)
rem
rem  Das Gegenstueck fuer Linux, Raspberry Pi und macOS ist tools/installer.sh.
rem
rem  WARUM ES DAS GIBT UND WAS ANDERS IST
rem  NIGHTCRAWLER ist fuer Linux gebaut: systemd haelt ihn am Leben, die MOTD
rem  zeigt den Zustand beim Login, CrowdSec sperrt Angreifer aus. Nichts davon
rem  gibt es unter Windows. Was hier laeuft, ist der Bot selbst - Tracking,
rem  Aufnahme, Restream, Dashboard, Telegram und Discord - und der laeuft
rem  vollstaendig. Fuer den Dauerbetrieb bleibt ein Linux-Server die bessere
rem  Wahl; Windows ist der richtige Ort zum Ausprobieren und Entwickeln.
rem
rem  ZWEI BATCH-REGELN, DIE HIER UEBERALL GELTEN
rem  1) In einem mehrzeiligen Klammerblock wird JEDE Variable schon beim Lesen
rem     des Blocks ersetzt. Wer darin fragt und die Antwort gleich auswertet,
rem     wertet den Wert von VORHER aus. Deshalb: Fragen immer auf oberster
rem     Ebene, Verzweigung per einzeiligem "if ... goto" oder "if ... call".
rem  2) Bewusst ohne Umlaute - cmd.exe rendert je nach Codepage sonst
rem     Buchstabensalat.
rem ===========================================================================

setlocal
chcp 65001 >nul 2>&1
title NIGHTCRAWLER v37 - Installation

if /i "%~1"=="/?"     goto :hilfe
if /i "%~1"=="/help"  goto :hilfe
if /i "%~1"=="--help" goto :hilfe

set "MODUS=gefuehrt"
if /i "%~1"=="/express" set "MODUS=express"
if /i "%~1"=="/auto"    set "MODUS=auto"

set "SCHRITT=0"
set "GESAMT=10"
set "MERK=%TEMP%\nc-merkzettel.txt"
if exist "%MERK%" del "%MERK%"
rem uvloop hat keine Windows-Fassung - das ist reine Beschleunigung fuer
rem asyncio unter Linux und darf hier fehlen. Ohne diese Zeile bricht
rem "pip install -r requirements.txt" auf jedem Windows-Rechner ab.
set "OPT_AUS=uvloop"

rem ---------------------------------------------------------------- 1 -------
call :kopf "Willkommen"
echo.
echo   NIGHTCRAWLER v37 - TikTok-Live-Ueberwachung, Aufnahme,
echo   Multi-Ziel-Restream und KI-Moderation (AZRAEL).
echo.
echo   Dieses Skript richtet den Bot ein und erklaert dabei, was es tut
echo   und warum. Es fragt vor jedem Eingriff. Strg+C bricht gefahrlos ab.
echo.
echo   Der Weg in zehn Schritten:
echo     1  Willkommen            6  Konfiguration (.env)
echo     2  System pruefen        7  Selbsttest
echo     3  Python                8  Startskript und Autostart
echo     4  Zielverzeichnis       9  Was unter Windows anders ist
echo     5  Pakete               10  Zusammenfassung
echo.
if /i not "%MODUS%"=="gefuehrt" goto :los
call :frage_ja J "Loslegen?"
if /i "%ANTWORT%"=="N" goto :abbruch_freiwillig
:los

rem ---------------------------------------------------------------- 2 -------
call :kopf "System pruefen"
for /f "tokens=*" %%i in ('ver') do call :info "Windows: %%i"
call :info "Benutzer: %USERNAME%   Rechner: %COMPUTERNAME%"
set "WINGET=0"
where winget >nul 2>&1 && set "WINGET=1"
if "%WINGET%"=="1" call :info "winget vorhanden - fehlende Programme koennen installiert werden."
if "%WINGET%"=="0" call :warn "winget fehlt - Python und ffmpeg muessten von Hand kommen."
if "%WINGET%"=="0" call :erklaere "winget ist der Paketmanager von Windows, er steckt in der App 'App Installer' aus dem Microsoft Store."

rem ---------------------------------------------------------------- 3 -------
call :kopf "Python"
call :erklaere "bot.py braucht mindestens Python 3.12. Das ist keine Empfehlung: die Datei benutzt f-strings mit Backslash (PEP 701) - unter 3.11 scheitert schon das Einlesen mit einem SyntaxError."
call :finde_python
if defined PY goto :python_da
call :warn "Kein Python 3.12 oder neuer gefunden."
if "%WINGET%"=="0" goto :python_fehlt
call :frage_ja J "Python 3.13 jetzt per winget installieren?"
if /i "%ANTWORT%"=="N" goto :python_fehlt
winget install --id Python.Python.3.13 -e --source winget --accept-package-agreements --accept-source-agreements
call :finde_python
if defined PY goto :python_da
:python_fehlt
call :fehler "Ohne Python 3.12 oder neuer geht es nicht weiter."
echo      Download: https://www.python.org/downloads/windows/
echo      Beim Installieren "Add python.exe to PATH" ankreuzen.
echo      Danach ein NEUES Fenster oeffnen und dieses Skript erneut starten.
goto :ende_fehler
:python_da
for /f "tokens=*" %%i in ('%PY% -V') do call :gut "Python: %%i"

rem ffmpeg ist ein Programm, keine Bibliothek - es kommt nicht ueber pip.
where ffmpeg >nul 2>&1 && goto :ffmpeg_da
call :warn "ffmpeg fehlt."
call :erklaere "ffmpeg schneidet, kodiert und sendet - es ist das Herz von Aufnahme und Restream. Der Bot startet auch ohne, kann dann aber nichts aufzeichnen und nichts weitersenden."
if "%WINGET%"=="0" goto :ffmpeg_hand
call :frage_ja J "ffmpeg jetzt per winget installieren?"
if /i "%ANTWORT%"=="N" goto :ffmpeg_hand
winget install --id Gyan.FFmpeg -e --source winget --accept-package-agreements --accept-source-agreements
call :warn "winget setzt den PATH erst fuer NEUE Fenster. Steht ffmpeg gleich noch als fehlend da: Fenster schliessen, neu oeffnen, Skript erneut starten."
goto :ffmpeg_fertig
:ffmpeg_hand
echo      Download: https://www.gyan.dev/ffmpeg/builds/   (den Ordner bin in den PATH legen)
call :merken "OFFEN: ffmpeg installieren - ohne ihn keine Aufnahme und kein Restream"
goto :ffmpeg_fertig
:ffmpeg_da
for /f "tokens=*" %%i in ('where ffmpeg') do call :gut "ffmpeg: %%i"
:ffmpeg_fertig

rem ---------------------------------------------------------------- 4 -------
call :kopf "Zielverzeichnis"
set "SKRIPTDIR=%~dp0"
set "QUELLE="
if exist "%SKRIPTDIR%..\bot.py" call :setze_quelle
if defined QUELLE call :info "Quelltext liegt bereits hier: %QUELLE%"
if defined QUELLE set "VORGABE=%QUELLE%"
if not defined QUELLE call :info "Kein Quelltext neben dem Skript - er wird von GitHub geholt."
if not defined QUELLE set "VORGABE=%USERPROFILE%\nightcrawler"
call :frage_text "In welches Verzeichnis soll NIGHTCRAWLER?" "%VORGABE%"
set "ZIEL=%ANTWORT%"
if /i "%ZIEL%"=="%QUELLE%" goto :quelle_fertig
if defined QUELLE goto :kopieren
where git >nul 2>&1 || goto :kein_git
if exist "%ZIEL%\bot.py" call :info "Bestehende Installation gefunden - Quelltext bleibt unangetastet."
if exist "%ZIEL%\bot.py" goto :quelle_fertig
git clone --depth 1 https://github.com/itsamemedev/Telegram-Stream-Info-Bot.git "%ZIEL%"
if errorlevel 1 goto :ende_fehler
call :gut "Quelltext geholt."
goto :quelle_fertig
:kein_git
call :fehler "git fehlt und wird zum Holen des Quelltexts gebraucht."
if "%WINGET%"=="1" echo      winget install --id Git.Git -e
goto :ende_fehler
:kopieren
if not exist "%ZIEL%" mkdir "%ZIEL%"
call :info "Kopiere Quelltext nach %ZIEL%"
call :erklaere ".env, Datenbanken, Aufnahmen und Logs bleiben dabei unberuehrt - sie gehoeren dir, nicht dem Build."
robocopy "%QUELLE%" "%ZIEL%" /E /XD .git .venv recordings logs __pycache__ /XF .env *.db /NFL /NDL /NJH /NJS /NP >nul
rem Rueckgabewert sofort sichern: jedes weitere Kommando - auch ein echo in
rem einem Unterprogramm - setzt ERRORLEVEL zurueck. Ein zweites
rem "if errorlevel" haette sonst nie ausgeloest.
set "RC=%ERRORLEVEL%"
rem robocopy meldet 0-7 als Erfolg (1 = kopiert, 3 = kopiert und uebersprungen).
if %RC% GEQ 8 call :fehler "Kopieren fehlgeschlagen (robocopy %RC%)."
if %RC% GEQ 8 goto :ende_fehler
call :gut "Quelltext liegt in %ZIEL%"
:quelle_fertig
cd /d "%ZIEL%"
set "ENVF=%ZIEL%\.env"
set "VENV=%ZIEL%\.venv"
set "VPY=%VENV%\Scripts\python.exe"

rem ---------------------------------------------------------------- 5 -------
call :kopf "Pakete"
call :erklaere "Alles Weitere lebt in einer virtuellen Umgebung unter .venv - ein eigener Ordner mit eigenem Python und eigenen Bibliotheken. Damit kann keine Installation hier dein System-Python beschaedigen und umgekehrt."
if not exist "%VPY%" goto :venv_neu
"%VPY%" -c "import sys;sys.exit(0 if sys.version_info>=(3,12) else 1)" >nul 2>&1 && goto :venv_da
call :warn "Vorhandenes .venv passt nicht (zu altes Python) - wird neu angelegt."
rmdir /s /q "%VENV%"
:venv_neu
call :info "Lege virtuelle Umgebung an"
%PY% -m venv "%VENV%"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" call :fehler "venv liess sich nicht anlegen."
if not "%RC%"=="0" goto :ende_fehler
call :gut "Umgebung angelegt."
goto :venv_fertig
:venv_da
call :gut "Vorhandene Umgebung wird weiterbenutzt."
:venv_fertig

call :erklaere "Fuenf Pakete sind Zubehoer: jedes kostet Platz und Zeit, keines ist fuer den Kern noetig, jedes laesst sich spaeter nachruesten mit  .venv\Scripts\pip install NAME"
if /i not "%MODUS%"=="gefuehrt" goto :opt_vorgabe
call :frage_ja J "discord.py installieren?  (zweite Bedienoberflaeche: 45 Slash-Commands, Moderation, Community)"
if /i "%ANTWORT%"=="N" call :opt_aus "discord.py"
call :frage_ja N "faster-whisper installieren?  (Transkription des Streams, Grundlage fuer Clips und Highlights; rund 300 MB und viel CPU)"
if /i "%ANTWORT%"=="N" call :opt_aus "faster-whisper"
call :frage_ja N "PyMySQL installieren?  (nur noetig, wenn die Daten in MariaDB statt SQLite liegen sollen)"
if /i "%ANTWORT%"=="N" call :opt_aus "PyMySQL"
call :frage_ja N "redis installieren?  (Cache; erst bei sehr vielen gleichzeitigen Dashboard-Zugriffen sinnvoll)"
if /i "%ANTWORT%"=="N" call :opt_aus "redis"
call :frage_ja N "boto3 installieren?  (schiebt Aufnahmen automatisch in einen S3-Speicher)"
if /i "%ANTWORT%"=="N" call :opt_aus "boto3"
goto :opt_fertig
:opt_vorgabe
set "OPT_AUS=%OPT_AUS% faster-whisper PyMySQL redis boto3"
if /i "%MODUS%"=="auto" set "OPT_AUS=%OPT_AUS% discord.py"
:opt_fertig
call :info "Nicht installiert wird:%OPT_AUS%"

set "NC_REQ=%TEMP%\nc-req.txt"
set "NC_AUS=%OPT_AUS%"
%PY% -c "import os,re;L=[x.split('#')[0].strip() for x in open('requirements.txt',encoding='utf-8')];A=set(os.environ.get('NC_AUS','').lower().replace('_','-').split());open(os.environ['NC_REQ'],'w',encoding='utf-8').write('\n'.join(x for x in L if x and re.split(r'[;<>=!~\[]',x)[0].strip().lower().replace('_','-') not in A))"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" call :fehler "requirements.txt liess sich nicht auswerten."
if not "%RC%"=="0" goto :ende_fehler

"%VPY%" -m pip install --upgrade pip wheel >nul 2>&1
call :info "pip install laeuft - je nach Verbindung 1 bis 15 Minuten."
"%VPY%" -m pip install -r "%NC_REQ%"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" goto :pip_fehler
rem streamlink und yt-dlp sind Python-Programme: unter Windows kommen sie
rem ueber pip mit und liegen dann in .venv\Scripts - immer aktuell, was bei
rem TikTok wichtiger ist als bei allem anderen.
"%VPY%" -m pip install --upgrade streamlink yt-dlp
call :gut "Python-Pakete stehen."
goto :pip_fertig
:pip_fehler
call :fehler "Mindestens ein Paket liess sich nicht installieren."
call :erklaere "Haeufigste Ursache unter Windows: ein Paket ohne fertiges Rad braucht einen Compiler. Abhilfe: 'Microsoft C++ Build Tools' installieren, oder das Paket auslassen. Wiederholen ist gefahrlos: .venv\Scripts\pip install -r requirements.txt"
goto :ende_fehler
:pip_fertig

rem ---------------------------------------------------------------- 6 -------
call :kopf "Konfiguration (.env)"
call :erklaere "Alle Einstellungen leben in einer einzigen Datei: .env. Sie enthaelt Bot-Token, Stream-Keys und Cookies - sie gehoert nie in ein Archiv und nie in ein Repository."
if not exist "%ENVF%" goto :env_neu
call :zeitstempel
copy /y "%ENVF%" "%ENVF%.bak.%STAMP%" >nul
call :gut "Vorhandene .env gesichert: .env.bak.%STAMP%"
goto :env_da
:env_neu
if exist "%ZIEL%\.env.example" copy /y "%ZIEL%\.env.example" "%ENVF%" >nul
if not exist "%ENVF%" type nul > "%ENVF%"
call :gut ".env aus der Vorlage angelegt (alle Vorgaben aktiv, nichts gesetzt)."
:env_da
rem Altlast frueherer Vorlagen: Zeilen der Form  NAME=   # (Geheimnis ...).
rem Das sieht wie ein Kommentar aus, ist aber der WERT - python-dotenv liest
rem bei unquotierten Werten den Rest der Zeile mit. Wer die alte .env.example
rem kopiert hat, hatte rund 40 solcher Variablen: der Bot hielt Discord,
rem Twitch und YouTube fuer eingerichtet und meldete "Token abgelehnt"
rem statt "kein Token".
for /f "usebackq delims=" %%i in (`"%VPY%" "%ZIEL%\tools\envset.py" --file "%ENVF%" --heal`) do set "GEHEILT=%%i"
if not "%GEHEILT%"=="0" call :gut "%GEHEILT% Platzhalter-Werte geleert (sie waeren als echte Werte gelesen worden)."

echo.
echo   Telegram - der Pflichtteil
call :erklaere "NIGHTCRAWLER wird ueber Telegram bedient. Den Bot-Token gibt dir @BotFather in Telegram: /newbot, Namen vergeben, fertig. Er sieht aus wie 123456789:AAF... und laesst sich nicht erzeugen, nur holen."
call :frage_geheimnis "Telegram Bot-Token (von @BotFather)" 0 0
if not defined ANTWORT goto :kein_tg
call :env_set BOT_TOKEN "%ANTWORT%"
call :gut "BOT_TOKEN gesetzt."
goto :tg_fertig
:kein_tg
call :warn "Kein Token - der Telegram-Teil bleibt still, bis BOT_TOKEN in der .env steht."
call :merken "OFFEN: BOT_TOKEN in .env eintragen (von @BotFather)"
:tg_fertig
call :erklaere "Ohne Freigabeliste darf jeder, der deinen Bot findet, ihn bedienen. ALLOWED_USER_IDS ist diese Liste (Zahlen, per Komma getrennt). Deine eigene ID sagt dir @userinfobot in Telegram."
call :frage_text "Deine Telegram-Nutzer-ID (mehrere per Komma, leer = keine Sperre)" ""
if defined ANTWORT call :env_set ALLOWED_USER_IDS "%ANTWORT%"
if not defined ANTWORT call :warn "Keine Freigabeliste - jeder Telegram-Nutzer kann den Bot bedienen."

echo.
echo   Dashboard
call :erklaere "Das Dashboard ist die Weboberflaeche: Sendeleiste, Aufnahmen, Statistiken, Abwehr. Es bindet nur auf 127.0.0.1, ist also nur auf diesem Rechner erreichbar - unter Windows ist das genau richtig."
call :frage_text "Port fuers Dashboard" "8050"
set "DASHPORT=%ANTWORT%"
call :env_set DASHBOARD_PORT "%DASHPORT%"
call :env_set WEB_HOST "127.0.0.1"
call :erklaere "Der Dashboard-Token schuetzt den Zugriff von aussen. Er ist frei waehlbar - hier ist Erzeugen die bessere Wahl als Ausdenken."
call :frage_geheimnis "Dashboard-Token" 1 40
if defined ANTWORT call :env_set DASHBOARD_TOKEN "%ANTWORT%"
if defined ANTWORT call :merken "Dashboard-Token: steht in .env (DASHBOARD_TOKEN)"

if /i not "%MODUS%"=="gefuehrt" goto :pin_fertig
call :erklaere "Zusaetzlich gibt es einen PIN-Login fuer die Weboberflaeche und die Handy-PWA - bequemer als ein 40-Zeichen-Token im Browser."
call :frage_ja N "PIN-Login einrichten?"
if /i "%ANTWORT%"=="N" goto :pin_fertig
call :erzeuge_pin 6
echo       erzeugte PIN: %ANTWORT%
call :env_set DASHBOARD_PIN "%ANTWORT%"
call :merken "Dashboard-PIN: steht in .env (DASHBOARD_PIN)"
:pin_fertig

echo.
echo   Discord
call :erklaere "Optional: dieselben Funktionen als Slash-Commands in deinem Discord-Server. Token aus dem Discord Developer Portal (Bot, dann Reset Token). Ohne Token bleibt der Discord-Teil still - der Bot startet trotzdem."
if /i not "%MODUS%"=="gefuehrt" goto :discord_fertig
call :frage_ja N "Discord jetzt einrichten?"
if /i "%ANTWORT%"=="N" goto :discord_fertig
call :frage_geheimnis "Discord Bot-Token" 0 0
if defined ANTWORT call :env_set DISCORD_BOT_TOKEN "%ANTWORT%"
call :frage_text "Discord-Server-ID (Rechtsklick auf den Server, ID kopieren)" ""
if defined ANTWORT call :env_set DISCORD_GUILD_ID "%ANTWORT%"
call :frage_text "Name der Admin-Rolle (fuer /ban, /timeout, /setup_...)" "Admin"
if defined ANTWORT call :env_set DISCORD_ADMIN_ROLE "%ANTWORT%"
call :gut "Discord konfiguriert."
:discord_fertig

echo.
echo   Restream-Ziele
call :erklaere "Restream heisst: der TikTok-Stream geht gleichzeitig auf deine eigenen Kanaele. Der Stream-Key kommt von der Plattform (Kick: Creator-Dashboard, Twitch: Einstellungen/Stream, YouTube: Studio/Livestream). Er ist ein Geheimnis und laesst sich nicht erzeugen."
call :erklaere "Zur Last: sobald ein zweites Ziel dazukommt, muss ffmpeg umkodieren - das kostet ein Vielfaches an CPU. Ein Ziel ohne Transcode laeuft auch auf schwacher Hardware."
if /i not "%MODUS%"=="gefuehrt" goto :restream_fertig
call :restream_ziel KICK Kick
call :restream_ziel TWITCH Twitch
call :restream_ziel YOUTUBE YouTube
:restream_fertig
call :gut "Konfiguration geschrieben: %ENVF%"

rem ---------------------------------------------------------------- 7 -------
call :kopf "Selbsttest"
call :erklaere "Jetzt wird geprueft, ob das Zusammengestellte wirklich laeuft: bot.py --selfcheck laedt den kompletten Bot, prueft Werkzeuge, Konfiguration und Erreichbarkeiten und beendet sich wieder. Das ist der Unterschied zwischen 'installiert' und 'laeuft'."
"%VPY%" bot.py --selfcheck
set "RC=%ERRORLEVEL%"
if %RC% GEQ 2 goto :selftest_kaputt
if "%RC%"=="1" call :warn "Der Selbsttest meldet offene Punkte (oben). Meist fehlt ein Token - der Bot startet trotzdem."
if "%RC%"=="1" call :merken "Selbsttest hatte Befunde - erneut: .venv\Scripts\python.exe bot.py --selfcheck"
if "%RC%"=="0" call :gut "Selbsttest ohne Befund."
goto :selftest_fertig
:selftest_kaputt
call :warn "Der Selbsttest liess sich nicht ausfuehren - Ersatzpruefung: laesst sich bot.py einlesen?"
"%VPY%" -c "import ast;ast.parse(open('bot.py',encoding='utf-8').read());print('bot.py ist syntaktisch in Ordnung')"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" call :fehler "bot.py laesst sich nicht einlesen - Python-Fassung pruefen."
if not "%RC%"=="0" goto :ende_fehler
:selftest_fertig

rem ---------------------------------------------------------------- 8 -------
call :kopf "Startskript und Autostart"
> "%ZIEL%\start.bat" echo @echo off
>>"%ZIEL%\start.bat" echo rem Von tools\install.bat erzeugt - startet NIGHTCRAWLER.
>>"%ZIEL%\start.bat" echo title NIGHTCRAWLER
>>"%ZIEL%\start.bat" echo cd /d "%%~dp0"
>>"%ZIEL%\start.bat" echo .venv\Scripts\python.exe bot.py %%*
>>"%ZIEL%\start.bat" echo echo.
>>"%ZIEL%\start.bat" echo echo Der Bot wurde beendet. Fenster schliessen mit einer beliebigen Taste.
>>"%ZIEL%\start.bat" echo pause ^>nul
call :gut "Startskript: %ZIEL%\start.bat"
call :erklaere "Windows kennt kein systemd. Der uebliche Ersatz ist die Aufgabenplanung: eine Aufgabe, die den Bot bei der Anmeldung startet. Sie startet ihn nicht nach einem Absturz neu - fuer einen echten Dienst mit Neustart gibt es NSSM (nssm.cc)."
if /i not "%MODUS%"=="gefuehrt" goto :autostart_fertig
call :frage_ja N "Aufgabe 'NIGHTCRAWLER' anlegen, die bei der Anmeldung startet?"
if /i "%ANTWORT%"=="N" goto :autostart_fertig
schtasks /create /tn "NIGHTCRAWLER" /tr "\"%ZIEL%\start.bat\"" /sc onlogon /f >nul 2>&1
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" call :warn "Aufgabe liess sich nicht anlegen (fehlende Rechte?). Von Hand: Aufgabenplanung, Aufgabe erstellen, Ausloeser 'Bei Anmeldung'."
if "%RC%"=="0" call :gut "Aufgabe angelegt (entfernen: schtasks /delete /tn NIGHTCRAWLER /f)."
if "%RC%"=="0" call :merken "Autostart: Aufgabenplanung, Aufgabe 'NIGHTCRAWLER'"
:autostart_fertig

rem ---------------------------------------------------------------- 9 -------
call :kopf "Was unter Windows anders ist"
echo.
echo   - Kein systemd. Der Bot laeuft, solange sein Fenster offen ist,
echo     oder ueber die Aufgabenplanung ab der Anmeldung.
echo   - Kein MOTD-Statusbild beim Login (tools\motd.sh ist Linux und macOS).
echo   - Kein CrowdSec-Panel - die Abwehr ist ein Linux-Dienst.
echo   - Kein uvloop. Das ist reine Beschleunigung der asyncio-Schleife;
echo     ohne sie laeuft alles, nur etwas gemaechlicher.
echo   - tools\deploy.sh (Auslieferung mit Vorabpruefung und Rollback) ist
echo     ebenfalls Linux. Unter Windows aktualisierst du mit git pull.
echo   - Aufnahmen brauchen Platz: eine Stunde Stream sind grob 1 bis 3 GB.
echo     Der Ordner recordings gehoert auf die groesste Platte.
echo   - Der Ruhezustand unterbricht laufende Aufnahmen. Fuer Dauerbetrieb
echo     in den Energieoptionen den Standbymodus abschalten.
echo.

rem ---------------------------------------------------------------- 10 ------
call :kopf "Zusammenfassung"
set "NOTIZ=%USERPROFILE%\nightcrawler-installation.txt"
> "%NOTIZ%" echo NIGHTCRAWLER v37 - Installation
>>"%NOTIZ%" echo ==================================================
>>"%NOTIZ%" echo Verzeichnis   %ZIEL%
>>"%NOTIZ%" echo Konfiguration %ENVF%
>>"%NOTIZ%" echo Dashboard     http://127.0.0.1:%DASHPORT%
>>"%NOTIZ%" echo.
>>"%NOTIZ%" echo BEDIENUNG
>>"%NOTIZ%" echo   Starten     %ZIEL%\start.bat
>>"%NOTIZ%" echo   Selbsttest  .venv\Scripts\python.exe bot.py --selfcheck
>>"%NOTIZ%" echo   Aktualisieren  git pull ^&^& .venv\Scripts\pip install -r requirements.txt
>>"%NOTIZ%" echo.
if exist "%MERK%" >>"%NOTIZ%" echo MERKZETTEL
if exist "%MERK%" type "%MERK%" >> "%NOTIZ%"
>>"%NOTIZ%" echo.
>>"%NOTIZ%" echo WEITERLESEN
>>"%NOTIZ%" echo   docs\START_HIER.txt   Einstieg und Alltag
>>"%NOTIZ%" echo   docs\DEPLOY.md        Ausliefern, Rollback, Pruefschritte
>>"%NOTIZ%" echo   README.md             Uebersicht ueber alle Funktionen
echo.
call :gut "NIGHTCRAWLER ist eingerichtet."
echo.
echo   Verzeichnis   %ZIEL%
echo   Dashboard     http://127.0.0.1:%DASHPORT%
echo.
if exist "%MERK%" echo   Merkzettel
if exist "%MERK%" type "%MERK%"
if exist "%MERK%" echo.
echo   Naechste Schritte
echo     1  Starten:  %ZIEL%\start.bat
echo     2  In Telegram deinen Bot anschreiben:  /start, dann /track NAME
echo     3  Dashboard oeffnen:  http://127.0.0.1:%DASHPORT%
echo.
echo   Alles davon steht auch in %NOTIZ%
echo.
if exist "%NC_REQ%" del "%NC_REQ%"
if exist "%MERK%" del "%MERK%"
pause
endlocal
exit /b 0

rem ===========================================================================
rem  Unterprogramme
rem ===========================================================================

:kopf
set /a SCHRITT+=1
echo.
echo [%SCHRITT%/%GESAMT%] %~1
echo ------------------------------------------------------------------
goto :eof

:info
echo   - %~1
goto :eof

:gut
echo   [ok] %~1
goto :eof

:warn
echo   [!]  %~1
goto :eof

:fehler
echo   [X]  %~1
goto :eof

:erklaere
echo       %~1
goto :eof

:merken
rem Umleitung steht VORNE: bei "echo text>> datei" wuerde cmd eine Ziffer am
rem Textende als Handle-Nummer der Umleitung verschlucken.
>>"%MERK%" echo   - %~1
goto :eof

:opt_aus
set "OPT_AUS=%OPT_AUS% %~1"
call :merken "Python-Paket %~1 ausgelassen (spaeter: .venv\Scripts\pip install %~1)"
goto :eof

:setze_quelle
pushd "%SKRIPTDIR%.."
set "QUELLE=%CD%"
popd
goto :eof

:finde_python
set "PY="
for %%v in (3.13 3.14 3.12) do (
  if not defined PY (
    py -%%v -c "import sys;sys.exit(0 if sys.version_info>=(3,12) else 1)" >nul 2>&1 && set "PY=py -%%v"
  )
)
if defined PY goto :eof
python -c "import sys;sys.exit(0 if sys.version_info>=(3,12) else 1)" >nul 2>&1 && set "PY=python"
goto :eof

:zeitstempel
set "STAMP=%RANDOM%"
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"`) do set "STAMP=%%i"
goto :eof

rem  env_set SCHLUESSEL "WERT"
rem  Der Wert geht ueber die Umgebung, NICHT ueber die Kommandozeile: eine
rem  Kommandozeile steht in der Prozessliste, und dort haben Bot-Token und
rem  Stream-Keys nichts verloren. Den Rest macht tools/envset.py - in Batch
rem  laesst sich eine Datei nicht sicher zeilenweise umschreiben.
:env_set
set "NC_V=%~2"
"%VPY%" "%ZIEL%\tools\envset.py" --file "%ENVF%" %~1
set "NC_V="
goto :eof

rem  frage_ja VORGABE(J^|N) "Frage"  ->  ANTWORT=J oder N
rem  Ja/Nein-Fragen betreffen ausschliesslich Zubehoer, deshalb beantwortet
rem  /express sie mit der Vorgabe. Text- und Geheimnisfragen werden weiter
rem  gestellt - die kann niemand raten.
:frage_ja
set "ANTWORT=%~1"
if /i "%MODUS%"=="auto" goto :eof
if /i "%MODUS%"=="express" goto :eof
set "VORSCHLAG=[J/n]"
if /i "%~1"=="N" set "VORSCHLAG=[j/N]"
set "EINGABE="
set /p "EINGABE=  ? %~2 %VORSCHLAG% "
if not defined EINGABE goto :eof
if /i "%EINGABE:~0,1%"=="j" set "ANTWORT=J"
if /i "%EINGABE:~0,1%"=="y" set "ANTWORT=J"
if /i "%EINGABE:~0,1%"=="n" set "ANTWORT=N"
goto :eof

rem  frage_text "Frage" "Vorgabe"  ->  ANTWORT
:frage_text
set "ANTWORT=%~2"
if /i "%MODUS%"=="auto" goto :eof
set "EINGABE="
if "%~2"=="" set /p "EINGABE=  ? %~1: "
if not "%~2"=="" set /p "EINGABE=  ? %~1 [%~2] "
if defined EINGABE set "ANTWORT=%EINGABE%"
goto :eof

rem  frage_geheimnis "Beschreibung" ERZEUGBAR(0^|1) LAENGE  ->  ANTWORT
rem  Genau der gewuenschte Ablauf: erst fragen, ob erzeugt werden soll -
rem  sonst auf die Eingabe WARTEN, verdeckt und mit Wiederholung.
:frage_geheimnis
set "ANTWORT="
if "%~2"=="0" goto :geheim_eingabe
if /i "%MODUS%"=="auto" goto :geheim_erzeugen
call :frage_ja J "%~1: sicheres Passwort erzeugen lassen?"
if /i "%ANTWORT%"=="N" goto :geheim_eingabe
:geheim_erzeugen
call :erzeuge_pw %~3
echo       erzeugt: %ANTWORT%
echo       Notieren oder im Passwortmanager ablegen - es steht auch in der .env.
goto :eof
:geheim_eingabe
if /i "%MODUS%"=="auto" goto :eof
echo   ? %~1 eingeben (leer = spaeter selbst eintragen):
call :lies_still
goto :eof

:lies_still
set "ANTWORT="
set "PW1="
set "PW2="
where powershell >nul 2>&1 || goto :lies_klartext
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "$s=Read-Host -AsSecureString;[Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))"`) do set "PW1=%%i"
if not defined PW1 goto :lies_ende
echo   ? Zur Sicherheit wiederholen:
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "$s=Read-Host -AsSecureString;[Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))"`) do set "PW2=%%i"
if "%PW1%"=="%PW2%" goto :lies_ok
echo   [!]  Die Eingaben waren nicht gleich - noch einmal.
goto :lies_still
:lies_klartext
rem Ohne PowerShell bleibt nur die sichtbare Eingabe. Besser sichtbar als
rem gar nicht - der Wert landet ohnehin gleich in der .env.
set /p "PW1=  (sichtbar, PowerShell fehlt): "
:lies_ok
set "ANTWORT=%PW1%"
:lies_ende
set "PW1="
set "PW2="
goto :eof

:erzeuge_pw
set "ANTWORT="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "-join ((48..57)+(65..90)+(97..122) ^| Get-Random -Count %~1 ^| ForEach-Object {[char]$_})"`) do set "ANTWORT=%%i"
if not defined ANTWORT set "ANTWORT=%RANDOM%%RANDOM%%RANDOM%%RANDOM%"
goto :eof

:erzeuge_pin
set "ANTWORT="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "-join (1..%~1 ^| ForEach-Object {Get-Random -Maximum 10})"`) do set "ANTWORT=%%i"
if not defined ANTWORT set "ANTWORT=%RANDOM%"
goto :eof

rem  restream_ziel PRAEFIX Klarname
:restream_ziel
call :frage_ja N "%~2 als Restream-Ziel einrichten?"
if /i "%ANTWORT%"=="N" goto :rz_aus
call :frage_geheimnis "%~2 Stream-Key" 0 0
if not defined ANTWORT goto :rz_aus
call :env_set %~1_STREAM_KEY "%ANTWORT%"
call :env_set %~1_ENABLED 1
call :gut "%~2 eingerichtet."
goto :eof
:rz_aus
call :env_set %~1_ENABLED 0
goto :eof

:hilfe
echo NIGHTCRAWLER v37 - Installation fuer Windows
echo.
echo   tools\install.bat            gefuehrt, mit Erklaerungen
echo   tools\install.bat /express   nur Pflichtfragen (Token, Pfade, Keys);
echo                                alle Ja/Nein-Fragen per Vorgabe
echo   tools\install.bat /auto      gar keine Fragen, Passwoerter werden erzeugt
echo   tools\install.bat /?         diese Hilfe
echo.
echo Fuer Linux, Raspberry Pi und macOS: tools/installer.sh
endlocal
exit /b 0

:abbruch_freiwillig
echo.
echo   Abgebrochen - es wurde nichts veraendert.
endlocal
exit /b 0

:ende_fehler
echo.
echo   Die Installation wurde in Schritt %SCHRITT% abgebrochen.
echo   Was bereits geschrieben wurde, bleibt liegen - ein erneuter Lauf
echo   setzt dort auf, ohne Schaden anzurichten.
echo.
pause
endlocal
exit /b 1
