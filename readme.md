# Queries to create tables used ->

1. ## cUser table (Updated)
    ```sql
    CREATE TABLE IF NOT EXISTS public.cuser
    (
        id serial,
        username text COLLATE pg_catalog."default",
        password text COLLATE pg_catalog."default",
        CONSTRAINT cuser_pkey PRIMARY KEY (id),
        CONSTRAINT cuser_username_key UNIQUE (username)
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.cuser
    OWNER to postgres;
    ```
1. ## projectUserInfo (Updated)
   ```sql
    CREATE TABLE IF NOT EXISTS public.projectuserinfo
    (
        id serial,
        project_name text COLLATE pg_catalog."default" NOT NULL,
        users text COLLATE pg_catalog."default" NOT NULL,
        CONSTRAINT projectuserinfo_pkey PRIMARY KEY (id),
        CONSTRAINT projectuserinfo_project_name_key UNIQUE (project_name)
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.projectuserinfo
    OWNER to postgres;
   ```
1. ## userHierarchyProjects (Updated    )
   ```sql
    CREATE TABLE IF NOT EXISTS public.userhierarchyprojects
    (
        id serial,
        project_id integer NOT NULL,
        status text COLLATE pg_catalog."default" NOT NULL,
        user_id integer NOT NULL,
        CONSTRAINT userhierarchyprojects_pkey PRIMARY KEY (id),
        CONSTRAINT user_id_fk FOREIGN KEY (user_id)
            REFERENCES public.cuser (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,
        CONSTRAINT userhierarchyprojects_project_id_fkey FOREIGN KEY (project_id)
            REFERENCES public.projectuserinfo (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )

    TABLESPACE pg_default;

    ALTER TABLE IF EXISTS public.userhierarchyprojects
        OWNER to postgres;
   ```

1. ## projectData (Updated)
   ```sql
    CREATE TABLE IF NOT EXISTS public.projectdata
    (
        id serial,
        project_id integer NOT NULL,
        tag text COLLATE pg_catalog."default" NOT NULL,
        tag_color text COLLATE pg_catalog."default" NOT NULL,
        column_name text COLLATE pg_catalog."default" NOT NULL,
        description text COLLATE pg_catalog."default" NOT NULL,
        by_user integer,
        assigned_to integer,
        col_pos integer,
        CONSTRAINT projectdata_pkey PRIMARY KEY (id),
        CONSTRAINT assigned_to FOREIGN KEY (assigned_to)
            REFERENCES public.cuser (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION,
        CONSTRAINT by_user_fk FOREIGN KEY (by_user)
            REFERENCES public.cuser (id) MATCH SIMPLE
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

## Insert queries to get started (execute them in order given) ->
1. ## Create User
    ```
    Create user by going to localhost:5000/auth/register
    ```

1. ## Project user info
    ```sql
    insert into projectuserinfo (project_name, users) values("Hello There", "1")
    ```

1. ## Project data
    ```sql
    insert into projectdata (project_id, tag, tag_color, column_name, description, by_user, assigned_to) values (1, 'Severe', 'red', 'open', 'There is some problem in the database please check it out asap.', 1, 1, 1);
    ```

1. ## User hierarchy
    ```sql
    insert into userhierarchyprojects (project_id, status, user_id) values(1, 'admin', 1)
    ```