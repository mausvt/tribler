from tribler_core.restapi.base_api_test import AbstractApiTest
from tribler_core.tests.tools.tools import timeout
from tribler_core.utilities.utilities import succeed


class TestShutdownEndpoint(AbstractApiTest):

    @timeout(10)
    async def test_shutdown(self):
        """
        Testing whether the API triggers a Tribler shutdown
        """
        self.orig_shutdown = self.session.shutdown
        self.shutdown_called = False

        def fake_shutdown():
            # Record session.shutdown was called
            self.shutdown_called = True
            # Restore original shutdown for test teardown
            self.session.shutdown = self.orig_shutdown
            return succeed(True)

        self.session.shutdown = fake_shutdown

        expected_json = {"shutdown": True}
        await self.do_request('shutdown', expected_code=200, expected_json=expected_json, request_type='PUT')
        self.assertTrue(self.shutdown_called)
