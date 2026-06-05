# Changelog

## [0.7.2](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.7.1...otdf-python-v0.7.2) (2026-06-05)


### Bug Fixes

* fix D205 docstring formatting across otdf-python source files ([#149](https://github.com/b-long/opentdf-python-sdk/issues/149)) ([951fa33](https://github.com/b-long/opentdf-python-sdk/commit/951fa33d541f4662c1b6ec8d5cccd08ab8e03b50))
* fix/increase testing, fix misconfiguration ([#148](https://github.com/b-long/opentdf-python-sdk/issues/148)) ([1dc8c45](https://github.com/b-long/opentdf-python-sdk/commit/1dc8c4557bdcbcbf74b2f663c4e190664047cb7f))
* **main:** fix release issue, required arguments from workspace root ([#147](https://github.com/b-long/opentdf-python-sdk/issues/147)) ([668f00a](https://github.com/b-long/opentdf-python-sdk/commit/668f00a083990b5cea686e5885216e0359ceaf55))
* use --package flag with uv version for workspace layout ([#144](https://github.com/b-long/opentdf-python-sdk/issues/144)) ([12acfbb](https://github.com/b-long/opentdf-python-sdk/commit/12acfbb4f8d99c8c745f35cbd7bddfc41e63b8b4))

## [0.7.1](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.7.0...otdf-python-v0.7.1) (2026-06-04)


### Documentation

* fix project structure path in README ([#145](https://github.com/b-long/opentdf-python-sdk/issues/145)) ([c10f98b](https://github.com/b-long/opentdf-python-sdk/commit/c10f98bb67e823a8bd061c8100d8493d2083699f))

## [0.7.0](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.6.0...otdf-python-v0.7.0) (2026-06-04)


### Features

* **main:** upgrade from `httpx` to `httpx2`, update other dependencies & switch to uv workspace layout ([#142](https://github.com/b-long/opentdf-python-sdk/issues/142)) ([649f63c](https://github.com/b-long/opentdf-python-sdk/commit/649f63ce4eee4b564b92afd3dbda2b3e3d55803e))

## [0.6.0](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.5.0...otdf-python-v0.6.0) (2026-05-21)


### Features

* **main:** update to service v 0.12.0 ([#139](https://github.com/b-long/opentdf-python-sdk/issues/139)) ([125b12b](https://github.com/b-long/opentdf-python-sdk/commit/125b12b24aa89fceeca56e5878728ac329dd8659))

## [0.5.0](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.4.4...otdf-python-v0.5.0) (2026-05-08)


### Features

* **main:** update proto GIT_TAG to service/v0.8.0 ([#137](https://github.com/b-long/opentdf-python-sdk/issues/137)) ([05ea9a4](https://github.com/b-long/opentdf-python-sdk/commit/05ea9a4c2dcf23d2a709e421802f45ddb89d2ace))

## [0.4.4](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.4.3...otdf-python-v0.4.4) (2026-04-30)


### Bug Fixes

* **proto-gen:** fix buf plugin path replacement, GIT_TAG, and generated_dir ([#135](https://github.com/b-long/opentdf-python-sdk/issues/135)) ([88d227d](https://github.com/b-long/opentdf-python-sdk/commit/88d227d83eb5e1903e5a2ef86dc38ea016885f60))

## [0.4.3](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.4.2...otdf-python-v0.4.3) (2026-02-05)


### Bug Fixes

* implement KAS allowlist functionality ([#129](https://github.com/b-long/opentdf-python-sdk/issues/129)) ([c1306da](https://github.com/b-long/opentdf-python-sdk/commit/c1306da24eb27f80bb3f1c11cea0f24175b5fd23))

## [0.4.2](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.4.1...otdf-python-v0.4.2) (2026-01-07)


### ⚠ BREAKING CHANGES

* **main:** Upgrade from connect-python 0.4.2 to 0.6.0

### Bug Fixes

* **main:** ensure compatibility with the latest `connect-python` ([#123](https://github.com/b-long/opentdf-python-sdk/issues/123)) ([4d160db](https://github.com/b-long/opentdf-python-sdk/commit/4d160dbed2bdedc4baaa807f97903aad710de943))


### Miscellaneous Chores

* release 0.4.2 ([a840f28](https://github.com/b-long/opentdf-python-sdk/commit/a840f284bed82a4b7de170ca1224bd232108047b))

## [0.4.1](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.4.0...otdf-python-v0.4.1) (2025-12-09)


### Bug Fixes

* preserve exception chain ([#119](https://github.com/b-long/opentdf-python-sdk/issues/119)) ([09984b8](https://github.com/b-long/opentdf-python-sdk/commit/09984b843b369a6d2c76dc8a81d6315f195ea773))

## [0.4.0](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.3.5...otdf-python-v0.4.0) (2025-11-20)


### Features

* add Python 3.14 support & fix pre-commit ([#117](https://github.com/b-long/opentdf-python-sdk/issues/117)) ([b89edfc](https://github.com/b-long/opentdf-python-sdk/commit/b89edfc70b13139691b7d2a11b256f59b457176d))

## [0.3.5](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.3.4...otdf-python-v0.3.5) (2025-11-10)


### Bug Fixes

* NanoTDF support ([#114](https://github.com/b-long/opentdf-python-sdk/issues/114)) ([8f09297](https://github.com/b-long/opentdf-python-sdk/commit/8f092976f6473db7738a86d7ec30dc9ebbcb6a3a))

## [0.3.4](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.3.3...otdf-python-v0.3.4) (2025-10-04)

### Chores

* chore: remove placeholders  ([#110](https://github.com/b-long/opentdf-python-sdk/issues/110))


### Bug Fixes

* update ruff ([#108](https://github.com/b-long/opentdf-python-sdk/issues/108)) ([5e4c796](https://github.com/b-long/opentdf-python-sdk/commit/5e4c796a8c1fc10b206cd2769f7c8548903ad3c1))

## [0.3.3](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.3.2...otdf-python-v0.3.3) (2025-09-17)


### Bug Fixes

* improve docs ([#106](https://github.com/b-long/opentdf-python-sdk/issues/106)) ([49aa4ae](https://github.com/b-long/opentdf-python-sdk/commit/49aa4aea5e576c20b3e26c852331de8b0469742f))

## [0.3.2](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.3.1...otdf-python-v0.3.2) (2025-09-12)


### Bug Fixes

* fix release-please configuration ([#104](https://github.com/b-long/opentdf-python-sdk/issues/104)) ([3b1c949](https://github.com/b-long/opentdf-python-sdk/commit/3b1c949680b1c4e8ec5bae5d2dbb2f18dc53b559))

## [0.3.1](https://github.com/b-long/opentdf-python-sdk/compare/otdf-python-v0.3.0...otdf-python-v0.3.1) (2025-09-12)


### Bug Fixes

* testing improvements ([#102](https://github.com/b-long/opentdf-python-sdk/issues/102)) ([8e82361](https://github.com/b-long/opentdf-python-sdk/commit/8e8236190df157da8ab7fda0b6dfb9cd78bae3bf))

## [0.3.0](https://github.com/b-long/opentdf-python-sdk/compare/v0.2.20...otdf-python-v0.3.0) (2025-09-11)


### ⚠ BREAKING CHANGES

* rewrite in pure Python ([#62](https://github.com/b-long/opentdf-python-sdk/issues/62))

### Features

* configure release-please ([#74](https://github.com/b-long/opentdf-python-sdk/issues/74)) ([439becd](https://github.com/b-long/opentdf-python-sdk/commit/439becd82a5faf834a190516b64e21aa331c0176))
