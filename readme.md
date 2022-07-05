# Queries to create tables used ->

1. ## cUser table
    ```postgresql
    CREATE TABLE IF NOT EXISTS public.cuser
    (
        id integer NOT NULL DEFAULT nextval('cuser_id_seq'::regclass),
        username text COLLATE pg_catalog."default",
        password text COLLATE pg_catalog."default",
        CONSTRAINT cuser_pkey PRIMARY KEY (id),
        CONSTRAINT cuser_username_key UNIQUE (username)
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.cuser
    OWNER to postgres;
    ```
1. ## projectUserInfo
   ```postgresql
    CREATE TABLE IF NOT EXISTS public.projectuserinfo
    (
        id integer NOT NULL DEFAULT nextval('projectuserinfo_id_seq'::regclass),
        project_name text COLLATE pg_catalog."default" NOT NULL,
        users text COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT projectuserinfo_pkey PRIMARY KEY (id),
        CONSTRAINT projectuserinfo_project_name_key UNIQUE (project_name)
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.projectuserinfo
    OWNER to postgres;
   ```
1. ## userHierarchyProjects
   ```postgresql
    CREATE TABLE IF NOT EXISTS public.userhierarchyprojects
    (
        id integer NOT NULL DEFAULT nextval('userhierarchyprojects_id_seq'::regclass),
        project_id integer NOT NULL,
        status text COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT userhierarchyprojects_pkey PRIMARY KEY (id),
        CONSTRAINT userhierarchyprojects_project_id_fkey FOREIGN KEY (project_id)
            REFERENCES public.projectuserinfo (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.userhierarchyprojects
        OWNER to postgres;
   ```

1. ## projectData
   ```postgresql
    CREATE TABLE IF NOT EXISTS public.projectdata
    (
        id integer NOT NULL DEFAULT nextval('projectdata_id_seq'::regclass),
        project_id integer NOT NULL,
        tag text COLLATE pg_catalog."default" NOT NULL,
        tag_color text COLLATE pg_catalog."default" NOT NULL,
        by_user text COLLATE pg_catalog."default" NOT NULL,
        column_name text COLLATE pg_catalog."default" NOT NULL,
        description text COLLATE pg_catalog."default" NOT NULL,
        asigned_to integer,
        CONSTRAINT projectdata_pkey PRIMARY KEY (id),
        CONSTRAINT asigned_to_fk FOREIGN KEY (asigned_to)
            REFERENCES public.cuser (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,
        CONSTRAINT projectdata_by_user_fkey FOREIGN KEY (by_user)
            REFERENCES public.cuser (username) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,
        CONSTRAINT projectdata_project_id_fkey FOREIGN KEY (project_id)
            REFERENCES public.projectuserinfo (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.projectdata
        OWNER to postgres;
   ```