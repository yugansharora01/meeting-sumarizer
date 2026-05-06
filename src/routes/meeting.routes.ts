import { Router } from "express";
import { startMeetingBot } from "../controllers/meeting.controller";

export const meetingRouter = Router();

meetingRouter.post("/start-meeting-bot", startMeetingBot);
