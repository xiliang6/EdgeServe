import pulsar


class DataSource:
    def __init__(self, stream, pulsar_node, gate=None, topic='src'):
        self.client = pulsar.Client(pulsar_node)
        self.producer = self.client.create_producer(topic)
        self.stream = iter(stream)
        self.gate = (lambda x: x.encode('utf-8')) if gate is None else gate

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def __iter__(self):
        return self

    def __next__(self):
        data = self.gate(next(self.stream))
        self.producer.send(data)
        return data
