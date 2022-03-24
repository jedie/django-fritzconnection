import os
from pathlib import Path

import cmd2
from dev_shell.base_cmd2_app import DevShellBaseApp, run_cmd2_app
from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.command_sets.dev_shell_commands import DevShellCommandSet as OriginDevShellCommandSet
from dev_shell.config import DevShellConfig
from dev_shell.utils.assertion import assert_is_dir
from dev_shell.utils.colorful import blue, bright_yellow, print_error
from dev_shell.utils.subprocess_utils import argv2str, make_relative_path, verbose_check_call

import djfritz
from djfritz_project.manage import main


PACKAGE_ROOT = Path(djfritz.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT / 'djfritz')


class TempCwd:
    def __init__(self, cwd: Path):
        assert_is_dir(cwd)
        self.cwd = cwd

    def __enter__(self):
        self.old_cwd = Path().cwd()
        os.chdir(self.cwd)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.old_cwd)


def call_manage_py(*args, cwd):
    print()
    print('_' * 100)
    cwd_rel = make_relative_path(cwd, relative_to=Path.cwd())
    print(f'+ {cwd_rel}$ {bright_yellow("manage.py")} {blue(argv2str(args))}\n')
    args = list(args)
    args.insert(0, 'manage.py')  # Needed for argparse!
    with TempCwd(cwd):
        try:
            main(argv=args)
        except SystemExit as err:
            print_error(f'finished with exit code {err}')
        except BaseException as err:
            print_error(err)


@cmd2.with_default_category('django-fritzconnection commands')
class DjFritzCommandSet(DevShellBaseCommandSet):
    def do_manage(self, statement: cmd2.Statement):
        """
        Call django-fritzconnection test "manage.py"
        """
        call_manage_py(*statement.arg_list, cwd=PACKAGE_ROOT / 'djfritz')

    def do_run_testserver(self, statement: cmd2.Statement):
        """
        Start Django dev server with the test project
        """
        # Start the "[tool.poetry.scripts]" script via subprocess
        # This works good with django dev server reloads
        verbose_check_call('run_testserver', *statement.arg_list, cwd=PACKAGE_ROOT)

    def do_makemessages(self, statement: cmd2.Statement):
        """
        Make and compile locales message files
        """
        call_manage_py(
            'makemessages',
            '--all',
            '--no-location',
            '--no-obsolete',
            '--ignore=.*',
            '--ignore=htmlcov',
            '--ignore=volumes',
            cwd=PACKAGE_ROOT / 'djfritz',
        )

    def do_fill_verbose_name_translations(self, statement: cmd2.Statement):
        """
        Auto fill "verbose_name" translations:
        Just copy the model field name as translation.
        """
        MESSAGE_MAP = {'id': 'ID'}

        for lang_code in ('de', 'en'):
            print('_' * 100)
            print(lang_code)
            po_file_path = PACKAGE_ROOT / f'djfritz/locale/{lang_code}/LC_MESSAGES/django.po'
            old_content = []
            new_content = []
            with po_file_path.open('r') as f:
                for line in f:
                    old_content.append(line)

                    if line.startswith('msgid "'):
                        msgstr = ''
                        msgid = line[7:-2]
                        try:
                            model, attribute, kind = msgid.strip().split('.')
                        except ValueError:
                            pass
                        else:
                            if kind == 'verbose_name':
                                if attribute in MESSAGE_MAP:
                                    msgstr = MESSAGE_MAP[attribute]
                                else:
                                    words = attribute.replace('_', ' ').split(' ')
                                    msgstr = ' '.join(i.capitalize() for i in words)
                            elif kind == 'help_text':
                                msgstr = ' '  # "hide" empty "help_text"

                    elif (line == 'msgstr ""\n' or line == 'msgstr "&nbsp;"\n') and msgstr:
                        line = f'msgstr "{msgstr}"\n'

                    line = line.replace('Content Tonie', 'Content-Tonie')
                    new_content.append(line)

            if new_content == old_content:
                print('Nothing to do, ok.')
                return

            with po_file_path.open('w') as f:
                f.write(''.join(new_content))

            print(f'updated: {po_file_path}')

    def do_update_test_snapshots(self, statement: cmd2.Statement):
        """
        Update all test snapshot files by run tests with RAISE_SNAPSHOT_ERRORS=0
        """
        verbose_check_call(
            'pytest',
            *statement.arg_list,
            cwd=self.config.base_path,
            exit_on_error=True,
            extra_env={
                # https://github.com/boxine/bx_py_utils#notes-about-snapshot
                'RAISE_SNAPSHOT_ERRORS': '0'
            },
        )


class DevShellCommandSet(OriginDevShellCommandSet):
    pass


class DevShellApp(DevShellBaseApp):
    pass


def get_devshell_app_kwargs():
    """
    Generate the kwargs for the cmd2 App.
    (Separated because we needs the same kwargs in tests)
    """
    config = DevShellConfig(package_module=djfritz)

    # initialize all CommandSet() with context:
    kwargs = dict(config=config)

    app_kwargs = dict(
        config=config,
        command_sets=[
            DjFritzCommandSet(**kwargs),
            DevShellCommandSet(**kwargs),
        ],
    )
    return app_kwargs


def devshell_cmdloop():
    """
    Entry point to start the "dev-shell" cmd2 app.
    Used in: [tool.poetry.scripts]
    """
    app = DevShellApp(**get_devshell_app_kwargs())
    run_cmd2_app(app)  # Run a cmd2 App as CLI or shell
