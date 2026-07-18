# Nova-Ideo

**Golden master certified, port executed (2026-07):** the full 2017
stack rebuilds from scratch and its certified suite stays green — and
the same working tree now runs on **Python 3.12** (phase 3, milestones
M0→M5 complete, including a migration rehearsal on a real production
copy). The suite has since grown from 29 to **128 tests** through a
characterisation campaign that pinned the five process families of the
platform's social contract (question, person, invitation, registration,
report/moderation), then conducted BOTH moderation ballots to their
verdicts (content-report decision and moderated registration). Along
the way the campaign caught one modernisation regression (substanced's
password-API drift) and four latent bugs — **all fixed, each repair
guarded by its consciously flipped pinning test**; both CI pipelines
(legacy golden master and `py312-tests`) are green on every push
(see [`docs/en/worklog.md`](docs/en/worklog.md) and
[`docs/en/phase3-porting-plan.md`](docs/en/phase3-porting-plan.md)).

Nova-Ideo is a free (AGPL) participatory-innovation platform — the
merger of the ideas box and the collaborative portal. Members post
ideas and questions, organise idea challenges, form working groups
that co-write proposals through short timeboxed iterations (wiki,
validation or amendment modes), vote using majority judgment, and
support or reject published content with a limited number of tokens.

## Lineage

