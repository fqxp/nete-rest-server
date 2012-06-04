import unittest
import mock
import nete.utils
import uuid

class TestUUIDEncoder(unittest.TestCase):

    def setUp(self):
        self.uuid_encoder = nete.utils.UUIDEncoder()

    def test_encode_arbitrary_value_uses_default_encoding(self):
        with mock.patch('json.JSONEncoder.default') as base_default_mock:
            base_default_mock.return_value = 'bar foo'
            self.uuid_encoder.default('foo bar')

            base_default_mock.assert_called_once_with(self.uuid_encoder, 'foo bar')

    def test_encode_uuid_returns_uuid_string_representation(self):
        result = self.uuid_encoder.default(uuid.UUID('347d4132-ae66-4284-84a7-f27be5f482a6'))

        self.assertEquals('347d4132-ae66-4284-84a7-f27be5f482a6', result)
