# Fil de l'eau

Journal au fil de l'eau des travaux sur ce dépôt, du plus récent au plus ancien.
English version: [`../en/worklog.md`](../en/worklog.md).

## 2026-07-13

- Fork de `ecreall/KuneAgi` vers `michaellaunay/KuneAgi` ; reprise de la
  maintenance par Michaël Launay (Logikascium). KuneAgi est le tronc de
  référence de la modernisation de Nova-Ideo (audit de juillet 2026).
- Conversion de `README.rst` et `CHANGES.rst` en Markdown ; README rebaptisé
  de « Nova Ideo » en « KuneAgi », réécrit avec le statut du dépôt (droits :
  Cosmopolitical.coop pour les développements propres à KuneAgi, Logikascium
  pour le socle Nova-Ideo ; AGPL v3+ pour l'ensemble) et la feuille de route ;
  instructions d'exploitation obsolètes annotées (« less secure apps » de
  Google, images Docker Hub historiques).
- Mise à jour des métadonnées de build (`setup.py` : URLs du fork, champ
  mainteneur, description longue en Markdown, classifieur Python 3.6) ; ajout
  d'un `pyproject.toml` minimal (PEP 518) ; mise à jour du `MANIFEST.in`. Nom
  du paquet `novaideo` et chemins de modules inchangés (pickles ZODB).
- `sources.cfg` : `ecreall_dace`, `ecreall_pontus`, `ecreall_daceui` repointés
  vers leurs forks maintenus. Point connu pour la phase 1 : `cryptacular`
  référence encore une URL Mercurial Bitbucket (service arrêté en 2020).
- Ajout d'un workflow de CI « smoke » (`python:3.6-buster` : `compileall` sur
  `novaideo` + vérification des métadonnées de packaging) ; le build legacy
  complet est le livrable de la phase 1.
- Exclusion des artefacts de livraison (`*.patch`, `*.diff`, archives) et des
  résidus de `git apply` via `.gitignore`.
- Mise en place de la structure de documentation bilingue (`docs/en`,
  `docs/fr`) et de ce fil de l'eau.
- Restauration des changements de maintenance du fork : le commit initial
  (8883913) ne contenait que le fichier de patch de livraison, *non
  appliqué* — la commande d'application référençait
  `../kuneagi-fork-maj.patch` alors que le fichier avait été enregistré dans
  le dépôt ; la chaîne `&&` s'est arrêtée au `--check` et le fichier orphelin
  a été commité seul. Le contenu du patch est désormais appliqué et le
  fichier orphelin supprimé (et ignoré à l'avenir).


## 2026-07-14

- Lancement du « golden master » applicatif (phase 1) : un nouveau workflow
  `golden-master` reconstruit l'image Docker historique (le Dockerfile
  exécute le buildout complet pendant le `docker build`, avec les
  épinglages d'époque que le projet portait déjà : setuptools 42,
  zc.buildout 2.13.3) puis rejoue `bin/test -s novaideo`.
- Correctifs d'époque appliqués au Dockerfile : sources apt de Debian
  stretch repointées vers archive.debian.org (stretch archivée) ; dépôt
  packagecloud varnish 4.1 rendu best-effort avec le varnish de la
  distribution en repli (la suite de tests n'utilise pas varnish) ;
  `cryptacular` préinstallé depuis sa réécriture 2.x maintenue — même
  mécanisme de préinstallation pip que l'image historique pour la 1.5.5 —
  avec `bcrypt`/`cffi`/`pycparser` épinglés dans `versions.cfg` ; la source
  Mercurial Bitbucket morte remplacée par le dépôt maintenu. Chantier
  itératif attendu, comme pour les CI des bibliothèques.
- Itération 1 du golden master (build local) : apt sur la stretch archivée
  télécharge bien mais `upgrade -y` refuse les paquets — les clés de
  signature de stretch ont *expiré* (EXPKEYSIG), et Check-Valid-Until ne
  neutralise que le contrôle de date du Release, pas la vérification de
  signature. Les sources d'archive sont désormais marquées `[trusted=yes]`
  (compromis assumé et documenté pour une CI legacy figée). Montée
  préventive de pip en <22 dans l'image : le pip 19 de stretch est
  antérieur aux tags manylinux2014 des wheels bcrypt/cffi.
- Alignement complet sur Docker Compose v2 (`docker compose`) : correction
  de `run.sh`, où un remplacement global antérieur avait aussi mangé le
  *nom de fichier* (`-f docker compose-dev.yml`), cassant toutes les
  commandes enveloppées ; cible de l'attach rendue indépendante du nommage
  via `docker compose ps -q` (v2 nomme les conteneurs avec des tirets, pas
  des tirets bas) ; conversion des commandes `docker-compose` restantes du
  README ; suppression de l'attribut obsolète `version: '2'` des quatre
  fichiers compose (v2 le signale en avertissement).
- Itération 2 du golden master : `./run.sh rebuild` construit l'image avec
  `run_buildout=false` (le buildout doit tourner ensuite, hors build, avec
  le volume de cache monté), mais la ligne historique
  `RUN $run_buildout && bin/buildout` court-circuite en exit 1 quand
  l'argument vaut false — le `|| true` qui la rendait viable avait été
  commenté. Remplacée par un `if` explicite, qui garde aussi fatals les
  vrais échecs de buildout quand l'argument vaut true (le chemin du
  workflow golden-master). Correction du piège suivant dans
  `do_buildout()` : le nom d'image par défaut utilisait encore le nommage
  v1 à tiret bas (`kuneagi_novaideo`) — v2 construit `kuneagi-novaideo`.
