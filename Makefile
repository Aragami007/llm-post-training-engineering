.PHONY: validate test issues-plan progress
validate:
	python3 scripts/validate_course.py
	python3 -m unittest discover -s tests -v
issues-plan:
	python3 scripts/publish_issues.py --repo $${REPO:?set REPO=owner/name} --dry-run
progress:
	python3 scripts/progress.py --repo $${REPO:?set REPO=owner/name}
