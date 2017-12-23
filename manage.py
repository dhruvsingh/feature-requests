#!/usr/bin/env python
from fr_app import app


@app.cli.command()
def createdb():
    """Create database while setting up initially."""
    from fr_app.models import db
    db.create_all()


@app.cli.command()
def runserver():
    """Run flask local dev server."""
    app.run()
