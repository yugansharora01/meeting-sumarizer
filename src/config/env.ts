import dotenv from "dotenv";

dotenv.config();

const getNumber = (name: string, fallback: number): number => {
  const value = process.env[name];
  if (!value) {
    return fallback;
  }

  const parsed = Number(value);
  if (Number.isNaN(parsed)) {
    throw new Error(`${name} must be a number`);
  }

  return parsed;
};

const getBoolean = (name: string, fallback: boolean): boolean => {
  const value = process.env[name];
  if (!value) {
    return fallback;
  }

  return ["true", "1", "yes"].includes(value.toLowerCase());
};

export const env = {
  port: getNumber("PORT", 3000),
  publicBaseUrl: process.env.PUBLIC_BASE_URL ?? "http://localhost:3000",
  recall: {
    apiKey: process.env.RECALL_API_KEY ?? "",
    baseUrl: process.env.RECALL_API_BASE_URL ?? "https://api.recall.ai/api/v1",
  },
  openai: {
    apiKey: process.env.OPENAI_API_KEY ?? "",
    model: process.env.OPENAI_MODEL ?? "gpt-5.4-mini",
  },
  smtp: {
    host: process.env.SMTP_HOST ?? "",
    port: getNumber("SMTP_PORT", 587),
    secure: getBoolean("SMTP_SECURE", false),
    user: process.env.SMTP_USER ?? "",
    pass: process.env.SMTP_PASS ?? "",
    from: process.env.EMAIL_FROM ?? "Meeting Bot <no-reply@example.com>",
    attachRecording: getBoolean("EMAIL_ATTACH_RECORDING", false),
  },
};

export const requireEnv = (name: string, value: string): void => {
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
};
