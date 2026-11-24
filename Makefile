venv:
	@[ -x .venv/bin/python3 ] || { python3 -m venv .venv && .venv/bin/python3 -m pip install -q -r requirements.txt; }

validate: venv
	@.venv/bin/python3 -m py_compile dropzettel.py scripts/setup_wizard.py shortcut/build_shortcut.py tests/selftest.py
	@bash -n run.sh setup.sh
	@plutil -lint launchd/*.template >/dev/null
	@.venv/bin/python3 -B tests/selftest.py
	@! grep -rIl --exclude-dir=.venv --exclude-dir=.git --exclude=Makefile -e "/Users/" . || { echo "absolute home paths found in the files above"; exit 1; }
	@echo "validate: OK"

.PHONY: venv validate
