import { Request, Response } from "express";
import { createMeetingBot } from "../services/recall.service";
import { saveMeeting } from "../stores/meeting.store";

export const startMeetingBot = async (req: Request, res: Response): Promise<void> => {
  const { meetingUrl, email } = req.body as { meetingUrl?: string; email?: string };

  if (!meetingUrl || !email) {
    res.status(400).json({
      success: false,
      message: "meetingUrl and email are required",
    });
    return;
  }

  try {
    const bot = await createMeetingBot(meetingUrl);
    const botId = bot.id ?? bot.bot_id;

    if (!botId) {
      res.status(502).json({
        success: false,
        message: "Recall API did not return a bot id",
        recallResponse: bot,
      });
      return;
    }

    saveMeeting({
      botId,
      meetingUrl,
      email,
      status: "bot_created",
      transcript: [],
    });

    res.status(201).json({
      success: true,
      message: "Bot started",
      botId,
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Failed to start meeting bot";
    res.status(500).json({ success: false, message });
  }
};
