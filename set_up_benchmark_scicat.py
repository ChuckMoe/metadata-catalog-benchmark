# coding: utf-8
"""
Script for setting up demo data in a previously unused SampleDB installation.
Usage: python -m sampledb set_up_demo
"""
import json
import os
import sys
import time

sys.path.append("/home/sampledb")

import sampledb
from sampledb import create_app
from sampledb.models import UserType, ActionType, Language
from sampledb.logic.instruments import create_instrument, add_instrument_responsible_user
from sampledb.logic.instrument_translations import set_instrument_translation
from sampledb.logic.action_translations import set_action_translation
from sampledb.logic.action_type_translations import set_action_type_translation
from sampledb.logic.actions import create_action, create_action_type
from sampledb.logic import groups, object_permissions, projects, comments, files


def main(arguments):
    print('test')
    if len(arguments) != 0:
        print(__doc__)
        exit(1)
    app = create_app()
    if not app.config.get("SERVER_NAME"):
        app.config["SERVER_NAME"] = "localhost:8000"
    with app.app_context():
        if sampledb.logic.actions.get_actions() or sampledb.logic.instruments.get_instruments() or len(
                sampledb.logic.users.get_users()) > 1:
            print("Error: database must be empty for demo", file=sys.stderr)
            exit(1)

        data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'benchmark_data'))
        schema_directory = os.path.join(data_directory, 'schemas')

        if sampledb.logic.users.get_users():
            # admin might have been created from environment variables
            admin = sampledb.logic.users.get_users()[0]
        else:
            admin = sampledb.logic.users.create_user(
                name="Administrator",
                email="admin@example.com",
                type=UserType.PERSON)
            sampledb.logic.users.set_user_administrator(admin.id, True)

        api_user = sampledb.logic.users.create_user(name="API User", email="api@example.com", type=UserType.OTHER)
        sampledb.logic.authentication.add_other_authentication(api_user.id, 'api', 'password')
        sampledb.logic.authentication.add_api_token(
            api_user.id,
            api_token='abcd' * 16,
            description="API user API-Token")

        # enable german for input
        german = sampledb.logic.languages.get_language(sampledb.models.Language.GERMAN)
        sampledb.logic.languages.update_language(
            language_id=german.id,
            names=german.names,
            lang_code=german.lang_code,
            datetime_format_datetime=german.datetime_format_datetime,
            datetime_format_moment=german.datetime_format_moment,
            enabled_for_input=True,
            enabled_for_user_interface=True
        )

        ### Create Action Types
        new_action_types = {
            'Proposal': -1,
            'Datablock': -1
        }
        for new_action_type in new_action_types.keys():
            new_action_types[new_action_type] = create_action_type(
                admin_only=False,
                show_on_frontpage=True,
                show_in_navbar=True,
                enable_labels=True,
                enable_files=True,
                enable_locations=True,
                enable_publications=True,
                enable_comments=True,
                enable_activity_log=True,
                enable_related_objects=True,
                enable_project_link=True,
                disable_create_objects=False,
                is_template=False
            )
            set_action_type_translation(
                action_type_id=new_action_types[new_action_type].id,
                language_id=Language.ENGLISH,
                name=new_action_type,
                description=new_action_type,
                object_name=new_action_type,
                object_name_plural=new_action_type,
                view_text=new_action_type,
                perform_text='Create {}'.format(new_action_type)
            )
            sampledb.db.session.commit()

        ### Create Actions
        schema_files = [
            ['proposal.action.json', new_action_types['Proposal'].id, 'Proposal Creation', 'Create a new Proposal'],
            ['sample.action.json', ActionType.SAMPLE_CREATION, 'SciCat Sample Creation', 'Create new SciCat Sample'],
            ['measurement.action.json', ActionType.MEASUREMENT, 'SciCat Dataset Creation', 'Create new SciCat Dataset'],
            ['measurement.action.json', new_action_types['Datablock'].id, 'SciCat DataBlock Creation', 'Create new SciCat Datablock']
        ]
        for schema_information in schema_files:
            with open(os.path.join(schema_directory, schema_information[0]), 'r', encoding='utf-8') as handler:
                schema = json.load(handler)
                action = create_action(action_type_id=schema_information[1], schema=schema)
                set_action_translation(
                    Language.ENGLISH,
                    action.id,
                    name=schema_information[2],
                    description=schema_information[3])
                sampledb.logic.action_permissions.set_action_public(action.id)
        sampledb.db.session.commit()

    print("Success: set up demo data", flush=True)


if __name__ == '__main__':
    time.sleep(10)
    main([])
    sys.exit(0)
