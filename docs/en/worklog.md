# Worklog

Running log of the work on this repository, newest first.
Version française : [`../fr/worklog.md`](../fr/worklog.md).

## 2026-07-13

- Forked `ecreall/KuneAgi` to `michaellaunay/KuneAgi`; maintenance resumed by
  Michaël Launay (Logikascium). KuneAgi is the reference trunk of the
  Nova-Ideo modernisation (audit of July 2026).
- Converted `README.rst` and `CHANGES.rst` to Markdown; README retitled from
  "Nova Ideo" to "KuneAgi", rewritten with the repository status (copyright:
  Cosmopolitical.coop for the KuneAgi-specific work, Logikascium for the
  Nova-Ideo base; AGPL v3+ for the whole) and the modernisation roadmap;
  outdated operating instructions annotated (Google "less secure apps",
  historical Docker Hub images).
- Updated build metadata (`setup.py`: fork URLs, maintainer field, Markdown
  long description, Python 3.6 classifier); added a minimal PEP 518
  `pyproject.toml`; updated `MANIFEST.in`. Package name `novaideo` and module
  paths unchanged (ZODB pickles).
- `sources.cfg`: `ecreall_dace`, `ecreall_pontus`, `ecreall_daceui` repointed
  to their maintained forks. Known Phase 1 issue: `cryptacular` still points
  to a Mercurial Bitbucket URL (service discontinued in 2020).
- Added a smoke CI workflow (`python:3.6-buster`: `compileall` on `novaideo`
  + packaging metadata check); the full legacy build is the Phase 1
  deliverable.
- Ignored delivery artifacts (`*.patch`, `*.diff`, archives) and `git apply`
  leftovers in `.gitignore`.
- Established the bilingual documentation structure (`docs/en`, `docs/fr`)
  and this worklog.
- Restored the fork-maintenance changes: the initial commit (8883913)
  contained only the *unapplied* delivery patch file — the apply command
  referenced `../kuneagi-fork-maj.patch` while the file had been saved inside
  the repository, so the `&&` chain stopped at `--check` and the stray file
  was committed alone. The patch content is now applied and the stray file
  removed (and ignored from now on).


## 2026-07-14

- Started the Phase 1 "golden master" of the application: a new
  `golden-master` workflow rebuilds the historical Docker image (the
  Dockerfile runs the full buildout inside `docker build`, with the era pins
  the project already carried: setuptools 42, zc.buildout 2.13.3) and
  replays `bin/test -s novaideo`.
- Era fixes applied to the Dockerfile: Debian stretch apt sources repointed
  to archive.debian.org (stretch archived); the varnish 4.1 packagecloud
  repository made best-effort with the distro varnish as fallback (the test
  suite does not use varnish); `cryptacular` preinstalled from its
  maintained 2.x rewrite — same pip-preinstall mechanism the historical
  image used for 1.5.5 — with `bcrypt`/`cffi`/`pycparser` pinned in
  `versions.cfg`; the dead Mercurial Bitbucket source replaced by the
  maintained repository. Expected to be iterative, like the library CIs.
- Golden-master iteration 1 (local build): apt on the archived stretch
  fetched fine but `upgrade -y` refused the packages — the stretch signing
  keys have *expired* (EXPKEYSIG), and Check-Valid-Until only bypasses the
  Release date check, not signature verification. Archive sources are now
  marked `[trusted=yes]` (accepted, documented trade-off for a frozen
  legacy CI). Preemptively upgraded pip to <22 inside the image: stretch's
  pip 19 predates the manylinux2014 tags of the bcrypt/cffi wheels.
- Aligned everything on Docker Compose v2 (`docker compose`): fixed
  `run.sh`, where an earlier global replace had also mangled the *file
  name* (`-f docker compose-dev.yml`), breaking every wrapped command;
  made the attach target naming-agnostic via `docker compose ps -q`
  (v2 names containers with dashes, not underscores); converted the
  remaining `docker-compose` commands in the README; removed the obsolete
  `version: '2'` attribute from the four compose files (v2 warns on it).
