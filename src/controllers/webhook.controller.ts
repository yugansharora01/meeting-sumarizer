import { Request, Response } from "express";
import { generateMeetingSummary } from "../services/ai.service";
import { sendMeetingSummaryEmail } from "../services/email.service";
import { appendTranscript, getMeeting, markMeetingStatus, updateMeeting } from "../stores/meeting.store";
import { RecallWebhookPayload } from "../types/meeting";
import { extractBotId, extractRecordingUrl, extractTranscript, shouldFinalizeMeeting } from "../utils/webhook";

export const handleRecallWebhook = async (req: Request, res: Response): Promise<void> => {
  const payload = req.body as RecallWebhookPayload;
  const botId = extractBotId(payload);

  if (!botId) {
    res.status(400).json({ success: false, message: "Webhook payload missing bot id" });
    return;
  }

  const meeting = getMeeting(botId);
  if (!meeting) {
    res.status(202).json({ success: true, message: "Webhook accepted for unknown bot" });
    return;
  }

  const transcript = extractTranscript(payload);
  const recordingUrl = extractRecordingUrl(payload);

  let updatedMeeting = meeting;
  if (transcript.length > 0) {
    updatedMeeting = appendTranscript(botId, transcript) ?? updatedMeeting;
  }

  if (recordingUrl) {
    updatedMeeting = updateMeeting(botId, { recordingUrl }) ?? updatedMeeting;
  }

  if (!shouldFinalizeMeeting(payload)) {
    res.json({ success: true, message: "Webhook processed" });
    return;
  }

  if (updatedMeeting.transcript.length === 0) {
    markMeetingStatus(botId, "failed", "No transcript received before completion");
    res.status(422).json({ success: false, message: "No transcript available to summarize" });
    return;
  }

  try {
    const summary = await generateMeetingSummary(updatedMeeting.transcript);
    await sendMeetingSummaryEmail({
      to: updatedMeeting.email,
      summary,
      recordingUrl: updatedMeeting.recordingUrl,
    });

    updateMeeting(botId, { summary, status: "summary_sent" });
    res.json({ success: true, message: "Summary email sent" });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Failed to process meeting summary";
    markMeetingStatus(botId, "failed", message);
    res.status(500).json({ success: false, message });
  }
};
