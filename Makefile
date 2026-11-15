# make check  — validate every skill before upload
# make zips   — build one uploadable zip per skill into dist/
# make clean  — remove dist/

SKILLS := $(notdir $(wildcard skills/*))

.PHONY: check zips clean help

help:
	@echo "make check  validate frontmatter, name match, description limits, privacy lint"
	@echo "make zips   build dist/<skill>.zip, one per skill, ready to upload"
	@echo "make clean  remove dist/"

check:
	@python3 scripts/check_skills.py

zips: check
	@mkdir -p dist
	@rm -f dist/*.zip
	@cd skills && for s in $(SKILLS); do \
		zip -qr "../dist/$$s.zip" "$$s" && echo "dist/$$s.zip"; \
	done
	@echo "Upload each at Customize -> Skills -> + -> Create skill -> Upload a skill."

clean:
	@rm -rf dist
