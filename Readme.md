# Etude de cas Arcane

## Contexte

Une équipe de consultants Data Analyst souhaite pouvoir analyser des tweets récents de
Twitter afin de pouvoir proposer à ses clients français des analyses de tendances marketing.
Ils ont pour cela besoin d’avoir accès à la donnée dans un outil permettant de faire des
analyses. L’équipe de Data Analyst a des connaissances dans les langages VBA et SQL et
utilise déjà Google Workspace et Google Cloud Platform.
Elle souhaite une solution fiable, pouvant supporter des grands volumes de données et qui
soit capable de mettre à jour les données automatiquement et quotidiennement.
Les tweets à récupérer sont ceux correspondant au hashtag #Arcane (pas forcément ceux
de l’entreprise Arcane). Dans les données, on voudra les métriques:
- Le texte du tweet
- Le nombre de “like”
- Le nombre de retweets
- Le nombre de réponses
- Si il y a une vidéo, le nombre de vues
Toutes ces données sont publiques (https://developer.twitter.com/en/docs/twitter-api/metrics)
et sont accessibles via des accès standards à l’API Twitter.

## Problématique

Pouvez vous proposer un POC (proof of concept) etune vision de l’architecture cloud
permettant de mettre à disposition les données aux utilisateurs ?

## Approche

Vu que l'équipe de data analyst utilise GCP et a des conaissances en VBA et SQL on part du principe que l'on veut les données dans une table big query. A partir de la il est très facile d'utiliser datastudio pour faire de la dataviz.
Pour la partie ingestion de données le choix est beaucoup plus large. On peut utiliser une pipeline data 3rd party comme funnel, airbyte ou zapier pour connecter l'API twitter et la table big query en question mais dans le cas présent ça nous laisserai avec très peu de code à implémenter. On choisit donc d'implémenter une cloud function qui sera régulièrement appelé par cloud scheduler
pour alimenter big query. Pour des workflow plus complexe un pourra utiliser airflow mais ce n'est pas nécessaire ici.

Pour les secrets et la configuration j'utilise dynaconf qui permet de prendre des infos soit par fichier soit par variable d'environnement (en les préfixant avec ARCANE)

## Probleme

Je n'ai pas pu créer un compte developpeur pour l'API (car il demande un numéro de téléphone) twitter donc j'ai écris cette fonction à l'aveugle donc possible qu'il y ait quelques problème mais je pense que le principal est présent.
