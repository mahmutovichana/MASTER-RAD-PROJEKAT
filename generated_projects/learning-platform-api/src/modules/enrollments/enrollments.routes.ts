import { Router } from "express";
            import { createEnrollment, listEnrollments } from "./enrollments.controller";

            export const enrollmentRouter = Router();

            enrollmentRouter.get("/", listEnrollments);
            enrollmentRouter.post("/", createEnrollment);