- Golden-master iteration 2: `./run.sh rebuild` builds the image with
  `run_buildout=false` (the buildout is meant to run afterwards, outside
  the build, with the cache volume mounted), but the historical
  `RUN $run_buildout && bin/buildout` short-circuits to exit 1 when the
  arg is false — the `|| true` that made it pass had been commented out.
  Replaced by an explicit `if`, which also keeps real buildout failures
  fatal when the arg is true (the golden-master workflow path). Fixed the
  next trap in `do_buildout()`: the default image name still used the
  Compose v1 underscore naming (`kuneagi_novaideo`) — v2 builds
  `kuneagi-novaideo`.
- Golden-master iteration 3, and the milestone with it: **the full buildout
  of the application completed** — 194 pins, mr.developer checkouts,
  cryptacular 2.0 — the first complete rebuild since March 2023. The
  remaining failure was in `run.sh`'s cache-copy step, a 2016 docker idiom:
  `docker run -i -a stdin` (without `-d`) used to print the container id on
  stdout; modern docker prints nothing in that mode, leaving `$id` empty
  ("invalid container name or ID: value is empty", then the bash `test`
  error on line 27). Replaced by an explicit `docker create` /
  `docker start -i -a` pair, same semantics (tar streamed to a u1000
  container, ownership preserved).

- BPMN-to-mermaid extractor (`tools/bpmn2mermaid.py`, stdlib `ast`, runs
  on 3.6 and 3.12): statically parses every `definition.py`
  (no engine import needed) and generates one Markdown page per
  definition module — mermaid flowchart per process (BPMN-ish shapes:
  events as circles, XOR/AND gateways as diamonds, sub-processes as
  subroutines with their target definition, timers/conditionals with
  their deadline/predicate callable, conditions and `sync` as edge
  labels) plus a node/behaviors table. 38 definition modules,
  43 processes extracted under `docs/en/processes/` and
  `docs/fr/processes/` (indexes included). Diagrams show the graphs as
  authored; the engine normalisation may add synthetic wiring. The
  runtime-composed work sub-process is labelled `(dynamic)`.

- Characterisation patch for the five golden-master failures (all in
  `TestIdeaManagement`). Two root causes, both **feature drift, not
  regressions**: (1) the 2017 individual moderation (a Moderator
  pressing publish_moderation/archive on a 'submitted' idea) was
  replaced by the *community moderation* — `SubmitIdea.start` draws up
  to ELECTORS_NB (3) random active members (author excluded;
  `get_random_users` returns *all* available when fewer than 3) and
  opens an 'ideamoderation' ballot, with an explicit fallback:
  no eligible elector, immediate publication. The sandbox holds no
  member besides the author, so the fallback always fired. (2) the
  site-vocabulary merge asserted by the create_and_publish tests goes
  through the idea's `_tree` (`root.merge_tree`) since the
  keywords→tree migration (63a01248, 2016-11) settled — the flat
  `keywords=` constructor argument no longer feeds it.
- The four moderation tests keep their names and now photograph the
  fallback (states pair, `published_at`, absence of the decision
  nodes, 'moderationarchive' substitution); exact action sets are
  replaced by must-have subsets, to be tightened once green. A new
  test, `test_submit_idea_moderation_conf_with_electors`, photographs
  the nominal path: three members added, the idea stays 'submitted'
  and gains a `ballot_processes` entry.
- Archaeology note: the mechanism took shape from 202a2849
  (2016-11-30, "adapt moderation") into the KuneAgi era; the 2017-05
  tests describe the earlier flow.

- Characterisation, iteration 2 (26/29 green on the first run — the
  ballot path itself worked, the error hit *after* ``start_ballot``):
  the action sets are now pinned to the observed reality — the 2017
  'moderationarchive' node **no longer exists anywhere in the code
  base** (published-content moderation moved to the reports process),
  so the published idea offers the six-action set the failure message
  displayed, asserted exactly in the four concerned tests. The
  with-electors test now authors the idea as a *Person*: the ballot
  branch mails the author (``author.user_locale``), which the
  substanced admin User of the sandbox does not have — a
  harness-reality gap, documented in the test.

