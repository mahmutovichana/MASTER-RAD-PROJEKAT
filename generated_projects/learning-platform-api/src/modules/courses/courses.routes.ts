import { Router } from "express";
            import { createCourse, listCourses } from "./courses.controller";

            export const courseRouter = Router();

            courseRouter.get("/", listCourses);
            courseRouter.post("/", createCourse);
