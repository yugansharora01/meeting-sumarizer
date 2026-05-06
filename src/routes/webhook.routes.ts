import { Router } from "express";
import { handleRecallWebhook } from "../controllers/webhook.controller";

export const webhookRouter = Router();

webhookRouter.post("/webhook", handleRecallWebhook);
