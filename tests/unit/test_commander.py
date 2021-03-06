from unittest.mock import MagicMock

import pytest

from pyrandall.commander import Commander, Flags
from pyrandall.reporter import Reporter, ResultSet
from pyrandall.spec import SpecBuilder
from tests.conftest import vcr


@pytest.fixture
def spec():
    builder = SpecBuilder(
        specfile="one_event.yaml",
        dataflow_path="examples/",
        default_request_url="http://localhost:5000",
        schemas_url="http://localhost:8899/schemas/",
    )
    return builder.feature()


@vcr.use_cassette("test_commander_run_one_for_one")
def test_commander_run_one_for_one(spec):
    reporter = MagicMock(Reporter(), unsafe=True)
    reporter.scenario.return_value = MagicMock(ResultSet, unsafe=True)

    c = Commander(spec, Flags.BLOCKING_E2E)
    c.run(reporter)

    reporter.feature.assert_called_once_with("One event"),
    reporter.scenario.assert_any_call("Send words1 event")
    # at least once called
    reporter.simulate.assert_called()
    reporter.validate.assert_called()
    reporter.run_task.assert_called()
    reporter.print_failures.assert_called_once_with()
    reporter.passed.assert_called_once()
