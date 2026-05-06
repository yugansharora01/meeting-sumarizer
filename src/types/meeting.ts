export type TranscriptSegment = {
  speaker?: string;
  text: string;
  startTime?: string | number;
  endTime?: string | number;
};

export type MeetingStatus =
  | "bot_created"
  | "transcript_received"
  | "summary_sent"
  | "failed";

export type MeetingRecord = {
  botId: string;
  meetingUrl: string;
  email: string;
  status: MeetingStatus;
  transcript: TranscriptSegment[];
  summary?: string;
  recordingUrl?: string;
  createdAt: Date;
  updatedAt: Date;
  error?: string;
};

export type RecallBotResponse = {
  id?: string;
  bot_id?: string;
  status?: string;
  [key: string]: unknown;
};

export type RecallWebhookPayload = {
  event?: string;
  data?: Record<string, unknown>;
  bot?: {
    id?: string;
  };
  bot_id?: string;
  [key: string]: unknown;
};
