# Clinic API API Reference

## Patients

### GET /patients

Returns all patients.

### POST /patients

Creates a patient.

- `riskScore`: integer, minimum 0, maximum 10

## Appointments

### GET /appointments

Returns all appointments.

### POST /appointments

Creates a appointment.

- `durationMinutes`: integer, minimum 10, maximum 180