- **Golden master certified**: `./run.sh test -s novaideo` → 29 tests,
  0 failures, 0 errors, 0 skipped on the rebuilt 2017 stack. The suite
  now tells the current truth of the software: the 23 original tests,
  four characterised ones (community moderation with its no-elector
  fallback; tree-based vocabulary merge), and the new nominal-ballot
  test. The untouched Alice block passed as-is: member support/oppose
  semantics are stable since 2017. Next: trigger the `golden-master`
  GitHub workflow (workflow_dispatch) for the reproducible CI
  certificate; Phase 3 (Python 3.12 port, asyncio reactor, substanced
  fork) opens, measured against this suite.

- **Phase 3 opens.** The porting plan is written
  (`docs/en/phase3-porting-plan.md`): Python 3.12 on maintained
  dependencies, measured against the certified 29/29 suite on both
  stacks; ZODB continuity as a hard rule (a persistent class never
  moves — the once-considered `Transaction` rename is rejected on
  evidence: it derives from `Persistent` and is stored on every
  process); substanced forked to its measured used-surface; the
  reactor moved to asyncio behind the same public API; bottom-up
  milestones M0–M5 (dace → pontus → daceui → KuneAgi 29/29 →
  data-migration rehearsal). Grounding facts measured today: the four
  code bases already compile on 3.12.3; the substanced import surface
  is inventoried; one confirmed py2 remnant
  (pontus `view_operation.py:724`) is scheduled at M2.

- Phase 3 / M1 side-effect, applied here for the golden master's
  protection: the three library checkouts are now **pinned by
  revision** in `sources.cfg` (dace/pontus/daceui at their certified
  SHAs). dace's `master` moves to Python 3.12 (asyncio reactor,
  88/88 green on the modern stack — see dace's worklog); the 3.6 proof
  lives on dace's `legacy-golden-master` tag. Operation order matters:
  tag dace's pre-M1 master first, then push dace M1, then this pin —
  re-running the golden-master workflow is the check.

- **Phase 3 / M4: the golden-master suite is green on Python 3.12 —
  the same 29 tests, 0 failures, 0 errors** (1 min 57 on the modern
  stack), while the harness stays dual-stack so the legacy container
  keeps its 29/29 on the very same working tree. Application changes:
  two one-line shims. The rest was dependency archaeology, all
  documented in `constraints-modern.txt`: the seven "fossils" (velruse,
  keas.kmi, cipher.encryptingstorage, yampy2, ovh, pyramid-sms,
  pyramid_retry) all still install; `graphql-wsgi` was withdrawn from
  PyPI and comes from its source (faassen); `html_diff_wrapper` gets a
  maintained fork (py3.11 forbids the mid-pattern `(?u)` flag); the
  GraphQL schema is graphene-1-era, and `tools/patch_graphql1_py312.py`
  ports the installed era stack (collections.abc) — 10 files,
  mechanical, idempotent — used by tox and the new `py312-tests`
  workflow. Acceptance closes when the golden-master workflow re-run
  confirms the legacy side.

- The harness configuration is now fully versioned (user request): the
  integrated Python 3.12 development environment M1-M4 were certified
  in is rebuilt by `tools/bootstrap-modern.sh` — editable sibling
  checkouts when present, git masters otherwise, the certified pins,
  and the graphene-1 era port applied. Documented in
  `docs/{en,fr}/modern-harness.md`, which also names the two layers
  already versioned: the dual-stack `testing.py` files and the
  tox/constraints/CI triplet of every repo.

- **Phase 3 / M5: the data-migration rehearsal PASSED on a real
  production copy.** Full chain proven on 2026-07-16: server-side
  decrypt (ZConfig-assembled era stack, keys never leaving the host),
  79,269 records 100 % plain; full load sweep — **381 classes, 0
  broken, 0 unloadable** (a decade of pickles, engine state included);
  the real `novaideo.main` boots on the data reactor-less
  (`dace.wosystem`, DummyMailer); the evolution chain is a **no-op**
  (73 finished, 0 unfinished on the modern code); era-index queries
  answer; the full 61-index reindex leaves every count identical;
  pack and final sweep stable. Deliverables: `tools/m5_rehearsal.py`
  (phased, aggregates-only, hard exit codes), `tools/decrypt_copy.py`
  (the server-side extractor and its two paid-for lessons: transform
  storages decrypt on load, not on iteration; the era wrapper is a
  patched checkout — let ZConfig build it), and the bilingual runbook
  `docs/{en,fr}/m5-migration-rehearsal.md`. Production-side finding
  recorded: encryption-config drift (64,987 encrypted vs 14,282 plain
  records; blobs never encrypted) — an audit is advisable.

