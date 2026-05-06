import { MeetingRecord, MeetingStatus, TranscriptSegment } from "../types/meeting";

const meetingsByBotId = new Map<string, MeetingRecord>();

export const saveMeeting = (record: Omit<MeetingRecord, "createdAt" | "updatedAt">): MeetingRecord => {
  const now = new Date();
  const meeting: MeetingRecord = {
    ...record,
    createdAt: now,
    updatedAt: now,
  };

  meetingsByBotId.set(meeting.botId, meeting);
  return meeting;
};

export const getMeeting = (botId: string): MeetingRecord | undefined => meetingsByBotId.get(botId);

export const updateMeeting = (
  botId: string,
  updates: Partial<Omit<MeetingRecord, "botId" | "createdAt">>,
): MeetingRecord | undefined => {
  const current = meetingsByBotId.get(botId);
  if (!current) {
    return undefined;
  }

  const updated: MeetingRecord = {
    ...current,
    ...updates,
    updatedAt: new Date(),
  };

  meetingsByBotId.set(botId, updated);
  return updated;
};

export const appendTranscript = (botId: string, segments: TranscriptSegment[]): MeetingRecord | undefined => {
  const current = meetingsByBotId.get(botId);
  if (!current) {
    return undefined;
  }

  return updateMeeting(botId, {
    transcript: [...current.transcript, ...segments],
    status: "transcript_received",
  });
};

export const markMeetingStatus = (
  botId: string,
  status: MeetingStatus,
  error?: string,
): MeetingRecord | undefined => updateMeeting(botId, { status, error });
