# Task Manager API API Reference

## Tasks

### GET /tasks

Returns all tasks.

### POST /tasks

Creates a task.

- `priority`: integer, minimum 1, maximum 5

## Projects

### GET /projects

Returns all projects.

### POST /projects

Creates a project.

- `memberLimit`: integer, minimum 1, maximum 50
