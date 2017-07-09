# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connections
from utils.config_info import get_config
from utils.sql_helper import get_sql_from_file


db_user = get_config('client', 'user')
if db_user == None:
    db_user = connections['default'].settings_dict['USER']

scoreboard_store_procedure_install_sql = get_sql_from_file(
    'get_scoreboard_penalty.sql',
    formatting_tuple=(db_user),
)
scoreboard_store_procedure_uninstall_sql = get_sql_from_file(
    'drop_get_scoreboard_penalty.sql')

def install_scoreboard_store_procedure(apps, schema_editor):
    schema_editor.execute(scoreboard_store_procedure_install_sql)

def uninstall_scoreboard_store_procedure(apps, schema_editor):
    schema_editor.execute(scoreboard_store_procedure_uninstall_sql)


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(
            install_scoreboard_store_procedure,
            uninstall_scoreboard_store_procedure
        ),
    ]
