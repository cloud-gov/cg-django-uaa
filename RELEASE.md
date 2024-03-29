# Releasing

Here's how to issue a new release:

1. Bump the version number in `uaa_client/__init__.py`.

1. Move the "unreleased" section to a new version entry in
   `CHANGELOG.md`.

1. From the project root, install dependencies and run automated tests:

   ```shell
   tox
   ```

1. Run the following to ensure that everything builds and
   installs OK in an isolated environment:

   ```shell
   # remove existing builds
   rm -rf dist build

   # build source distribution
   python -m build --sdist

   # install dependencies
   python -m venv venv
   source venv/bin/activate
   python -m pip install .

   # start up docker environment for manual tests
   python test.py manualtest
   ```

   You should be able to visit <http://localhost:8000> and log in
   as `foo@example.org` without any problems.

1. Commit and push your changes with a commit message like
   "Bump version to v1.0.4."

1. Tag your version and push it to GitHub. For instance, if you're
   releasing v1.0.4, do:

   ```shell
   git tag -a v1.0.4
   git push origin v1.0.4
   ```

   When running `git tag`, you'll be prompted for a tag
   message. Consider copy-pasting the version notes from
   `CHANGELOG.md` for this, as whatever you enter will
   show up on the [GitHub releases page][].

1. After you push, the [CI pipeline](./ci/pipeline.yml) will automatically
   create a [GitHub release][GitHub releases page] for the tag.

1. If you haven't already done so, create a `~/.pypirc` file
   with the following content:

   ```conf
   [distutils]
   index-servers =
      pypi
      cg-django-uaa

   [pypi]
   username = __token__
   password = <your API token>
   ```

1. Run `python -m twine upload dist/*`.  The new release should now
   be visible on [PyPI][].

[GitHub releases page]: https://github.com/cloud-gov/cg-django-uaa/releases
[PyPI]: https://pypi.python.org/pypi/cg-django-uaa
