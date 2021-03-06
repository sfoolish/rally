# Copyright 2013: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

import mock
from oslo_config import fixture
from oslotest import base

from rally import db


class DatabaseFixture(fixture.Config):
    """Create clean DB before starting test."""
    def setUp(self):
        super(DatabaseFixture, self).setUp()
        db_url = os.environ.get("RALLY_UNITTEST_DB_URL", "sqlite://")
        db.db_cleanup()
        self.conf.set_default("connection", db_url, group="database")
        db.db_drop()
        db.db_create()


class TestCase(base.BaseTestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        super(TestCase, self).setUp()
        self.addCleanup(mock.patch.stopall)

    def _test_atomic_action_timer(self, atomic_actions, name):
        action_duration = atomic_actions.get(name)
        self.assertIsNotNone(action_duration)
        self.assertIsInstance(action_duration, float)

    def assertSequenceEqual(self, iterable_1, iterable_2):
        self.assertEqual(tuple(iterable_1), tuple(iterable_2))


class DBTestCase(TestCase):
    """Base class for tests which use DB."""

    def setUp(self):
        super(DBTestCase, self).setUp()
        self.useFixture(DatabaseFixture())