- Itération 3 du golden master, et le jalon qui va avec : **le buildout
  complet de l'application est passé** — 194 épinglages, checkouts
  mr.developer, cryptacular 2.0 — première reconstruction intégrale depuis
  mars 2023. L'échec restant était dans l'étape de copie du cache de
  `run.sh`, un idiome docker de 2016 : `docker run -i -a stdin` (sans `-d`)
  imprimait l'id du conteneur sur stdout ; le docker moderne n'imprime rien
  dans ce mode, laissant `$id` vide (« invalid container name or ID: value
  is empty », puis l'erreur bash `test` ligne 27). Remplacé par une paire
  explicite `docker create` / `docker start -i -a`, sémantique identique
  (tar streamé vers un conteneur u1000, propriété des fichiers préservée).

- Extracteur BPMN→mermaid (`tools/bpmn2mermaid.py`, `ast` de la stdlib,
  tourne en 3.6 et 3.12) : analyse statiquement tous les
  `definition.py` (aucun import du moteur nécessaire) et génère une page
  Markdown par module de définition — flowchart mermaid par processus
  (formes façon BPMN : événements en cercles, passerelles XOR/AND en
  losanges, sous-processus en sous-routines avec leur définition cible,
  timers/conditionnels avec leur callable d'échéance/prédicat,
  conditions et `sync` en étiquettes d'arêtes) plus une table
  nœuds/behaviors. 38 modules de définition, 43 processus extraits sous
  `docs/en/processes/` et `docs/fr/processes/` (index compris). Les
  diagrammes montrent les graphes tels qu'écrits ; la normalisation du
  moteur peut ajouter un câblage synthétique. Le sous-processus de
  travail composé à l'exécution est étiqueté `(dynamic)`.

- Patch de caractérisation des cinq échecs du golden master (tous dans
  `TestIdeaManagement`). Deux causes racines, toutes deux des
  **évolutions fonctionnelles, pas des régressions** : (1) la
  modération individuelle de 2017 (un Moderator pressant
  publish_moderation/archive sur une idée 'submitted') a été remplacée
  par la *modération communautaire* — `SubmitIdea.start` tire jusqu'à
  ELECTORS_NB (3) membres actifs au hasard (auteur exclu ;
  `get_random_users` retourne *tous* les disponibles s'ils sont moins
  de 3) et ouvre un scrutin 'ideamoderation', avec un repli explicite :
  aucun électeur éligible, publication immédiate. Le bac à sable ne
  contient aucun membre hors l'auteur : le repli se déclenchait
  toujours. (2) la fusion du vocabulaire du site qu'affirmaient les
  tests create_and_publish passe par le `_tree` de l'idée
  (`root.merge_tree`) depuis que la migration keywords→tree (63a01248,
  2016-11) s'est achevée — l'argument plat `keywords=` du constructeur
  ne l'alimente plus.
- Les quatre tests de modération gardent leurs noms et photographient
  désormais le repli (paire d'états, `published_at`, absence des nœuds
  de décision, substitution 'moderationarchive') ; les ensembles
  d'actions exacts sont remplacés par des sous-ensembles
  indispensables, à resserrer une fois au vert. Un test nouveau,
  `test_submit_idea_moderation_conf_with_electors`, photographie le
  chemin nominal : trois membres ajoutés, l'idée reste 'submitted' et
  gagne une entrée `ballot_processes`.
- Note d'archéologie : le mécanisme a pris forme depuis 202a2849
  (30/11/2016, « adapt moderation ») jusqu'à l'ère KuneAgi ; les tests
  de mai 2017 décrivent le flux antérieur.

- Caractérisation, itération 2 (26/29 verts au premier run — le chemin
  du scrutin lui-même a fonctionné, l'erreur frappait *après*
  ``start_ballot``) : les ensembles d'actions sont désormais épinglés
  sur la réalité observée — le nœud 'moderationarchive' de 2017
  **n'existe plus nulle part dans la base de code** (la modération des
  contenus publiés est passée au processus des signalements), l'idée
  publiée offre donc l'ensemble de six actions que le message d'échec
  affichait, affirmé exactement dans les quatre tests concernés. Le
  test à électeurs crée désormais l'idée avec un auteur *Person* : la
  branche scrutin envoie un mail à l'auteur (``author.user_locale``),
  ce que le User admin substanced du bac à sable n'a pas — un écart
  harnais/réalité, documenté dans le test.

- **Golden master certifié** : `./run.sh test -s novaideo` → 29 tests,
  0 échec, 0 erreur, 0 sauté sur la pile 2017 reconstruite. La suite
  dit désormais la vérité actuelle du logiciel : les 23 tests
  d'origine, quatre caractérisés (modération communautaire et son repli
  sans électeurs ; fusion du vocabulaire par l'arbre), et le nouveau
  test du scrutin nominal. Le bloc Alice, intouché, est passé tel
  quel : la sémantique support/oppose des membres est stable depuis
  2017. Suite : déclencher le workflow GitHub `golden-master`
  (workflow_dispatch) pour le certificat CI reproductible ; la phase 3
  (portage Python 3.12, réacteur asyncio, fork substanced) s'ouvre,
  mesurée contre cette suite.

- **La phase 3 s'ouvre.** Le plan de portage est écrit
  (`docs/fr/phase3-porting-plan.md`) : Python 3.12 sur dépendances
  maintenues, mesuré contre la suite certifiée 29/29 sur les deux
  piles ; continuité ZODB en règle dure (une classe persistante ne
  bouge jamais — le renommage un temps envisagé de `Transaction` est
  rejeté sur preuve : elle dérive de `Persistent` et est stockée sur
  chaque processus) ; substanced forké à sa surface d'usage mesurée ;
  le réacteur porté sur asyncio derrière la même API publique ; jalons
  de bas en haut M0–M5 (dace → pontus → daceui → KuneAgi 29/29 →
  répétition de migration de données). Faits d'ancrage mesurés
  aujourd'hui : les quatre bases compilent déjà en 3.12.3 ; la surface
  d'import substanced est inventoriée ; un reliquat py2 confirmé
  (pontus `view_operation.py:724`) est planifié à M2.

- Effet de bord de la phase 3 / M1, appliqué ici pour protéger le
  golden master : les trois checkouts de bibliothèques sont désormais
  **épinglés par révision** dans `sources.cfg` (dace/pontus/daceui à
  leurs SHAs certifiés). Le `master` de dace passe à Python 3.12
  (réacteur asyncio, 88/88 verts sur la pile moderne — voir le fil de
  l'eau de dace) ; la preuve 3.6 vit sur le tag `legacy-golden-master`
  de dace. L'ordre des opérations compte : taguer d'abord le master
  pré-M1 de dace, puis pousser dace M1, puis cet épinglage — la
  relance du workflow golden-master est le contrôle.

- **Phase 3 / M4 : la suite du golden master est verte sur
  Python 3.12 — les mêmes 29 tests, 0 échec, 0 erreur** (1 min 57 sur
  la pile moderne), le harnais restant bi-pile pour que le conteneur
  legacy garde ses 29/29 sur le même arbre de travail. Modifications
  applicatives : deux shims d'une ligne. Le reste fut de l'archéologie
  de dépendances, documentée dans `constraints-modern.txt` : les sept
  « fossiles » (velruse, keas.kmi, cipher.encryptingstorage, yampy2,
  ovh, pyramid-sms, pyramid_retry) s'installent tous encore ;
  `graphql-wsgi` a été retiré de PyPI et vient de sa source
  (faassen) ; `html_diff_wrapper` reçoit un fork maintenu (py3.11
  interdit le drapeau `(?u)` en cours de motif) ; le schéma GraphQL est
  d'ère graphene 1, et `tools/patch_graphql1_py312.py` porte la pile
  d'époque installée (collections.abc) — 10 fichiers, mécanique,
  idempotent — utilisé par tox et le nouveau workflow `py312-tests`.
  L'acceptation se clôt quand la relance du workflow golden-master
  confirme le côté legacy.

- La configuration du harnais est désormais entièrement versionnée
  (demande utilisateur) : l'environnement de développement intégré
  Python 3.12 dans lequel M1-M4 ont été certifiés se reconstruit par
  `tools/bootstrap-modern.sh` — checkouts frères en editable s'ils sont
  présents, masters git sinon, les pins certifiés, et le portage de
  l'ère graphene 1 appliqué. Documenté dans
  `docs/{en,fr}/modern-harness.md`, qui nomme aussi les deux étages
  déjà versionnés : les `testing.py` bi-pile et le triplet
  tox/constraints/CI de chaque dépôt.

- **Phase 3 / M5 : la répétition de migration de données RÉUSSIT sur
  une vraie copie de production.** Chaîne complète prouvée le
  16/07/2026 : déchiffrement côté serveur (pile d'époque assemblée par
  ZConfig, clés jamais sorties de l'hôte), 79 269 enregistrements
  100 % en clair ; balayage intégral — **381 classes, 0 broken, 0
  inchargeable** (dix ans de pickles, état du moteur compris) ; le
  vrai `novaideo.main` démarre sur les données sans réacteur
  (`dace.wosystem`, DummyMailer) ; la chaîne d'évolution est un
  **no-op** (73 finies, 0 non finie sur le code moderne) ; les
  requêtes sur index d'époque répondent ; la réindexation intégrale
  des 61 index laisse chaque compte identique ; pack et balayage final
  stables. Livrables : `tools/m5_rehearsal.py` (phasé, agrégats
  seulement, codes de sortie durs), `tools/decrypt_copy.py`
  (l'extracteur côté serveur et ses deux leçons payées : les transform
  storages déchiffrent sur load, pas à l'itération ; le wrapper
  d'époque est un checkout patché — laisser ZConfig l'assembler), et
  le mode opératoire bilingue `docs/{en,fr}/m5-migration-rehearsal.md`.
  Constat côté production consigné : dérive de la configuration de
  chiffrement (64 987 enregistrements chiffrés contre 14 282 en
  clair ; blobs jamais chiffrés) — un audit est recommandé.

- **Mode opératoire de migration de production livré** (demande
  utilisateur) : gel + repozo + extraction-déchiffrement sur l'ancien
  hôte, porte de répétition (`REHEARSAL PASSED` exigé sur la copie
  même qu'on promeut), environnement cible via `bootstrap-modern.sh`,
  puis le **réveil contrôlé** : les premiers boots font tourner le
  vrai réacteur avec les sorties *écrites sur disque*
  (`pyramid_mailer.debug` → `var/mail-out/` ; `DummySMSService`) pour
  qu'un humain dépouille ce que dix ans de timers expirés déclenchent
  avant d'écrire au moindre membre. Fournit
  `etc/production-modern.ini.example` (profils réveil et réel,
  `tm.annotate_user=false` obligatoire) et
  `novaideo/utilities/dummy_sms.py`. Retour arrière = l'ancien
  conteneur intact.
- **Campagne de tests unitaires ouverte, mesurée d'abord** : baseline
  de couverture — dace 91 %, pontus 63 % (widget.py 38 %,
  view_operation.py 51 %, file/*), daceui 67 % (util 56 %, views
  54 %), novaideo **56 %** (39 172 instructions ; gisement de
  fonctions pures : french_dates_parser 16 %, pseudo_react 15 %,
  ical_date_utility 18 %, utilities/util 22 %). La première passe vise
  les modules purs (sans harnais lourd), puis les branches
  widget/view-operation de pontus.

- **T1 (campagne de tests unitaires) : le parseur de dates françaises
  est épinglé.** Deux nouveaux modules unittest purs (sans harnais
  fonctionnel, 16 tests, exécutés sur les deux piles) :
  `test_french_dates_parser.py` et `test_ical_date_utility.py` —
  caractérisation sous la référence figée du module lui-même
  (`mockLocalTime`, 15/05/2006). Couverture : french_dates_parser
  **16 % → 57 %**, ical_date_utility **18 % → 41 %** ; suite complète
  45/45 verte. Faits de contrat épinglés : l'article majuscule ancre
  la grammaire (`Du`/`Le` ; minuscule → None), les années explicites
  sont hors de la forme `Du..au..`, `getRangJour` capture le jour mais
  pas le rang, les helpers `occurences_*` sont paresseux et `is_ints`
  signifie timestamps entiers. Et les sondes **ont affûté le bug
  d'en-tête de 2006** : « sauf le <jour> » exclut toutes les
  occurrences intérieures mais LES DEUX BORNES échappent au filtre —
  le repro de 2016 n'en exposait que la moitié ouvrante (sa clôture
  tombait un jeudi). Épinglé tel quel ; corriger le parseur devra
  retourner ces assertions consciemment.

- **T1b : la veine pure d'`utilities/util` est épinglée** (18 tests)
  plus les deux helpers purs de `pseudo_react` (2 tests ; les
  composeurs de métadonnées exigent le harnais fonctionnel — reportés
  en batch dédié). Couverture : utilities/util **22 % → 32 %** ; suite
  complète **65/65** verte. Bizarreries de contrat épinglées :
  `combinaisons` concatène des chaînes ; `word_frequencies` produit
  des tuples `(compte, mot)` ; `guess_extension` répond sans point
  pour les types natifs ('png') mais AVEC le point pour les types
  enregistrés ('.kat'), repli 'file' ; `get_files_data` ne garde que
  les images ; `to_localized_time` retourne les gabarits `${...}` non
  traduits (épinglage déterministe du choix de branche) et lève
  KeyError sur un format inconnu ; `truncate_text` coupe en pleine
  URL. Un cycle d'import historique documenté (pseudo_react ↔
  views/__init__) : les tests l'amorcent dans l'ordre applicatif.

- **Réparation CI, pilotée par les preuves (triage via token GitHub).**
  L'incendie tenait en UN lieu : KuneAgi (dace/pontus/daceui tous
  verts). Deux causes racines, prouvées sur pièces et corrigées :
  (1) **golden-master rouge depuis le commit M4** : retirer
  `graphql-wsgi` des requires l'a aussi retiré de ce que le buildout
  legacy installe depuis le cache d'eggs d'époque — crash d'import au
  scan. Correctif : le requirement revient **conditionnellement**
  (`sys.version_info < (3,7)`) ; la pile moderne continue de
  l'installer depuis la source.
  (2) **py312-tests jamais vert** : un résolveur à froid a exposé ce
  que le venv au long cours masquait — dérive amont (substanced
  `1.0.post1` tirant pyramid 2.1), conflit d'époque insoluble
  (graphene 1.4.2 épingle promise<2.1 contre notre contrainte ==2.3)
  et tir ami (demande URL-sans-sha contre contrainte URL-avec-sha).
  Correctifs : CHAQUE ligne pip tourne désormais sous
  `constraints-modern.txt` ; promise reste au pin d'époque (2.0.2) et
  `tools/patch_graphql1_py312.py` le porte aussi ; `graphql-wsgi` est
  demandé par nom nu (la contrainte porte l'URL épinglée).
  Deux bogues latents sont tombés de la reproduction : l'outil de
  portage était localisé en IMPORTANT les paquets mêmes qui crashent
  avant portage (paradoxe d'amorçage) — les appelants localisent
  désormais via `sysconfig` sans importer ; et `lxml`, installé à la
  main pendant M4, est maintenant un requirement déclaré. Preuve
  d'or : depuis un venv vierge, la séquence CI exacte installe vert et
  passe **65/65** en 1 min 37.

- **T2a : les composeurs de métadonnées de `pseudo_react` sont
  épinglés en fonctionnel** — une seule application réelle (le harnais
  M4), des asserts de payloads derrière : les deux tables de dispatch
  (121 getters, 16 compteurs — tous appelables, format des clés
  vérifié), la branche sans action, et le contrat de payload de quatre
  familles d'actions d'idée (`abandon` avec son alerte et son
  `objects_to_hide` exact calculé sur l'oid ; la forme minimale de
  `duplicate` ; `edit`/`publish` avec `is_excuted` — la graphie
  historique fait partie du contrat) plus trois compteurs
  ('Ideas (0)', item_nb, propositions vides). Convention épinglée :
  dans la signature des composeurs, `api` est la *vue* appelante —
  seul `params(name)` est consommé. 7 tests, verts au premier run
  grâce à la méthode sonder-puis-épingler.

- **T2a élargi : le cycle de vie a ouvert six familles de plus** —
  piloter la publication, un second membre (alice) et un vrai
  commentaire/une vraie question a dévoilé ce que le sandbox neuf
  cachait. Épinglés : les ensembles d'actions EXACTS dépendant du rôle
  (un membre simple gagne support/oppose ; seul l'auteur du
  commentaire a edit/remove) ; la famille `footer_action`
  (comment/present : titres, icônes, compteurs d'items, et
  l'identifiant de composant bâti sur l'oid de L'ACTION — pas du
  canal, comme une première dérivation fausse l'a enseigné) ; la
  famille `support_action` (alertes interpolées au titre,
  `counters-to-update: mysupports`) ; `select` minimal ; le quatuor
  commentmanagement (edit porte `status`, pin rejoint la famille
  redirect, respond compte 1) ; le flux question (creat → ensemble de
  9 getters, answer/archive en famille redirect). 13 tests dans le
  module ; suite complète **78/78** verte.

- **Rafraîchissement documentaire (post-phase 3, post-campagne).** Le
  README énonce la réalité bi-pile (legacy certifié + Python 3.12 dans
  le même arbre, 78 tests, deux CI vertes) ; CHANGES consolide la
  réparation CI et les premiers lots de la campagne de tests ; le plan
  de portage porte un bandeau EXÉCUTÉ (M0→M5, répétition réussie) ; le
  document du harnais moderne gagne la section de durcissement
  post-réparation (contraintes partout, graphql-wsgi par nom nu, trio
  graphene d'époque, localisation sysconfig, lxml déclaré, requirement
  legacy conditionnel).

- **Le runbook de migration de production rejoint le dépôt** (ses
  compagnons de code — gabarit de réveil et puits SMS — étaient déjà
  poussés ; la référence de l'en-tête du ini résout désormais).
  Bilingue, conditionné à REHEARSAL PASSED, profil de réveil d'abord,
  observation en agrégats seulement, rollback par construction.

- **T4 (première tranche) : le cycle de vie du processus question est
  épinglé** — le plus gros ensemble de règles non testé (1 049 lignes
  de behaviors) désormais à **81 %** par 9 tests de niveau behavior
  (content/question.py 74 %, les vues de la famille entraînées en
  effet de bord). Contrats épinglés : `creat` publie avec l'état
  DOUBLE `['pending', 'published']` ; gardes par rôle exactes (extras
  auteur/admin `{edit, archive, seehistory}` sur la question ;
  `{archive}` seul sur la réponse d'autrui) ; répondre lève une alerte
  AU ROOT (magasin central) ; soutenir ne consomme AUCUN jeton
  personnel et bascule `support` en `withdraw_token` (retrait
  symétrique épinglé) ; VALIDER une réponse ferme la question (cascade
  inter-objets `['validated', 'published']` /
  `['closed', 'published']`) ; `archive` EXIGE une `explanation`
  (KeyError sinon), alerte, et effondre les gardes (membres : ensemble
  vide ; admin : le quintette avec `delquestion` qui apparaît). Suite
  complète **87/87** verte.

- **T4b : le cycle de vie de la personne est épinglé** — le cœur
  sécurité d'`user_management` (885 instructions de behaviors,
  jusqu'ici sans test) atteint **50 %** par 9 tests de niveau behavior
  (content/person.py 47 %) ; suite complète **96/96** verte. Contrats
  épinglés : un membre neuf est `['active']` avec
  `['Member', 'Owner']` ; gardes exactes (les extras admin incluent
  `discuss` — on ne discute pas avec soi-même) ; `deactivate` effondre
  les gardes au quatuor `{seehistory, activate, see, see_notations}`
  et `activate` restaure ; `assign_roles` EXIGE `roles` et REMPLACE
  l'ensemble assignable (Member disparaît, la relation Owner est
  préservée) ; `Edit.start` exige le mapping IMBRIQUÉ
  `change_password` — le mode sans-changement garde le mot de passe
  mais tamponne `modified_at`, le mode changement avec le mot de passe
  courant correct le bascule ; `get_api_token` exige le mot de passe
  et pose un jeton de 32 caractères derrière un HTTPFound ; `quit` est
  une DEMANDE, pas l'acte (l'état reste `['active']` jusqu'à la
  confirmation par courriel).

- **T4c : le cycle de vie des invitations est épinglé** — le parcours
  d'entrée (360 instructions de behaviors, jusqu'ici sans test)
  atteint **76 %** par 7 tests de niveau behavior
  (content/invitation.py 80 %) ; suite complète **103/103** verte.
  Contrats épinglés : `invite` prend
  `{'invitations': [{'_object_data': Invitation}]}` et estampille
  chacune (état `['pending']`, manager = l'invitant, `__name__`
  jeton aléatoire, rôles par défaut `['Member']`) ; les gardes
  S'INVERSENT de part et d'autre du lien de courriel (admin :
  `{edit, remind, remove, seeinvitation}` ; anonyme :
  `{accept, refuse, seeinvitation}`) ; `accept` exige le mot de
  passe, crée la Person DEPUIS les données de l'invitation (active,
  rôles de l'invitation plus Owner), RETIRE l'invitation du root et
  la relie en retour par `invitation.person` ; `refuse` est le
  jumeau asymétrique — conservée au root, marquée `['refused']`, les
  actions anonymes s'effondrant sur `seeinvitation` ; le `remove`
  admin supprime une invitation en attente purement et simplement.

- **L'arc Registration est épinglé — et une RÉGRESSION DE
  MODERNISATION corrigée** : l'API mot de passe de substanced a dérivé
  (`pwd_manager` → staticmethod `hash_new_password`), crashant le
  constructeur de `Preregistration` sur 3.12 ; `person.py` honore
  désormais l'un ou l'autre, prouvé par `check_password` sur toute la
  chaîne. 7 tests ; suite complète **110/110** verte. Épinglés : la
  `registration` anonyme au root, fermée par `only_invitation` (et
  l'override SiteAdmin de niveau dace qui montre toutes les actions,
  épinglé au passage) ; le constructeur encode le mot de passe
  immédiatement (bcrypt, jamais le clair) ; l'estampillage (état
  `['pending']`, nom-jeton, échéance = création + 4 jours) ; les
  gardes (l'anonyme ne tient QUE `confirmregistration` ; l'admin le
  quintette avec remind/remove) ; la confirmation créant la Person
  (clé `name_chooser` `'Bob-B'`, active, Member+Owner, redirection
  auto-login) et retirant la préinscription ; l'expiration fermant
  toute garde anonyme ; le `remove` admin net. Idiome de harnais
  consigné : l'abonné d'audit substanced (LoggedIn) lit
  `request.context` — le poser sur la requête de test.

- **Le cycle signalement/modération est épinglé** — la machinerie de
  sûreté sociale de `reports_management` (207 instructions de
  behaviors) atteint **85 %** par 6 tests de niveau behavior
  (content/report.py 80 %, les adaptateurs de signalement entraînés à
  ~47 %) ; suite complète **116/116** verte. Contrats épinglés :
  `report` est réservé aux MEMBRES (pas d'anonyme) et gardé sur l'état
  `published` ; signaler ajoute `'reported'`, dépose le rapport
  (`['pending']`, signaleur en auteur) et DÉMARRE le scrutin
  `contentreportdecision` (le tirage des modérateurs exclut l'auteur
  du contenu), le signalement restant disponible tant qu'aucun scrutin
  fini valide n'existe ; `censor()` REMPLACE tout l'état du contenu
  par `['censored']` (l'adaptateur `ISignalableObject`) et traite les
  rapports en attente ; `restor` est réservé aux MODÉRATEURS depuis
  `censored` et restaure les états de publication d'origine ;
  `ignore()` retire `'reported'` et traite les rapports ; le
  référentiel des motifs est fermé (clé inconnue → KeyError). Faits de
  harnais consignés : l'auteur du contenu doit être une vraie Person
  (`user_locale`), et l'import du module de behaviors exige l'amorçage
  du cycle historique (`import novaideo.views` d'abord).

- **Pause documentaire (post-campagne).** Le README porte la réalité
  des 116 tests et les cinq familles épinglées ; CHANGES consolide les
  lots familles-de-processus ; le document du harnais moderne gagne
  les idiomes de tests de niveau behavior fixés par la campagne.

- **Le scrutin `contentreportdecision` est conduit jusqu'à son
  verdict** — l'approfondissement du cycle de signalement : 6 tests,
  suite complète **122/122** verte (désormais certifiée en deux
  moitiés — tronc historique + premiers lots, puis les six suites de
  cycles de vie — la passe unique a dépassé une invocation).
  Couverture de la machinerie de scrutin : behaviors du référendum
  **100 %**, définition content_ballot 99 %, ballot_processes 83 %,
  behaviors des reports **85 % → 91 %**. Épinglés : le tirage des
  électeurs n'exclut QUE l'auteur du contenu (la signaleuse EST
  jurée), chaque électeur reçoit `('LocalModerator', contenu)` et un
  scrutin Référendum est attaché ; l'action `referendumprocess.vote`
  apparaît sur le contenu pour les seuls électeurs, disparaît une fois
  le bulletin déposé, et exige la clé `vote` ; majorité CONTRE →
  censure (`['censored']`, rapports traités), majorité POUR → ignore
  (publication intacte) ; chaque verdict révoque les rôles
  LocalModerator et un scrutin fini valide BLOQUE le re-signalement —
  la seconde moitié du contrat anti-récidive. Fait d'architecture
  consigné honnêtement : le nœud de décision se termine à l'ÉCHÉANCE
  du scrutin en production (le sous-processus de vote est fermé par
  minuterie via le `SubProcess.stop` sur mesure) ; les tests invoquent
  l'`after_execution` du nœud après le dernier bulletin — le chemin de
  code exact que l'échéance exécute.

- **La variante `moderate_registration` est épinglée — et le bug
  latent n°4 rejoint le registre** : le repli sans-électeurs n'a
  JAMAIS pu aboutir — il force `['accepted']` et envoie le courriel,
  puis meurt sur la ligne partagée `alert_user(...)` dont seule la
  branche scrutin lie `alert_data` (`UnboundLocalError`, présent dans
  la source historique importée ; l'ÉCRITURE DÉCHIRÉE est épinglée
  aussi — l'état est `['accepted']` après le crash). Les sites
  modérés exigent donc un vivier de membres disponible. 6 tests ;
  suite complète **128/128** (deux moitiés : 78 + 50) ; behaviors
  d'user_management **50 % → 61 %**. Contrats épinglés : sous
  modération la candidature reste `['pending']` avec un scrutin
  `registrationmoderation` attaché (tirage aléatoire parmi TOUS les
  membres), électeurs dotés de `('LocalModerator', préinscription)`
  et votant SUR la préinscription, la garde anonyme
  `confirmregistration` FERMÉE pendant l'attente ; l'acceptation
  remplace l'état par `['accepted']`, ouvre la garde, et le parcours
  d'entrée s'achève à travers la modération (la Person est créée) ;
  le refus SUPPRIME la candidature purement et simplement ; et les
  électeurs muets refusent — `ballot_result(self)` prend False par
  défaut ici, l'asymétrie de miséricorde avec la décision de
  signalement dont le silence vaut absolution.

- **Le bug latent n°4 est réparé, son test retourné en conscience.**
  La notification de mise-à-l'étude (`alert_data` liée au scrutin)
  rejoint la seule branche scrutin : le repli sans-électeurs de
  `moderate_registration` accepte désormais d'office et le parcours
  d'entrée s'achève jusqu'à la Person
  (`test_no_electors_fallback_accepts_at_once` garde la réparation).
  Suite complète **128/128** (deux moitiés : 78 + 50).

- **Fenêtre des renommages.** Les appels `pseudo_react` passent à
  l'`action_informations` de daceui ; `${nember}` devient `${number}`
  dans `see_notations` et à travers les catalogues (pot, fr, de — le
  `.mo` fr compilé patché en place par remplacement à longueur égale,
  le nouveau msgid vérifié résolvant sa traduction) ;
  `get_random_users(nember)` devient `number`. Suite complète 128/128
  (deux moitiés : 78 + 50).

- **Mise à jour documentaire (post-approfondissement).** Le README
  porte l'état final de campagne (128 tests, les deux scrutins
  conduits, quatre bugs latents et une régression — tous corrigés et
  gardés) ; CHANGES consolide l'approfondissement ; le harnais
  moderne gagne l'idiome de conduite de scrutin et la doctrine de la
  suite en deux moitiés.

- **Nova-Ideo 2.0 : le parent adopte le tronc modernisé.** README
  re-marqué (identité Nova-Ideo, section Filiation nommant le tronc de
  référence KuneAgi et l'intendance Logikascium) ; CHANGES porte
  l'entrée d'adoption. Appliqué sur le dépôt nova-ideo APRÈS la
  couture d'adoption (`-s ours` avec le tip 2020 en parent) — jamais
  sur le dépôt KuneAgi.
