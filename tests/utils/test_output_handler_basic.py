import unittest

from app.output_handler import OutputDispatcher
from app.utils.types import OutputMode


class TestOutputDispatcherBasic(unittest.TestCase):
    def test_output_dispatcher_init(self):
        dispatcher = OutputDispatcher()
        self.assertIsInstance(dispatcher.output_modes, list)

    def test_get_dispatch_method(self):
        dispatcher = OutputDispatcher()
        method = dispatcher._get_dispatch_method(OutputMode.LOG)
        self.assertTrue(callable(method))


if __name__ == "__main__":
    unittest.main()
