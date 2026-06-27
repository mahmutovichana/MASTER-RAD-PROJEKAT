import express from "express";
        import { patientRouter } from "./modules/patients/patients.routes";
import { appointmentRouter } from "./modules/appointments/appointments.routes";

        export const app = express();

        app.use(express.json());
        app.use("/patients", patientRouter);
app.use("/appointments", appointmentRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