Nova-Ideo (Ecréall, 2014-2020) is the PARENT project of this code
line and served several deployments. Its
[KuneAgi](https://github.com/michaellaunay/KuneAgi) variant — the
reference trunk of the cooperative-governance branch — carried the
development from 2020 to 2023, then the full modernisation
(2026). This repository ADOPTS that modernised trunk as
**Nova-Ideo 2.0**: the historical 2010-2020 line remains reachable
underneath the adoption merge, and the few Nova-Ideo-specific changes
of 2016-2020 (nine files) are catalogued for selective review.
Maintained by Logikascium since 2024 (Ecréall's IP acquired).

The Python package inside this repository is still named `novaideo`: module paths are **frozen** to keep existing ZODB databases loadable (see the roadmap).

## Repository status

This repository is a **maintained fork** of [`ecreall/KuneAgi`](https://github.com/ecreall/KuneAgi) (Nova-Ideo lineage developed by Ecréall from 2014, KuneAgi-specific development until 2023), forked in July 2026 and maintained by Michaël Launay ([Logikascium](https://github.com/michaellaunay)). Per the Nova-Ideo modernisation audit (Logikascium, July 2026), **KuneAgi is the reference trunk** of the modernisation effort.

Intellectual property: the KuneAgi-specific developments are copyright **Cosmopolitical.coop** (rights transferred by Laurent Zibell); the underlying Nova-Ideo base is copyright **Logikascium** (Ecréall's intellectual property, acquired in 2024). The whole remains under the **AGPL v3+**, unchanged.

The `master` branch is **dual-stack**: the certified legacy container
(Python 3.6-era buildout) and the modern Python 3.12 harness
(`tox.ini`, `constraints-modern.txt`, `tools/bootstrap-modern.sh`)
live in the same tree and are both exercised by the CI on every push;
see [`docs/en/modern-harness.md`](docs/en/modern-harness.md), the
[roadmap](#roadmap--planned-updates) below and `CHANGES.md`.

## Translations

This product has been translated into: English, French, Deutsch.

## Documentation

Documentation lives in [`docs/`](docs/):

- [`docs/en/`](docs/en/) — primary documentation, in English
- [`docs/fr/`](docs/fr/) — documentation in French

Audits, design documents and the worklog are maintained in both languages. See [`docs/README.md`](docs/README.md) for the documentation policy. Dependency pins for the legacy build live in [`versions.cfg`](versions.cfg) (buildout).

## Getting started for development

### Without docker

To run in development mode without docker:

```bash
sudo apt-get install python3 python3-dev libxml2-dev libxslt1-dev \
  libjpeg-dev zlib1g-dev libfreetype6-dev libtiff5-dev libzmq3-dev \
  libyaml-dev git  # this was working on debian jessie and ubuntu xenial
python3 bootstrap.py
mkdir -p var/{filestorage,blobstorage,log}
bin/buildout  # It takes a long time...
bin/runzeo -C etc/zeo.conf  # Starts in foreground, no output. Ctrl+C to stop.
bin/pserve development.ini  # in another terminal
```

The application is on <http://127.0.0.1:6543>.

I'll use `$DOMAIN` for `http://127.0.0.1:6543` in the rest of the documentation.

To send emails with gmail smtp, you need to uncomment some lines and configure the mail and password in `development.ini`.

> **Note (2026):** the legacy build targets Python 3.6 on a Debian jessie-era system and is being repaired as Phase 1 of the roadmap ("golden master"). On this fork, `sources.cfg` already points `ecreall_dace`, `ecreall_pontus` and `ecreall_daceui` to their maintained forks; the `cryptacular` source still references a Mercurial Bitbucket URL (service discontinued in 2020) and will be fixed during Phase 1.

### With docker

You first need to install the [docker engine](https://docs.docker.com/engine/install/) with the [Compose plugin](https://docs.docker.com/compose/install/) (the `docker compose` command).

There is a current limitation for the `run.sh` script: the folder needs to be named `nova-ideo` or `novaideo`. And your user needs to be in the docker group:

```bash
usermod -a -G docker your_user
```

You need to log out and log in again for this to take effect.

To run in development mode with docker, as your regular user:

```bash
./run.sh rebuild
./run.sh
```

The app is deployed on <https://local.ecreall.com:8443> (`local.ecreall.com` resolves to 127.0.0.1 and is necessary for nginx).

I'll use `$DOMAIN` for `https://local.ecreall.com:8443` in the rest of the documentation.

The default configuration in `docker-compose-dev.yml` is used to connect with a postfix via a ssh tunnel like this:

```bash
ssh -L 172.17.0.1:9025:localhost:25 myserver.example.com
```

To send emails with gmail smtp instead, you need to configure the MAILER variables in `docker-compose.override.yml`: copy the file `docker-compose.override.yml.templ` to `docker-compose.override.yml` and edit it. This overrides the configuration in `docker-compose-dev.yml`.

To stop the application, do a Ctrl-C, and to stop the other containers (nginx), run:

```bash
./run.sh down
```

To execute the tests:

```bash
./run.sh test -s novaideo
```

## Allow your gmail account to be used to send emails

> **Note (2026):** Google has since removed the "less secure apps" option this section relied on. Use an app password or another SMTP provider; this section will be reworked in Phase 1.

To allow your gmail account to be used to send emails, you historically needed to enable [less secure apps](https://support.google.com/accounts/answer/6010255) (less secure means we use a login and password and not OAuth 2.0) and do maybe the [captcha](https://support.google.com/accounts/answer/6009563). Look at the logs in the terminal if you have an error when sending a mail.

If you have a G suite account, to be able to enable less secure apps for a specific account, the G suite administrator needs to first [enable it](https://support.google.com/a/answer/6260879).

Be careful to not commit your gmail password! The ini file doesn't support the use of the `%` character in your password — it thinks it's the beginning of a variable. If you use this character in your password, you will need to change it!

## How to assign roles to a person

If you want to give a person some additional roles, you need to have the *Administrator* or *Site administrator* role. The first time, you will need to do it with the special super administrator account. Go to `$DOMAIN/manage` (there is no accessible link from the home page) and authenticate with login `admin` and the password you have in the `SECRET` environment variable (it's the `substanced.initial_password` key in `development.ini` if you use the install without docker). Return to `$DOMAIN` and go to the hamburger menu on the top left, select *See/Members*, go to a person's profile, click on the *Assign roles* button and give her the *Site administrator*, *Examiner* or *Moderator* role.

## Deployment with docker

> **Note (2026):** the historical release images on Docker Hub (`ecreall/novaideo:release-VERSION`) are no longer maintained. Rebuilding the image locally (`./run.sh rebuild` or `docker compose build`) is the supported path until Phase 1 re-establishes releases.

Clone a specific version:

```bash
git clone -b VERSION https://github.com/michaellaunay/KuneAgi.git
cd KuneAgi
```

(replace VERSION with the latest release)

The compose configuration runs an nginx container on ports 80 and 443. You need to edit the `nginx-app-prod.conf` file to replace `mynovaideo.example.com` by your domain and add certificates (`server.key` and `server.crt`) to the `tls` directory.

Be sure that in `docker-compose.yml` it uses the correct version. Edit it if it's not the case.

You need to configure some environment variables: copy the file `docker-compose.override.yml.templ` to `docker-compose.override.yml` and edit it.

- `SECRET`: the initial admin password
- `APPLICATION_URL`: your domain, same as you put in `nginx-app-prod.conf`
- `MAIL_DEFAULT_SENDER`: the sender of the mails that the application uses
- `MAILER_HOST`: SMTP host
- `MAILER_PORT`: SMTP port
- `MAILER_USERNAME`: SMTP username
- `MAILER_PASSWORD`: SMTP password
- `MAILER_TLS`: use TLS
- `MAILER_SSL`: use SSL
- `LOGO_FILENAME`: empty by default to use the Nova-Ideo logo. You can set the variable to `marianne.svg` or other images included in the `novaideo/static/images/` directory to configure the logo when the application is created.

If you want to connect to a postfix container, there is a commented example in `docker-compose.override.yml.templ` that uses an external postfix container connected on a `mybridge` bridge network. You need to create a `mybridge` bridge network and start a postfix container yourself (not documented here).

To deploy:

```bash
sudo docker compose up -d
```

To connect with the super administrator (for the evolve steps and to create another admin account only), go to `https://mynovaideo.example.com/manage` and log in with `admin`; the password is the one you gave in the `SECRET` environment variable.

After the initial connection, you can increase the number of workers that are used to handle the requests in `docker-compose.override.yml` and run again `sudo docker compose up -d` (`WORKERS=3` is a good default).

To see the logs:

```bash
docker compose logs -f
```

## How to upgrade your install

For each release, a docker image is built and the `docker-compose.yml` is modified accordingly.

If you previously cloned the repository with version 1.1, to upgrade to 1.2 for example, do:

```bash
git checkout 1.2
sudo docker compose up -d
```

After that, be sure to execute the evolve steps by connecting with the super administrator at `https://mynovaideo.example.com/manage`, going to the *Database* tab, and clicking on the *Evolve* red button. You can see the evolve steps with the *Summarize* button.

## Backup and maintenance of your database

Your data is in the `var` folder, be sure to back it up.

The database is a ZODB filestorage, you should pack it regularly (every week) to reduce its size. Example of cron for user root run at 1am sunday:

```
0 1 * * 0 docker exec kuneagi-novaideo-1 /app/bin/zeopack -d 1 -u /app/var/zeo.sock
```

Be sure that the container name matches in your case (Compose v2 uses dashes, e.g. `kuneagi-novaideo-1`). You can verify it with `docker ps`.

## Roadmap — planned updates

The plan follows the Nova-Ideo modernisation audit (Logikascium, July 2026); KuneAgi is its reference trunk.

1. **Phase 1 — Reproducible legacy build ("golden master").** Repair and freeze the buildout/Docker build, green CI replaying the existing test suite: the non-regression baseline. Until then, this repository's CI is a packaging/syntax smoke check only.
2. **Phase 2 — Exhaustive documentation.** Architecture documentation, catalogue of the business processes (auto-generated BPMN diagrams from the DaCE definitions), docstring pass, glossary.
3. **Phase 3 — Backend modernisation.** Python 3.12; Pyramid 2.x; ZODB 6; maintained substanced fork; removal or replacement of dead dependencies (velruse → standard OIDC, yampy2 → removed with the discontinued Yammer connector, xlrd → openpyxl, graphene 1.4 → graphene 3); pytest; PEP 621 packaging with `uv`; ruff; gradual typing. The server-rendered UI is kept unchanged in this phase.
4. **Phase 4 — Frontend.** Progressive rebuild on **SolidJS + TypeScript + Vite** over the GraphQL API (strangler-fig strategy: the Chameleon server-rendered UI stays in place while screens migrate one by one).
5. **Phase 5 — Data and operations.** Migration tooling for existing ZODB databases (evolve steps, `zodbupdate`); modern Docker images and CI/CD. Python module names (dotted paths, including the `novaideo` package name) are **frozen** to preserve existing ZODB pickles.

Reunification with the nova-ideo lineage into a single trunk (KuneAgi specifics as configuration profiles) is planned in coordination with Cosmopolitical.coop. Versioning: `1.4.dev` = legacy maintenance on this fork; `2.0.0` = the modernised application.

## Contribute

- Issue tracker: <https://github.com/michaellaunay/KuneAgi/issues>
- Source code: <https://github.com/michaellaunay/KuneAgi>
- Historical upstreams: <https://github.com/ecreall/KuneAgi> and <https://github.com/ecreall/nova-ideo>

## License

The project is licensed under the AGPL v3 or later (AGPLv3+). See [`LICENSE`](LICENSE) and the [Repository status](#repository-status) section for the copyright holders.
