"""File containing PostgreSQL procedure to retrieve label mapping in json text format"""

__LOGINS__ = '''CREATE OR REPLACE FUNCTION github.pg_User_GetLogins() RETURNS TEXT AS
$BODY$
DECLARE
    l_json TEXT;
BEGIN
    SELECT JSON_OBJECT_AGG(t1.id, t1.login)::TEXT
    INTO STRICT l_json
    FROM (
             SELECT id, login
             FROM github.t_user
         ) t1;

    SELECT id
    FROM github.t_user;

    RETURN l_json;
END;
$BODY$ LANGUAGE plpgsql'''

ROUTINES = [__LOGINS__]