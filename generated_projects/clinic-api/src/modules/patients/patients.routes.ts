import { Router } from "express";
            import { createPatient, listPatients } from "./patients.controller";

            export const patientRouter = Router();

            patientRouter.get("/", listPatients);
            patientRouter.post("/", createPatient);
