import nodemailer from "nodemailer";
import { env, requireEnv } from "../config/env";

type SendMeetingSummaryEmailInput = {
  to: string;
  summary: string;
  recordingUrl?: string;
};

const createTransport = () => {
  requireEnv("SMTP_HOST", env.smtp.host);
  requireEnv("SMTP_USER", env.smtp.user);
  requireEnv("SMTP_PASS", env.smtp.pass);

  return nodemailer.createTransport({
    host: env.smtp.host,
    port: env.smtp.port,
    secure: env.smtp.secure,
    auth: {
      user: env.smtp.user,
      pass: env.smtp.pass,
    },
  });
};

export const sendMeetingSummaryEmail = async ({
  to,
  summary,
  recordingUrl,
}: SendMeetingSummaryEmailInput): Promise<void> => {
  const transporter = createTransport();
  const recordingText = recordingUrl ? `\n\nRecording:\n${recordingUrl}` : "";
  const attachments =
    env.smtp.attachRecording && recordingUrl
      ? [
          {
            filename: "meeting-recording.mp4",
            path: recordingUrl,
          },
        ]
      : undefined;

  await transporter.sendMail({
    from: env.smtp.from,
    to,
    subject: "Meeting Summary",
    text: `${summary}${recordingText}`,
    attachments,
  });
};
