import redis

from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

MYSQL_SETTINGS = {
    "host": "192.168.222.9",
    "port": 3306,
    "user": "juwai",
    "passwd": "password"
}


def main():
    r = redis.Redis()

    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        server_id=10,
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
        skip_to_timestamp='1523171'
        )
    print stream
    for binlogevent in stream:
        print 'test'
        prefix = "%s:%s:" % (binlogevent.schema, binlogevent.table)
        print prefix

        for row in binlogevent.rows:
            if isinstance(binlogevent, DeleteRowsEvent):
                vals = row["values"]
                r.delete(prefix + str(vals["id"]))
            elif isinstance(binlogevent, UpdateRowsEvent):
                vals = row["after_values"]
                r.hmset(prefix + str(vals["id"]), vals)
            elif isinstance(binlogevent, WriteRowsEvent):
                vals = row["values"]
                r.hmset(prefix + str(vals["id"]), vals)
    stream.close()


if __name__ == "__main__":
    main()
