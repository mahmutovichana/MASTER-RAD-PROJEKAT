import { Request, Response } from "express";
            import { createEnrollmentSchema } from "./enrollments.schema";
            import { enrollmentService } from "./enrollments.service";

            export function listEnrollments(_req: Request, res: Response) {
              res.status(200).json({ data: enrollmentService.listEnrollments() });
            }

            export function createEnrollment(req: Request, res: Response) {
              const input = createEnrollmentSchema.parse(req.body);
              const result = enrollmentService.createEnrollment(input);
              res.status(201).json({ data: result });
            }
