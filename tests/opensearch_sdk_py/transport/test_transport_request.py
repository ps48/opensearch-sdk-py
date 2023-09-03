import unittest

from opensearch_sdk_py.transport.stream_input import StreamInput
from opensearch_sdk_py.transport.stream_output import StreamOutput
from opensearch_sdk_py.transport.task_id import TaskId
from opensearch_sdk_py.transport.transport_request import TransportRequest


class TestTransportRequest(unittest.TestCase):
    def test_transport_request(self):
        tr = TransportRequest(TaskId("test", 42))
        self.assertEqual(tr.parent_task_id.node_id, "test")
        self.assertEqual(tr.parent_task_id.id, 42)

        out = StreamOutput()
        tr.write_to(out)
        out.write(b"\x01\x02\x03")
        self.assertEqual(
            out.getvalue(), b"\x04test\x00\x00\x00\x00\x00\x00\x00\x2a\x01\x02\x03"
        )

        tr = TransportRequest()
        self.assertEqual(tr.parent_task_id.node_id, "")
        self.assertEqual(tr.parent_task_id.id, -1)
        tr.read_from(input=StreamInput(out.getvalue()))
        self.assertEqual(tr.parent_task_id.node_id, "test")
        self.assertEqual(tr.parent_task_id.id, 42)
