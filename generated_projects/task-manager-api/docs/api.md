# Task Manager API Documentation

## Tasks

            ### GET /tasks

            Returns all tasks.

            Response: `200 OK`

            ### POST /tasks

            Creates a task.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `priority`: integer, minimum 1, maximum 5

            Response: `201 Created`
## Projects

            ### GET /projects

            Returns all projects.

            Response: `200 OK`

            ### POST /projects

            Creates a project.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `memberLimit`: integer, minimum 1, maximum 50

            Response: `201 Created`
