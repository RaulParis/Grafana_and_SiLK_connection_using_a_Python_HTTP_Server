#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `Grafana_and_SiLK_connection_using_a_Python_HTTP_Server` package."""


import unittest
from click.testing import CliRunner

from Grafana_and_SiLK_connection_using_a_Python_HTTP_Server import Grafana_and_SiLK_connection_using_a_Python_HTTP_Server
from Grafana_and_SiLK_connection_using_a_Python_HTTP_Server import cli


class TestGrafana_and_silk_connection_using_a_python_http_server(unittest.TestCase):
    """Tests for `Grafana_and_SiLK_connection_using_a_Python_HTTP_Server` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Grafana_and_SiLK_connection_using_a_Python_HTTP_Server.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
