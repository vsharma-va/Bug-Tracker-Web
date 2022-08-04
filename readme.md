# Queries to create tables used ->

1.  ## cUser table

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

1.  ## projectUserInfo

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

1.  ## userHierarchyProjects

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

1.  ## projectData (Updated)

    ```sql
     CREATE TABLE IF NOT EXISTS public.projectdata
    (
     id serial NOT NULL,
     project_id integer NOT NULL,
     tag text COLLATE pg_catalog."default" NOT NULL,
     tag_color text COLLATE pg_catalog."default" NOT NULL,
     column_name text COLLATE pg_catalog."default" NOT NULL,
     description text COLLATE pg_catalog."default" NOT NULL,
     by_user integer,
     assigned_to integer,
     col_pos integer,
     steps_to_reproduce text COLLATE pg_catalog."default",
     expected_behaviour text COLLATE pg_catalog."default",
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
    ```

1.  ## userInvites

    ```sql
    CREATE TABLE IF NOT EXISTS public.userinvites
    (
        id serial,
        created_by integer,
        key bytea,
        encrypted_code bytea,
        nonce_length integer,
        date_time_created timestamp without time zone,
        CONSTRAINT userinvites_pkey PRIMARY KEY (id),
        CONSTRAINT userinvites_created_by_fkey FOREIGN KEY (created_by)
            REFERENCES public.cuser (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )

    TABLESPACE pg_default;
    ALTER TABLE IF EXISTS public.userinvites
    OWNER to postgres;
    ```

1.  ## projectRoles (new)

    ```sql
    CREATE TABLE IF NOT EXISTS public.projectroles
    (
        id serial,
        project_id integer NOT NULL,
        can_delete_from text COLLATE pg_catalog."default",
        can_move_to_and_from text COLLATE pg_catalog."default",
        role_name text COLLATE pg_catalog."default",
        CONSTRAINT projectroles_pkey PRIMARY KEY (id),
        CONSTRAINT projectroles_project_id_fkey FOREIGN KEY (project_id)
            REFERENCES public.projectuserinfo (id) MATCH SIMPLE
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    )

    TABLESPACE pg_default;
    ALTER TABLE IF EXISTS public.projectroles
    OWNER to postgres;
    ```

# Insert queries to get started (execute them in order given) ->

1.  ## Create User

    ```
    Create user by going to localhost:5000/auth/register
    ```

1.  ## Project user info

    ```sql
    insert into projectuserinfo (project_name, users) values("Hello There", "1")
    ```

1.  ## Project data

    ```sql
    insert into projectdata (project_id, tag, tag_color, column_name, description, by_user, assigned_to) values (1, 'Severe', 'red', 'open', 'There is some problem in the database please check it out asap.', 1, 1, 1);
    ```

1.  ## User hierarchy

    ```sql
    insert into userhierarchyprojects (project_id, status, user_id) values(1, 'admin', 1)
    ```

# Current Progress ->

## Landing Page

![Dashboard](https://github.com/vsharma-va/Bug-Tracker-Web/blob/main/progress-images/Dashboard-1.jpg?raw=true)

## Landing Page part 2

![Dasboard 2](https://github.com/vsharma-va/Bug-Tracker-Web/blob/main/progress-images/Dashboard-2.jpg?raw=true)

## Dashboard Create Popup

![Dasboard 2](https://github.com/vsharma-va/Bug-Tracker-Web/blob/main/progress-images/Dashboard-create.jpg?raw=true)

## Dasboard Invite Popup

![Dasboard 2](https://github.com/vsharma-va/Bug-Tracker-Web/blob/main/progress-images/Dashboard-invite.jpg?raw=true)

## View All Page

![Dasboard 2](https://github.com/vsharma-va/Bug-Tracker-Web/blob/main/progress-images/view-all.jpg?raw=true)
