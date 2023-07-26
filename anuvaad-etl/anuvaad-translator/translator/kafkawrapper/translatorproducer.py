import json
import logging
import random

from kafka import KafkaProducer
from configs.translatorconfig import kafka_bootstrap_server_host, total_no_of_partitions
from anuvaad_auditor.errorhandler import post_error
from anuvaad_auditor.loghandler import log_info
from anuvaad_auditor.loghandler import log_exception


log = logging.getLogger('file')


class Producer:

    def __init__(self):
        pass

    # Method to instantiate producer
    # Any other method that needs a producer will get it from her
    def instantiate(self):
        producer = KafkaProducer(bootstrap_servers=list(str(kafka_bootstrap_server_host).split(",")),
                                 api_version=(1, 0, 0),
                                 value_serializer=lambda x: json.dumps(x).encode('utf-8'))
        return producer

    # Method to push records to a topic in the kafka queue
    def produce(self, object_in, topic, partition, translate_wf_input=None):
        producer = self.instantiate()
        try:
            if object_in:
                if partition is None:
                    partition = random.choice(list(range(0, total_no_of_partitions)))
                if translate_wf_input == None:
                    translate_wf_input = object_in
                log_info("Before Pushing to topic: " + str(topic) + " and partition : "+str(partition), translate_wf_input)
                producer.send(topic, value=object_in, partition=partition)
                log_info("Pushing to topic: " + str(topic), translate_wf_input)
            producer.flush()
        except Exception as e:
            log_exception("Exception in translator while producing: " + str(e), translate_wf_input, e)
            post_error("TRANSLATOR_PRODUCER_EXC", "Exception in translator while producing: " + str(e), None)
