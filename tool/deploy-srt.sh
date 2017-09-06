#!/bin/sh

set -e

cd "${TRAVIS_BUILD_DIR}"

git config --global push.default simple
git config user.name "Travis CI"
git config user.email "travis@travis-ci.org"

git checkout "${TRAVIS_BRANCH}"
git add --all
git commit -m "Extract srt files for commit: ${TRAVIS_COMMIT}" -m "Travis build: ${TRAVIS_BUILD_NUMBER} [ci skip]"
git push "https://${GH_REPO_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git" "${TRAVIS_BRANCH}"
