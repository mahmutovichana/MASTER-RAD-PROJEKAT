import { Router } from 'express';
export const router = Router();
router.get('/reviews/:id', getReview);
