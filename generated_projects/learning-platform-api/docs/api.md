# Learning Platform API Documentation

## Courses

            ### GET /courses

            Returns all courses.

            Response: `200 OK`

            ### POST /courses

            Creates a course.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `lessonCount`: integer, minimum 1, maximum 80

            Response: `201 Created`
## Enrollments

            ### GET /enrollments

            Returns all enrollments.

            Response: `200 OK`

            ### POST /enrollments

            Creates a enrollment.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `progressPercent`: integer, minimum 0, maximum 100

            Response: `201 Created`
