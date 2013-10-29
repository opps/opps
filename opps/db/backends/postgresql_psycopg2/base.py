#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
INSTALL:
    apt-get install postgresql-contrib-9.1

RUN IN DBSHELL
   CREATE EXTENSION IF NOT EXISTS unaccent;

USAGE:

DATABASES = {
    'default': {
        'ENGINE': 'opps.db.backends.postgresql_psycopg2',
        ...
    }
}

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}

DATABASE_POOL_ARGS = {
    'max_overflow': 10,
    'pool_size': 5,
    'recycle': 300
}
"""
import logging
from functools import partial

from sqlalchemy import event
from sqlalchemy.pool import manage, QueuePool
from psycopg2 import InterfaceError, ProgrammingError, OperationalError

from django.conf import settings
from django.db.backends.postgresql_psycopg2.base import *
from django.db.backends.postgresql_psycopg2.base import \
    DatabaseWrapper as Psycopg2DatabaseWrapper
from django.db.backends.postgresql_psycopg2.base import \
    CursorWrapper as DjangoCursorWrapper
from django.db.backends.postgresql_psycopg2.creation \
    import DatabaseCreation as Psycopg2DatabaseCreation


class DatabaseOperations(DatabaseOperations):
    def lookup_cast(self, lookup_type):
        if lookup_type in('icontains', 'istartswith'):
            return "UPPER(unaccent(%s::text))"
        else:
            return super(DatabaseOperations, self).lookup_cast(lookup_type)

"""
# Uncomment this class to disable the pool
class DatabaseWrapper(DatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.operators['icontains'] = 'LIKE UPPER(unaccent(%s))'
        self.operators['istartswith'] = 'LIKE UPPER(unaccent(%s))'
        self.ops = DatabaseOperations(self)

# comment everything below to disable the pool
"""

POOL_SETTINGS = 'DATABASE_POOL_ARGS'

# DATABASE_POOL_ARGS should be something like:
# {'max_overflow':10, 'pool_size':5, 'recycle':300}
pool_args = getattr(settings, POOL_SETTINGS, {})
db_pool = manage(Database, **pool_args)

log = logging.getLogger('z.pool')


def _log(message, *args):
    log.debug(message)


# Only hook up the listeners if we are in debug mode.
if settings.DEBUG:
    event.listen(QueuePool, 'checkout', partial(_log, 'retrieved from pool'))
    event.listen(QueuePool, 'checkin', partial(_log, 'returned to pool'))
    event.listen(QueuePool, 'connect', partial(_log, 'new connection'))


def is_disconnect(e, connection, cursor):
    """
    Connection state check from SQLAlchemy:
    https://bitbucket.org/sqlalchemy/sqlalchemy/src/tip/
        lib/sqlalchemy/dialects/postgresql/psycopg2.py
    """
    if isinstance(e, OperationalError):
        # these error messages from libpq: interfaces/libpq/fe-misc.c.
        # TODO: these are sent through gettext in libpq and we can't
        # check within other locales - consider using connection.closed
        return 'terminating connection' in str(e) or \
               'closed the connection' in str(e) or \
               'connection not open' in str(e) or \
               'could not receive data from server' in str(e)
    elif isinstance(e, InterfaceError):
        # psycopg2 client errors, psycopg2/conenction.h, psycopg2/cursor.h
        return 'connection already closed' in str(e) or \
               'cursor already closed' in str(e)
    elif isinstance(e, ProgrammingError):
        # not sure where this path is originally from, it may
        # be obsolete.   It really says "losed", not "closed".
        return "losed the connection unexpectedly" in str(e)
    else:
        return False


class CursorWrapper(DjangoCursorWrapper):
    """
    A thin wrapper around psycopg2's normal cursor class so that we can catch
    particular exception instances and reraise them with the right types.

    Checks for connection state on DB API error and invalidates
    broken connections.
    """

    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def execute(self, query, args=None):
        try:
            return self.cursor.execute(query, args)
        except Database.IntegrityError, e:
            raise utils.IntegrityError, utils.IntegrityError(
                *tuple(e)), sys.exc_info()[2]
        except Database.DatabaseError, e:
            if is_disconnect(e, self.connection.connection, self.cursor):
                log.error("invalidating broken connection")
                self.connection.invalidate()
            raise utils.DatabaseError, utils.DatabaseError(
                *tuple(e)), sys.exc_info()[2]

    def executemany(self, query, args):
        try:
            return self.cursor.executemany(query, args)
        except Database.IntegrityError, e:
            raise utils.IntegrityError, utils.IntegrityError(
                *tuple(e)), sys.exc_info()[2]
        except Database.DatabaseError, e:
            if is_disconnect(e, self.connection.connection, self.cursor):
                log.error("invalidating broken connection")
                self.connection.invalidate()
            raise utils.DatabaseError, utils.DatabaseError(
                *tuple(e)), sys.exc_info()[2]


class DatabaseCreation(Psycopg2DatabaseCreation):
    def destroy_test_db(self, *args, **kw):
        """Ensure conn pool is disposed before trying to drop database."""
        self.connection._dispose()
        super(DatabaseCreation, self).destroy_test_db(*args, **kw)


class DatabaseWrapper(Psycopg2DatabaseWrapper):
    """SQLAlchemy FTW."""

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.creation = DatabaseCreation(self)
        self.operators['icontains'] = 'LIKE UPPER(unaccent(%s))'
        self.operators['istartswith'] = 'LIKE UPPER(unaccent(%s))'
        self.ops = DatabaseOperations(self)

    def _cursor(self):
        if self.connection is None or self.connection.is_valid is False:
            self.connection = db_pool.connect(**self._get_conn_params())
            self.connection.set_client_encoding('UTF8')
            tz = 'UTC' if settings.USE_TZ else self.settings_dict.get(
                'TIME_ZONE')
            if tz:
                try:
                    get_parameter_status = self.connection.get_parameter_status
                except AttributeError:
                    # psycopg2 < 2.0.12 doesn't have get_parameter_status
                    conn_tz = None
                else:
                    conn_tz = get_parameter_status('TimeZone')

                if conn_tz != tz:
                    # Set the time zone in autocommit mode (see #17062)
                    self.connection.set_isolation_level(
                        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                    self.connection.cursor().execute(
                        self.ops.set_time_zone_sql(), [tz])
            self.connection.set_isolation_level(self.isolation_level)
            self._get_pg_version()
            connection_created.send(sender=self.__class__, connection=self)
        cursor = self.connection.cursor()
        cursor.tzinfo_factory = utc_tzinfo_factory if settings.USE_TZ else None
        return CursorWrapper(cursor, self.connection)

    def _commit(self):
        if self.connection is not None and self.connection.is_valid:
            return self.connection.commit()

    def _rollback(self):
        if self.connection is not None and self.connection.is_valid:
            return self.connection.rollback()

    def _dispose(self):
        """Dispose of the pool for this instance, closing all connections."""
        self.close()
        # _DBProxy.dispose doesn't actually call dispose on the pool
        conn_params = self._get_conn_params()
        key = db_pool._serialize(**conn_params)
        try:
            pool = db_pool.pools[key]
        except KeyError:
            pass
        else:
            pool.dispose()
            del db_pool.pools[key]

    def _get_conn_params(self):
        settings_dict = self.settings_dict
        if not settings_dict['NAME']:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(
                "settings.DATABASES is improperly configured. "
                "Please supply the NAME value.")
        conn_params = {
            'database': settings_dict['NAME'],
        }
        conn_params.update(settings_dict['OPTIONS'])
        if 'autocommit' in conn_params:
            del conn_params['autocommit']
        if settings_dict['USER']:
            conn_params['user'] = settings_dict['USER']
        if settings_dict['PASSWORD']:
            conn_params['password'] = settings_dict['PASSWORD']
        if settings_dict['HOST']:
            conn_params['host'] = settings_dict['HOST']
        if settings_dict['PORT']:
            conn_params['port'] = settings_dict['PORT']
        return conn_params
