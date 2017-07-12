from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cqlengine.management import create_keyspace_simple

try:
    from machine_settings import CASSANDRA_USERNAME, CASSANDRA_PASSWORD
except ImportError:
    raise Exception('Please create machine_settings.py with CASSANDRA_USERNAME and CASSANDRA_PASSWORD')

class BaseModel(Model):
    __abstract__ = True
    @classmethod
    def log(cls, **kwargs):
        obj = cls.create(**kwargs)
        return obj

class CronTraceByCron(BaseModel):
    command_name = columns.Text(partition_key=True)
    log_timestamp = columns.DateTime(primary_key=True)
    state = columns.Integer(primary_key=True)
    state_verbose = columns.Text()
    context = columns.Map(columns.Text(), columns.Text())
    hostname = columns.Text()

KEYSPACE = 'cronlog'

def create_keyspace():
    create_keyspace_simple(KEYSPACE, replication_factor=1)


def setup_connection():
    auth_provider = PlainTextAuthProvider(
            username=CASSANDRA_USERNAME, password=CASSANDRA_PASSWORD)
    connection.setup(['127.0.0.1'], KEYSPACE, protocol_version=3, auth_provider=auth_provider)


def setup_models():
    setup_connection()
    sync_table(CronTraceByCron)


def drop_models():
    setup_connection()
    drop_table(CronTraceByCron)
