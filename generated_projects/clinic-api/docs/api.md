# Clinic API Documentation

## Patients

            ### GET /patients

            Returns all patients.

            Response: `200 OK`

            ### POST /patients

            Creates a patient.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `riskScore`: integer, minimum 0, maximum 10

            Response: `201 Created`
## Appointments

            ### GET /appointments

            Returns all appointments.

            Response: `200 OK`

            ### POST /appointments

            Creates a appointment.

            Request fields:

            - `name`: string, minimum length 2
            - `status`: one of `draft`, `active`, `archived`
            - `durationMinutes`: integer, minimum 10, maximum 180

            Response: `201 Created`
