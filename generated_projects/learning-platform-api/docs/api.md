# Learning Platform API API Reference

## Courses

### GET /courses

Returns all courses.

### POST /courses

Creates a course.

- `lessonCount`: integer, minimum 1, maximum 80

## Enrollments

### GET /enrollments

Returns all enrollments.

### POST /enrollments

Creates a enrollment.

- `progressPercent`: integer, minimum 0, maximum 100
