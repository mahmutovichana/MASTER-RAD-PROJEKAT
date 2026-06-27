import { Request, Response } from "express";
            import { createCourseSchema } from "./courses.schema";
            import { courseService } from "./courses.service";
            export function listCourses(_req: Request, res: Response) { res.status(200).json({ data: courseService.listCourses() }); }
            export function createCourse(req: Request, res: Response) {
              const input = createCourseSchema.parse(req.body);
              const result = courseService.createCourse(input);
              res.status(201).json({ data: result });
            }
