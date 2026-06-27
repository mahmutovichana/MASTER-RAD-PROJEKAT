import express from "express";
        import { courseRouter } from "./modules/courses/courses.routes";
import { enrollmentRouter } from "./modules/enrollments/enrollments.routes";

        export const app = express();

        app.use(express.json());
        app.use("/courses", courseRouter);
app.use("/enrollments", enrollmentRouter);

        app.get("/health", (_req, res) => {
          res.status(200).json({ status: "ok" });
        });
