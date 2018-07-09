#!/usr/bin/env bash

PACKAGE_NAME=nodegraph
PACKAGE_BUILD_DIR=./build
DOCS_ROOT=./docs
DOCS_BUILD_DIR=${DOCS_ROOT}/build

.PHONY: clean

clean:
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .tox
	rm -rf dist
	rm -rf ${DOCS_BUILD_DIR}
	rm -rf ${PACKAGE_BUILD_DIR}
	rm -rf ${PACKAGE_NAME}.egg-info
	rm -f .coverage
	rm -f coverage.xml
	rm -f junit-*.xml
