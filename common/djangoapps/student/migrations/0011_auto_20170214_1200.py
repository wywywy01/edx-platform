# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_email_uniqueness_constraint(apps, schema_editor):
    # Do we already have an email uniqueness constraint?
    cursor = schema_editor.connection.cursor()
    constraints = schema_editor.connection.introspection.get_constraints(cursor, "auth_user")
    email_constraint = constraints.get("email", {})
    if email_constraint.get("columns") == ["email"] and email_constraint.get("unique") == True:
        # We already have the constraint, we're done.
        return

    # We don't have the constraint, make it.
    schema_editor.execute("create unique index email on auth_user (email)")


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_auto_20170207_0458'),
    ]

    operations = [
        migrations.RunPython(add_email_uniqueness_constraint)
    ]
