import { Request, Response } from "express";
            import { createPatientSchema } from "./patients.schema";
            import { patientService } from "./patients.service";
            export function listPatients(_req: Request, res: Response) { res.status(200).json({ data: patientService.listPatients() }); }
            export function createPatient(req: Request, res: Response) {
              const input = createPatientSchema.parse(req.body);
              const result = patientService.createPatient(input);
              res.status(201).json({ data: result });
            }
