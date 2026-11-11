# IamGroot

[English](../README.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [বাংলা](README.bn.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [اردو](README.ur.md) · [Bahasa Indonesia](README.id.md) · **Deutsch** · [日本語](README.ja.md) · [मराठी](README.mr.md) · [Tiếng Việt](README.vi.md)

**Dein persönlicher Jobsucher.**

Die Jobsuche kostet viel Zeit. IamGroot nimmt dir die langsamen, langweiligen Teile ab. Es ist ein Helfer, der in KI-Chat-Tools wie Claude Code, Codex, ChatGPT, Gemini und Cursor arbeitet. Es funktioniert für jede Art von Job, in jedem Land.

## Was es macht

1. **Lernt dich kennen.** Es liest deinen Lebenslauf und stellt dir ein paar Fragen, zum Beispiel wo du arbeiten möchtest und wann du anfangen kannst.
2. **Erstellt einen sauberen Lebenslauf.** Es baut einen einseitigen Lebenslauf, den Bewerbungssoftware ohne Fehler lesen kann.
3. **Findet Jobs.** Es durchsucht die Stellenseiten vieler Firmen und behält die Jobs, die zu dir passen.
4. **Bewirbt sich für dich.** Es füllt die Bewerbungsformulare mit deinen Daten aus und schickt sie ab. Wenn dein KI-Tool keinen Browser bedienen kann, schreibt es die Antworten und du schickst sie selbst ab.
5. **Führt eine Liste.** Jeder Job kommt in eine einzige Liste. So weißt du immer, wo du dich beworben hast und was daraus geworden ist.
6. **Lernt dazu.** Es merkt sich deine Antworten und stellt dieselbe Frage nicht zweimal.

## So fängst du an

Du brauchst ein KI-Chat-Tool. Für alle Funktionen brauchst du außerdem Python, ein kostenloses Programm, auf deinem Computer.

1. Hol dir IamGroot. Führe diesen Befehl aus oder lade dieses Projekt herunter und öffne es in deinem KI-Tool:

   ```bash
   npx skills add ashok-cse/iamgroot
   ```

2. Sag deinem KI-Tool: **"You are IamGroot. Onboard me."** (Das heißt: Du bist IamGroot, lerne mich kennen.)
3. Gib ihm deinen Lebenslauf und beantworte seine Fragen.
4. Bitte es, Jobs zu finden und sich zu bewerben.

## Deine Daten bleiben bei dir

Alles über dich wird in einem Ordner namens `profile/` auf deinem eigenen Computer gespeichert. Es wird nie in dieses Projekt aufgenommen und nie weitergegeben.

## Was es niemals tut

- Fähigkeiten, Jobs oder Antworten erfinden. Wenn nur du die Antwort kennst, fragt es dich.
- Konten anlegen, Passwörter eintippen oder „Ich bin kein Roboter“-Prüfungen umgehen.
- Sich auf Jobs bewerben, die nicht zu dir passen, nur damit die Zahl größer wird.

## Mehr Details

Die folgenden Dateien sind auf Englisch.

- Wie es Schritt für Schritt arbeitet: [`skills/iamgroot/SKILL.md`](../skills/iamgroot/SKILL.md)
- Alle Regeln, an die es sich hält: [`skills/iamgroot/references/instructions.md`](../skills/iamgroot/references/instructions.md)
- Mit welchen KI-Tools es funktioniert: [`skills/iamgroot/references/agents.md`](../skills/iamgroot/references/agents.md)
- Was es aus echten Bewerbungen gelernt hat: [`skills/iamgroot/references/lessons.md`](../skills/iamgroot/references/lessons.md)
- Wie es Formulare auf Job-Websites ausfüllt: [`skills/iamgroot/references/ats-playbook.md`](../skills/iamgroot/references/ats-playbook.md)
- Die Befehle: `python3 skills/iamgroot/scripts/iamgroot.py --help`
