""" Tests for the Migration tools
"""

import pytest
from unittest.mock import Mock, patch

from styler_rest_framework.helpers import migration


class TestCheckAndRetryMigration:
    """ Tests for check_and_retry_migration
    """
    def test_version_up_to_date(self):
        """ It should return without errors
        """
        migration.get_heads_version = Mock(return_value=['head'])
        migration.get_current_version = Mock(return_value='head')

        migration.check_and_retry_migration('mock_path')

        migration.get_heads_version.assert_called_once()
        migration.get_current_version.assert_called_once()

    def test_multiple_head(self):
        """ It should raise migration error
        """
        migration.get_heads_version = Mock(return_value=['head1', 'head2'])
        migration.get_current_version = Mock(return_value='head')

        with pytest.raises(migration.MigrationError) as expected:
            migration.check_and_retry_migration('mock_path')

        assert "multiple heads detected!" in str(expected.value)

        migration.get_heads_version.assert_called_once()

    @patch('alembic.command.upgrade')
    @patch('logging.warning')
    def test_retry_success(self, log_mock, upgrade_mock):
        """ It should return without errors
        """
        migration.get_heads_version = Mock(return_value=['head'])
        migration.get_current_version = Mock(return_value='old_version')

        migration.check_and_retry_migration('mock_path')

        migration.get_heads_version.assert_called_once()
        migration.get_current_version.assert_called_once()
        upgrade_mock.assert_called_once()
        log_mock.assert_any_call('alembic version is not up-to-date, \
        will retry migration...')

    @patch('logging.warning')
    def test_retry_failed(self, log_mock):
        """ It should raise migration error
        """
        migration.get_heads_version = Mock(return_value=['head'])
        migration.get_current_version = Mock(return_value='old_version')

        with patch('alembic.command.upgrade',
                   side_effect=Exception()) as upgrade_mock:
            with pytest.raises(migration.MigrationError) as expected:
                migration.check_and_retry_migration('mock_path',
                                                    max_retry_count=3)

            migration.get_heads_version.assert_called_once()
            migration.get_current_version.assert_called_once()
            assert 3 == upgrade_mock.call_count
            assert "Could not execute alembic migrations." in str(
                expected.value)

    def test_missing_parameter(self):
        with pytest.raises(migration.MigrationError) as expected:
            migration.check_and_retry_migration('')

        assert "parameter required: cfg_path" in str(expected.value)