- **Production-migration runbook delivered** (user request): freeze +
  repozo + decrypt-extract on the old host, rehearsal gate
  (`REHEARSAL PASSED` required on the very copy being promoted),
  target env via `bootstrap-modern.sh`, then the **controlled
  wake-up**: first boots run the real reactor with outbound *written
  to disk* (`pyramid_mailer.debug` → `var/mail-out/`;
  `DummySMSService`) so a human reviews what a decade of expired
  timers fires before any member is mailed. Ships
  `etc/production-modern.ini.example` (wake-up and live profiles,
  `tm.annotate_user=false` mandatory) and
  `novaideo/utilities/dummy_sms.py`. Rollback = the untouched old
  container.
- **Unit-test campaign opened, measured first**: coverage baseline —
  dace 91 %, pontus 63 % (widget.py 38 %, view_operation.py 51 %,
  file/*), daceui 67 % (util 56 %, views 54 %), novaideo **56 %**
  (39,172 stmts; pure-function goldmine: french_dates_parser 16 %,
  pseudo_react 15 %, ical_date_utility 18 %, utilities/util 22 %).
  First pass targets the pure modules (no heavy harness), then the
  pontus widget/view-operation branches.

- **T1 (unit-test campaign): the French dates parser is pinned.** Two
  new plain-unittest modules (no functional harness, 16 tests, run on
  both stacks): `test_french_dates_parser.py` and
  `test_ical_date_utility.py` — characterisation under the module's
  own frozen reference (`mockLocalTime`, 2006-05-15). Coverage:
  french_dates_parser **16 % → 57 %**, ical_date_utility
  **18 % → 41 %**; full suite 45/45 green. Contract facts pinned: the
  capitalised article anchors the grammar (`Du`/`Le`; lowercase →
  None), explicit years are outside the `Du..au..` form, `getRangJour`
  captures the day but not the rank, the `occurences_*` helpers are
  lazy and `is_ints` means integer timestamps. And the probes
  **sharpened the 2006 header bug**: 'sauf le <jour>' excludes every
  interior occurrence but BOTH boundary days escape the filter — the
  2016 repro only exposed the opening half (its closing day was a
  Thursday). Pinned as-is; fixing the parser must flip those asserts
  consciously.

- **T1b: the pure vein of `utilities/util` is pinned** (18 tests) plus
  the two pure helpers of `pseudo_react` (2 tests; the metadata
  composers need the functional harness — moved to a dedicated batch).
  Coverage: utilities/util **22 % → 32 %**; full suite **65/65** green.
  Pinned contract oddities: `combinaisons` concatenates strings;
  `word_frequencies` yields `(count, word)` tuples; `guess_extension`
  answers dot-less for built-ins ('png') but WITH the dot for
  custom-registered types ('.kat'), falling back to 'file';
  `get_files_data` keeps images only; `to_localized_time` returns the
  untranslated `${...}` templates (deterministic format-branch pinning)
  and raises KeyError on unknown format ids; `truncate_text` cuts
  mid-URL. One historical import cycle documented (pseudo_react ↔
  views/__init__): tests prime it in application order.

- **CI repair, evidence-driven (GitHub token triage).** The fire was in
  ONE place: KuneAgi (dace/pontus/daceui all green). Two root causes,
  both proven on pieces and both fixed:
  (1) **golden-master red since the M4 commit**: removing `graphql-wsgi`
  from the requires also removed it from what the legacy buildout
  installs from the era egg cache — import crash at scan. Fix: the
  requirement returns **conditionally** (`sys.version_info < (3,7)`);
  the modern stack keeps installing it from source.
  (2) **py312-tests never green**: a fresh resolver exposed what the
  long-lived venv masked — upstream drift (substanced `1.0.post1`
  pulling pyramid 2.1) plus an unsolvable era conflict (graphene 1.4.2
  hard-pins promise<2.1 against our promise==2.3 constraint) plus a
  self-conflict (URL-without-sha request vs URL-with-sha constraint).
  Fixes: EVERY pip line now runs under `constraints-modern.txt`;
  promise stays on the era pin (2.0.2) and
  `tools/patch_graphql1_py312.py` also ports it; `graphql-wsgi` is
  requested by bare name (the constraint carries the pinned URL).
  Two latent bugs fell out of the reproduction: the porting tool was
  located by IMPORTING the very packages that crash before porting
  (bootstrap paradox) — callers now locate via `sysconfig` without
  importing; and `lxml`, hand-installed during M4, is now a declared
  requirement. Gold proof: from a clean venv, the exact CI sequence
  installs green and runs **65/65** in 1:37.

- **T2a: the `pseudo_react` metadata composers are pinned
  functionally** — one real application (the M4 harness), payload
  asserts behind: the two dispatch registries (121 metadata getters,
  16 counters — all callable, key format checked), the no-action
  branch, and the payload contract of four idea-action families
  (`abandon` with its alert and its exact `objects_to_hide` computed
  from the oid; `duplicate`'s minimal shape; `edit`/`publish` with
  `is_excuted` — the historical spelling is part of the contract) plus
  three counters ('Ideas (0)', item_nb, empty proposals). Convention
  pinned: in the composers' signature `api` is the calling *view* —
  only `params(name)` is consumed. 7 tests, first run green thanks to
  the probe-then-pin method.

- **T2a widened: the lifecycle unlocked six more families** — driving
  publish, a second member (alice) and a real comment/question opened
  what the fresh sandbox hid. Pinned: the exact ROLE-DEPENDENT action
  sets (a plain member additionally gets support/oppose; only the
  comment's author gets edit/remove); the `footer_action` family
  (comment/present: titles, icons, item counters, and the component id
  built on the ACTION's own oid — not the channel's, as a first wrong
  derivation taught); the `support_action` family (title-interpolated
  alerts, `counters-to-update: mysupports`); minimal `select`; the
  commentmanagement quartet (edit carries `status`, pin joins the
  redirect family, respond counts 1); the question flow (creat →
  9-getter set, answer/archive in the redirect family). 13 tests in
  the module; full suite **78/78** green.

- **Documentation refresh (post-phase-3, post-campaign).** README now
  states the dual-stack reality (certified legacy + Python 3.12 in the
  same tree, 78 tests, both CIs green); CHANGES consolidates the CI
  repair and the first test-campaign batches; the porting plan carries
  an EXECUTED banner (M0→M5, rehearsal passed); the modern-harness
  document gains the post-repair hardening section (constraints
  everywhere, bare-name graphql-wsgi, era graphene trio, sysconfig
  locate, declared lxml, conditional legacy requirement).

- **The production-migration runbook joins the repository** (its code
  companions — the wake-up template and the SMS sink — were already
  pushed; the ini header's reference now resolves). Bilingual, gated
  on REHEARSAL PASSED, wake-up profile first, aggregate-only
  observation, rollback by construction.

- **T4 (first slice): the question-process lifecycle is pinned** — the
  largest untested rule set (1 049 behaviour lines) now at **81 %**
  through 9 behaviour-level tests (content/question.py 74 %, the
  family's views dragged along as side effects). Pinned contracts:
  `creat` publishes with the DUAL state `['pending', 'published']`;
  exact role gates (author/admin extras `{edit, archive, seehistory}`
  on the question; `{archive}` alone on someone else's answer);
  answering raises one alert AT THE ROOT (central store); supporting
  consumes NO personal token and flips `support` to `withdraw_token`
  (symmetric withdrawal pinned); VALIDATING an answer closes the
  question (cross-object cascade `['validated', 'published']` /
  `['closed', 'published']`); `archive` REQUIRES an `explanation`
  (KeyError without), alerts, and collapses the gates (members: empty
  set; admin: the quintet with `delquestion` appearing). Full suite
  **87/87** green.

- **T4b: the person lifecycle is pinned** — the security core of
  `user_management` (885 behaviour statements, previously untested)
  reaches **50 %** through 9 behaviour-level tests (content/person.py
  47 %); full suite **96/96** green. Pinned contracts: a fresh member
  is `['active']` with `['Member', 'Owner']`; exact gates (the admin
  extras include `discuss` — one cannot discuss with oneself);
  `deactivate` collapses the gates to the quartet
  `{seehistory, activate, see, see_notations}` and `activate`
  restores; `assign_roles` REQUIRES `roles` and REPLACES the
  assignable set (Member disappears, the Owner relation is
  preserved); `Edit.start` requires the NESTED `change_password`
  mapping — no-change keeps the password yet bumps `modified_at`,
  change mode with the correct current password switches it;
  `get_api_token` requires the password and installs a 32-character
  token behind an HTTPFound; `quit` is a REQUEST, not the act (the
  state stays `['active']` until the mailed confirmation).

- **T4c: the invitation lifecycle is pinned** — the entry path
  (360 behaviour statements, previously untested) reaches **76 %**
  through 7 behaviour-level tests (content/invitation.py 80 %); full
  suite **103/103** green. Pinned contracts: `invite` takes
  `{'invitations': [{'_object_data': Invitation}]}` and stamps each
  one (state `['pending']`, manager = the inviter, a random-token
  `__name__`, default roles `['Member']`); the gates INVERT across the
  mail link (admin: `{edit, remind, remove, seeinvitation}`;
  anonymous: `{accept, refuse, seeinvitation}`); `accept` requires the
  password, creates the Person FROM the invitation's data (active,
  invitation roles plus Owner), REMOVES the invitation from the root
  and links back through `invitation.person`; `refuse` is the
  asymmetric twin — kept at the root, marked `['refused']`, anonymous
  actions collapsing to `seeinvitation`; the admin's `remove` deletes
  a pending invitation outright.

- **The Registration arc is pinned — and a MODERNISATION REGRESSION
  fixed**: substanced's password API drifted (`pwd_manager` →
  `hash_new_password` staticmethod), crashing the `Preregistration`
  constructor on 3.12; `person.py` now honours whichever is present,
  proven by `check_password` across the whole chain. 7 tests; full
  suite **110/110** green. Pinned: the anonymous `registration` on the
  root, closed by `only_invitation` (and the dace-level SiteAdmin
  override that shows every action pinned in passing); the constructor
  encodes the password immediately (bcrypt, never the clear text);
  stamping (state `['pending']`, token name, deadline = creation +
  4 days); the gates (anonymous holds `confirmregistration` ALONE;
  the admin the quintet with remind/remove); confirmation creating the
  Person (`name_chooser` key `'Bob-B'`, active, Member+Owner,
  auto-login redirect) and removing the preregistration; expiry
  closing every anonymous gate; the admin's outright `remove`.
  Harness idiom recorded: substanced's audit subscriber (LoggedIn)
  reads `request.context` — set it on the test request.

- **The report/moderation cycle is pinned** — the social-safety
  machinery of `reports_management` (207 behaviour statements) reaches
  **85 %** through 6 behaviour-level tests (content/report.py 80 %,
  the report adapters dragged to ~47 %); full suite **116/116** green.
  Pinned contracts: `report` is MEMBER-gated (no anonymous) and
  state-gated on `published` content; reporting appends `'reported'`,
  files the report (`['pending']`, reporter as author) and STARTS the
  `contentreportdecision` ballot (the moderator draw excludes the
  content author), reporting staying available while no finished valid
  ballot exists; `censor()` REPLACES the whole content state with
  `['censored']` (the `ISignalableObject` adapter) and processes the
  pending reports; `restor` is MODERATOR-gated from `censored` and
  restores the original publication states; `ignore()` removes
  `'reported'` and processes the reports; the reason referential is
  closed (unknown keys KeyError). Harness facts recorded: the content
  author must be a real Person (`user_locale`), and the behaviours
  module import needs the historical cycle primed
  (`import novaideo.views` first).

- **Documentation pause (post-campaign).** README carries the 116-test
  reality and the five pinned families; CHANGES consolidates the
  process-family batches; the modern-harness document gains the
  behaviour-level testing idioms settled by the campaign.

- **The `contentreportdecision` ballot is conducted to its verdict** —
  the deepening of the report cycle: 6 tests, full suite **122/122**
  green (now certified in two halves — historical trunk + first
  batches, then the six lifecycle suites — the single run has outgrown
  one invocation). Coverage of the ballot machinery: referendum
  behaviours **100 %**, content_ballot definition 99 %,
  ballot_processes 83 %, reports behaviours **85 % → 91 %**. Pinned:
  the elector draw excludes ONLY the content author (the reporter IS a
  juror), each elector granted `('LocalModerator', content)` with one
  Referendum ballot attached; the `referendumprocess.vote` action
  appears on the content for electors only, disappears once cast, and
  requires the `vote` key; majority AGAINST → censor (`['censored']`,
  reports processed), majority FOR → ignore (publication untouched);
  either verdict revokes the LocalModerator grants and a finished
  valid ballot BLOCKS re-reporting — the second half of the
  anti-re-report contract. Architecture fact recorded honestly: the
  decision node completes at the BALLOT DEADLINE in production (the
  vote sub-process is timer-closed by the custom `SubProcess.stop`);
  the tests invoke the node's `after_execution` after the last vote —
  the very code path the deadline runs.

- **The `moderate_registration` variant is pinned — and latent bug #4
  joins the register**: the no-electors fallback has NEVER been able
  to complete — it forces `['accepted']` and sends the mail, then
  dies on the shared `alert_user(...)` line whose `alert_data` only
  the ballot branch binds (`UnboundLocalError`, present in the
  imported historical source; the TORN WRITE is pinned too — the
  state is `['accepted']` after the crash). Moderated sites therefore
  require an available member pool. 6 tests; full suite **128/128**
  (two halves: 78 + 50); user_management behaviours **50 % → 61 %**.
  Pinned contracts: under moderation the candidacy stays `['pending']`
  with a `registrationmoderation` ballot attached (random draw among
  ALL members), electors granted `('LocalModerator', preregistration)`
  and voting ON the preregistration, the anonymous
  `confirmregistration` gate CLOSED while pending; acceptance replaces
  the state with `['accepted']`, opens the gate, and the entry path
  completes through moderation (the Person is created); refusal
  REMOVES the candidacy outright; and SILENT electors refuse —
  `ballot_result(self)` defaults to False here, the asymmetry of
  mercy with the report decision whose silence defaults to ignore.

- **Latent bug #4 is repaired, its test flipped in conscience.** The
  under-review notification (ballot-bound `alert_data`) moved into the
  ballot branch: the no-electors fallback of `moderate_registration`
  now accepts outright and the entry path completes to the Person
  (`test_no_electors_fallback_accepts_at_once` guards it). Full suite
  **128/128** (two halves: 78 + 50).

- **Rename window.** The `pseudo_react` callers move to daceui's
  `action_informations`; `${nember}` becomes `${number}` in
  `see_notations` and across the catalogues (pot, fr, de — the
  compiled fr `.mo` patched in place with a same-length replacement,
  the new msgid verified resolving to its translation);
  `get_random_users(nember)` becomes `number`. Full suite 128/128
  (two halves: 78 + 50).

- **Documentation update (post-deepening).** README carries the final
  campaign state (128 tests, both ballots conducted, four latent bugs
  and one regression — all fixed and guarded); CHANGES consolidates
  the deepening; modern-harness gains the ballot-conduct idiom and
  the two-halves suite doctrine.

- **Nova-Ideo 2.0: the parent adopts the modernised trunk.** README
  re-branded (Nova-Ideo identity, Lineage section naming the KuneAgi
  reference trunk and the Logikascium stewardship); CHANGES carries
  the adoption entry. Applied on the nova-ideo repository AFTER the
  adoption merge (`-s ours` with the 2020 tip as parent) — never on
  the KuneAgi repository.
