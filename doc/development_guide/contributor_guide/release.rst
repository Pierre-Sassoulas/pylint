Releasing a pylint version
==========================

So, you want to release the ``X.Y.Z`` version of pylint ?

The release is largely automated. Three GitHub Actions workflows do the work:

- ``release-prepare`` (``.github/workflows/release-prepare.yml``) — manually
  triggered. Bumps the version with ``tbump``, builds the changelog and opens
  the release pull request.
- ``release-publish`` (``.github/workflows/release-publish.yml``) — triggered
  when a ``vX.Y.Z`` tag is pushed. Builds the release notes from the
  ``What's New`` documents and creates the GitHub release.
- ``release`` (``.github/workflows/release.yml``) — triggered when the GitHub
  release is published. Builds, signs and uploads the distributions to PyPI.
- ``release-finalize`` (``.github/workflows/release-finalize.yml``) — also
  triggered when the release is published. Creates the maintenance branch,
  rotates the backport label and milestones.

The only manual steps left are: triggering ``release-prepare``, reviewing and
merging the release pull request, pushing the tag, and a couple of admin tasks
that need credentials the automation does not have (see below).

Releasing a major or minor version
-----------------------------------

**Before releasing a major or minor version check if there are any
unreleased commits on the maintenance branch. If so, release a last
patch release first. See ``Releasing a patch version``.**

-  Write the ``Summary -- Release highlights`` in the relevant
   ``doc/whatsnew/X/X.Y/index.rst`` and upgrade the release date.
-  Trigger the ``release-prepare`` workflow from the ``main`` branch
   (``Actions`` ▸ ``Prepare a release`` ▸ ``Run workflow``) with:

   -  ``version``: the version to release (for example ``2.5.0``).
   -  ``next_dev_version``: the dev version ``main`` should move to afterwards
      (for example ``2.6.0-dev0``).

   The workflow runs ``tbump`` to bump the version and build the changelog,
   bumps ``main`` to the dev version (which also creates the next
   ``What's New in Pylint X.Y+1`` document and wires it into the toctrees),
   pushes the ``release-X.Y.0`` branch and opens the release pull request.
-  Review the pull request (version bump, changelog, contributors list) and
   merge it. No one can push directly on ``main``.
-  Recover the merged commit on ``main`` and tag the release commit (the one
   whose version is ``X.Y.0``) as ``vX.Y.Z`` (for example ``v2.5.0``).
-  Push the tag. This triggers ``release-publish`` (which creates the GitHub
   release), then ``release`` (PyPI upload) and ``release-finalize``.
-  ``release-finalize`` automatically creates the ``maintenance/X.Y.x`` branch,
   marks the closed ``backport maintenance/X.Y-1.x`` issues as ``backported``,
   renames that label to ``backport maintenance/X.Y.x``, closes the ``X.Y.0``
   milestone and creates the ``X.Y.1`` and ``X.Y+1.0`` milestones.
-  Manually finish the admin tasks the automation cannot do:

   -  Upgrade the pattern for the protected branches in the settings under
      ``Branches`` / ``Branch protection rules`` (for example
      ``maintenance/2.5*`` instead of ``maintenance/2.4*``). There's a lot of
      configuration done in these settings, do NOT recreate it from scratch.
   -  Delete the ``maintenance/X.Y-1.x`` branch (for example
      ``maintenance/2.4.x``).
   -  Hide and deactivate all the patch releases for the previous minor release
      on `readthedocs <https://readthedocs.org/projects/pylint/versions/>`__,
      except the last one. (For example: hide ``v2.4.0``, ``v2.4.1``,
      ``v2.4.2`` and keep only ``v2.4.3``.)

Back-porting a fix from ``main`` to the maintenance branch
----------------------------------------------------------

Whenever a PR on ``main`` should be released in a patch release on the
current maintenance branch:

-  Label the PR with ``backport maintenance/X.Y.x``. (For example
   ``backport maintenance/2.4.x``)
-  Squash the PR before merging (alternatively rebase if there's a
   single commit). The ``backport`` GitHub App
   (``.github/workflows/backport.yml``) opens the cherry-pick pull request
   automatically.
-  (If the automated cherry-pick has conflicts)

   -  Add a ``Needs backport`` label and do it manually.
   -  You might alternatively also:

      -  Cherry-pick the changes that create the conflict if it's not a
         new feature before doing the original PR cherry-pick manually.
      -  Decide to wait for the next minor to release the PR
      -  In any case upgrade the milestones in the original PR and newly
         cherry-picked PR to match reality.

-  Release a patch version

Releasing a patch version
-------------------------

We release patch versions when a crash or a bug is fixed on the main
branch and has been cherry-picked on the maintenance branch.

-  Trigger the ``release-prepare`` workflow from the
   ``maintenance/X.Y.x`` branch with ``version`` set to the patch version
   (for example ``2.4.1``) and ``next_dev_version`` left empty. It bumps the
   version, builds the changelog and opens the release pull request against
   the maintenance branch.
-  Review and merge the release pull request to run the CI tests for this
   branch.
-  Tag the release commit as ``vX.Y.Z`` and push the tag. This triggers
   ``release-publish`` (GitHub release), ``release`` (PyPI upload) and
   ``release-finalize`` (which closes the ``X.Y.Z`` milestone and creates the
   ``X.Y.Z+1`` one).
-  Merge the ``maintenance/X.Y.x`` branch back into ``main``. The main branch
   should have the changelog for ``X.Y.Z+1`` (for example ``v2.4.2``). This
   merge is required so ``pre-commit autoupdate`` works for pylint.
-  Fix version conflicts properly, or bump the version to ``X.Y+1.0-devZ``
   (for example ``2.5.0-dev6``) before pushing on the main branch.

Manual fallback
---------------

If you need to run the release locally instead of through the workflows
(for example to debug a problem):

-  Install the release dependencies:
   ``pip3 install -r requirements_test.txt``
-  Bump the version and build the changelog with
   ``tbump X.Y.Z --no-push --no-tag`` (drop ``--no-tag`` for a patch release if
   you want ``tbump`` to create the tag). Check the result with ``git show``.
-  ``script/release_changelog.py X.Y.Z`` prints the markdown release notes used
   for the GitHub release body.
-  ``script/release_finalize.py X.Y.Z`` prints the post-release house-keeping;
   add ``--apply`` to perform it (requires an authenticated ``gh`` CLI).

Milestone handling
-------------------

We move issues that were not done to the next milestone and block
releases only if there are any open issues labelled as ``blocker``.
