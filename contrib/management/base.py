import os
import sys
from abc import ABC

import celery
from kombu.utils.encoding import str_to_bytes

try:
    import django_celery_beat
except ImportError:
    import djcelery

from django.core.management import BaseCommand


def setenv(k, v):  # noqa
    os.environ[str_to_bytes(k)] = str_to_bytes(v)


class CeleryCommand(BaseCommand, ABC):
    options = ()
    if hasattr(BaseCommand, "option_list"):
        options = BaseCommand.option_list
    else:

        def add_arguments(self, parser):
            option_typemap = {"string": str, "int": int, "float": float}
            for opt in self.option_list:
                option = {k: v for k, v in opt.__dict__.items() if v is not None}
                flags = option.get("_long_opts", []) + option.get("_short_opts", [])
                if option.get("default") == ("NO", "DEFAULT"):
                    option["default"] = None
                if option.get("nargs") == 1:
                    del option["nargs"]
                del option["_long_opts"]
                del option["_short_opts"]
                if "type" in option:
                    opttype = option["type"]
                    option["type"] = option_typemap.get(opttype, opttype)
                parser.add_argument(*flags, **option)

    skip_opts = ["--app", "--loader", "--config", "--no-color"]
    requires_system_checks = False
    keep_base_opts = False
    stdout, stderr = sys.stdout, sys.stderr

    def get_version(self):
        def get_version(self):
            try:
                version = "celery {c.__version__}\ndjango-celery-beat {d.__version__}".format(
                    c=celery,
                    d=django_celery_beat,
                )
            except ImportError:
                version = "celery {c.__version__}\ndjango-celery {d.__version__}".format(
                    c=celery,
                    d=djcelery,
                )
            return version

    def execute(self, *args, **options):
        broker = options.get("broker")
        if broker:
            self.set_broker(broker)
        super(CeleryCommand, self).execute(*args, **options)

    def set_broker(self, broker):
        setenv("CELERY_BROKER_URL", broker)

    def run_from_argv(self, argv):
        self.handle_default_options(argv[2:])
        return super(CeleryCommand, self).run_from_argv(argv)

    def handle_default_options(self, argv):
        acc = []
        broker = None
        for i, arg in enumerate(argv):
            # --settings and --pythonpath are also handled
            # by BaseCommand.handle_default_options, but that is
            # called with the resulting options parsed by optparse.
            if "--settings=" in arg:
                _, settings_module = arg.split("=")
                setenv("DJANGO_SETTINGS_MODULE", settings_module)
            elif "--pythonpath=" in arg:
                _, pythonpath = arg.split("=")
                sys.path.insert(0, pythonpath)
            elif "--broker=" in arg:
                _, broker = arg.split("=")
            elif arg == "-b":
                broker = argv[i + 1]
            else:
                acc.append(arg)
        if broker:
            self.set_broker(broker)
        return argv if self.keep_base_opts else acc

    def die(self, msg):
        sys.stderr.write(msg)
        sys.stderr.write("\n")
        sys.exit()

    def _is_unwanted_option(self, option):
        return option._long_opts and option._long_opts[0] in self.skip_opts

    @property
    def option_list(self):
        return [x for x in self.options if not self._is_unwanted_option(x)]
