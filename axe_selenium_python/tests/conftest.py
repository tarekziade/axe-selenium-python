# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from datetime import datetime
from py.xml import html
from axe_selenium_python import Axe
import pytest


HERE = os.path.dirname(__file__)


@pytest.fixture
def script_url():
    """Return a script URL"""
    return os.path.join(HERE, 'src', 'axe.min.js')


@pytest.fixture(scope='function')
def axe(selenium, base_url, script_url):
    """Return an Axe instance based on context and options."""
    selenium.get(base_url)
    yield Axe(selenium, script_url)


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(0, html.th('Time', class_='sortable time', col='time'))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # add docstring to 'description' column
    report.description = str(item.function.__doc__)
