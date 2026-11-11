# IamGroot

[English](../README.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · **Français** · [العربية](README.ar.md) · [বাংলা](README.bn.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [اردو](README.ur.md) · [Bahasa Indonesia](README.id.md) · [Deutsch](README.de.md) · [日本語](README.ja.md) · [मराठी](README.mr.md) · [Tiếng Việt](README.vi.md)

**Votre chasseur d'emploi personnel.**

Chercher un emploi prend beaucoup de temps. IamGroot fait pour vous les tâches longues et ennuyeuses. C'est un assistant qui fonctionne dans des outils de discussion IA comme Claude Code, Codex, ChatGPT, Gemini et Cursor. Il convient à tout type d'emploi, dans tous les pays.

## Ce qu'il fait

1. **Il apprend à vous connaître.** Il lit votre CV et vous pose quelques questions, par exemple où vous voulez travailler et quand vous pouvez commencer.
2. **Il prépare un CV propre.** Il crée un CV d'une page que les logiciels de recrutement peuvent lire sans erreur.
3. **Il trouve des offres d'emploi.** Il parcourt les pages emploi de nombreuses entreprises et garde les offres qui vous correspondent.
4. **Il postule pour vous.** Il remplit les formulaires de candidature avec vos informations et les envoie. Si votre outil IA ne peut pas utiliser de navigateur, il rédige les réponses et c'est vous qui les envoyez.
5. **Il tient une liste.** Chaque offre est notée dans une seule liste, pour que vous sachiez toujours où vous avez postulé et ce qui s'est passé.
6. **Il apprend.** Il retient vos réponses et ne pose donc pas deux fois la même question.

## Comment commencer

Il vous faut seulement un outil de discussion IA.

1. Ouvrez votre outil de discussion IA.
2. Copiez ce message et envoyez-le :

   ```text
   Set up IamGroot from https://github.com/ashok-cse/iamgroot and onboard me.
   ```

   (Cela veut dire : installe IamGroot depuis cette adresse et commence à faire ma connaissance.)

3. Donnez-lui votre CV et répondez à ses questions.
4. Demandez-lui de trouver des offres et de postuler.

## Vos informations restent chez vous

Tout ce qui vous concerne est enregistré dans un dossier nommé `profile/` sur votre propre ordinateur. Ces informations ne sont jamais ajoutées à ce projet ni partagées.

## Ce qu'il ne fera jamais

- Inventer des compétences, des emplois ou des réponses. Si vous seul connaissez la réponse, il vous la demande.
- Créer des comptes, saisir des mots de passe ou contourner les tests « Je ne suis pas un robot ».
- Postuler à des offres qui ne vous correspondent pas juste pour augmenter le nombre de candidatures.

## Plus de détails

Les fichiers ci-dessous sont en anglais.

- Comment il fonctionne, étape par étape: [`skills/iamgroot/SKILL.md`](../skills/iamgroot/SKILL.md)
- Toutes les règles qu'il suit: [`skills/iamgroot/references/instructions.md`](../skills/iamgroot/references/instructions.md)
- Avec quels outils IA il fonctionne: [`skills/iamgroot/references/agents.md`](../skills/iamgroot/references/agents.md)
- Ce qu'il a appris de vraies candidatures: [`skills/iamgroot/references/lessons.md`](../skills/iamgroot/references/lessons.md)
- Comment il remplit les formulaires sur les sites d'emploi: [`skills/iamgroot/references/ats-playbook.md`](../skills/iamgroot/references/ats-playbook.md)
- Quels sites d'emploi il connaît, pays par pays: [`skills/iamgroot/references/job-portals.md`](../skills/iamgroot/references/job-portals.md)
- Ce qui change d'un pays à l'autre (permis de travail, salaire, CV et quand postuler): [`skills/iamgroot/references/countries.md`](../skills/iamgroot/references/countries.md)
- Les commandes: `python3 skills/iamgroot/scripts/iamgroot.py --help`
