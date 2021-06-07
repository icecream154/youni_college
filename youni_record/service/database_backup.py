import time

from project_config import PROJECT_ROOT

requests_received = 0
backup_open = True


def backup(func):
    def wrapper(request):
        global requests_received
        global backup_open
        requests_received += 1
        if backup_open and requests_received % 5 == 0:
            with open(PROJECT_ROOT + '/db.sqlite3', 'rb') as f_read_db:
                db_data = f_read_db.read()
            with open(PROJECT_ROOT + '/backup/db-' + str(requests_received / 5) + '-' +
                      time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.sqlite3', 'wb') as f_write_db:
                f_write_db.write(db_data)

            print('backup %d success at %s' % (requests_received / 5,
                                               time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        return func(request)
    return wrapper
