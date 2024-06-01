------------------------------------------------------------- [ Extensions >>>
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
-------------------------------------------------------------- <<< Extension ]

-------------------------------------------------------- [ fn_create_table >>>
CREATE OR REPLACE FUNCTION public.fn_create_table(sch character varying, tbl character varying)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
    EXECUTE format('
        CREATE TABLE IF NOT EXISTS %I.%I (
            id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
            seq SERIAL
        )
    ', sch, tbl);
END;
$function$
;
-------------------------------------------------------- <<< fn_create_table ]

------------------------------------------------- [ fn_add_actions_columns >>>
CREATE OR REPLACE FUNCTION public.fn_add_actions_columns(schemaname character varying, tablename character varying)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
	EXECUTE format('ALTER TABLE %I.%I ADD COLUMN IF NOT EXISTS enabled_at TIMESTAMP WITH TIME ZONE', schemaname, tablename);
	EXECUTE format('ALTER TABLE %I.%I ADD COLUMN IF NOT EXISTS disabled_at TIMESTAMP WITH TIME ZONE', schemaname, tablename);
END
$function$
;
------------------------------------------------- <<< fn_add_actions_columns ]

-------------------------------------------------- [ fn_add_deleted_column >>>
CREATE OR REPLACE FUNCTION public.fn_add_deleted_column(schemaname character varying, tablename character varying)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
	EXECUTE format('ALTER TABLE %I.%I ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP WITH TIME ZONE', schemaname, tablename);
END
$function$
;
-------------------------------------------------- <<< fn_add_deleted_column ]

-------------------------------------------------- [ fn_add_created_column >>>
CREATE OR REPLACE FUNCTION public.fn_add_created_column(schemaname character varying, tablename character varying)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
BEGIN
	EXECUTE format('ALTER TABLE %I.%I ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP', schemaname, tablename);
END
$function$
;
-------------------------------------------------- <<< fn_add_created_column ]

---------------- [ fn_set_updated_at_to_current_timestamp_when_row_changed >>>
CREATE OR REPLACE FUNCTION public.fn_set_updated_at_to_current_timestamp_when_row_changed()
	RETURNS TRIGGER AS $fn_set_updated_at_to_current_timestamp_when_row_changed$
BEGIN
	NEW.updated_at := CURRENT_TIMESTAMP;
	RETURN NEW;
END
$fn_set_updated_at_to_current_timestamp_when_row_changed$ LANGUAGE plpgsql;
---------------- <<< fn_set_updated_at_to_current_timestamp_when_row_changed ]

-------------------------------------------------- [ fn_add_updated_column >>>
CREATE OR REPLACE FUNCTION public.fn_add_updated_column(schemaname VARCHAR, tablename VARCHAR)
	RETURNS void AS $fn_add_updated_column$
BEGIN
	EXECUTE format('ALTER TABLE %I.%I ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP', schemaname, tablename);

	EXECUTE format('
		DROP TRIGGER IF EXISTS tr_%I_%I_updated_at
			ON %I.%I
	', schemaname, tablename, schemaname, tablename);

	EXECUTE format('
		CREATE TRIGGER tr_%I_%I_updated_at BEFORE INSERT OR UPDATE ON %I.%I
			FOR EACH ROW EXECUTE FUNCTION fn_set_updated_at_to_current_timestamp_when_row_changed()
	', schemaname, tablename, schemaname, tablename);
END
$fn_add_updated_column$ LANGUAGE plpgsql;
-------------------------------------------------- <<< fn_add_updated_column ]
