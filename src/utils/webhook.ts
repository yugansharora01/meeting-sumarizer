import { RecallWebhookPayload, TranscriptSegment } from "../types/meeting";

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null;

export const extractBotId = (payload: RecallWebhookPayload): string | undefined => {
  if (typeof payload.bot_id === "string") {
    return payload.bot_id;
  }

  if (typeof payload.bot?.id === "string") {
    return payload.bot.id;
  }

  if (isRecord(payload.data)) {
    const botId = payload.data.bot_id ?? (isRecord(payload.data.bot) ? payload.data.bot.id : undefined);
    return typeof botId === "string" ? botId : undefined;
  }

  return undefined;
};

export const extractTranscript = (payload: RecallWebhookPayload): TranscriptSegment[] => {
  const transcript = payload.data?.transcript;
  if (!Array.isArray(transcript)) {
    return [];
  }

  return transcript
    .map((entry): TranscriptSegment | undefined => {
      if (!isRecord(entry)) {
        return undefined;
      }

      const text = entry.text ?? entry.words;
      if (typeof text !== "string" || text.trim().length === 0) {
        return undefined;
      }

      const speaker = entry.speaker ?? entry.speaker_name ?? entry.participant?.toString();

      return {
        speaker: typeof speaker === "string" ? speaker : undefined,
        text: text.trim(),
      };
    })
    .filter((entry): entry is TranscriptSegment => Boolean(entry));
};

export const extractRecordingUrl = (payload: RecallWebhookPayload): string | undefined => {
  const candidates = [
    payload.data?.recording_url,
    payload.data?.video_url,
    payload.data?.download_url,
    payload.recording_url,
  ];

  const value = candidates.find((candidate) => typeof candidate === "string");
  return typeof value === "string" ? value : undefined;
};

export const shouldFinalizeMeeting = (payload: RecallWebhookPayload): boolean => {
  const event = payload.event?.toLowerCase();
  return event === "transcript.done" || event === "bot.done" || event === "recording.done";
};
