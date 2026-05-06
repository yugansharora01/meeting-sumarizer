import axios from "axios";
import { env, requireEnv } from "../config/env";
import { RecallBotResponse } from "../types/meeting";

const recallClient = axios.create({
  baseURL: env.recall.baseUrl,
  timeout: 15_000,
});

recallClient.interceptors.request.use((config) => {
  requireEnv("RECALL_API_KEY", env.recall.apiKey);
  config.headers.Authorization = `Token ${env.recall.apiKey}`;
  config.headers["Content-Type"] = "application/json";
  return config;
});

export const createMeetingBot = async (meetingUrl: string): Promise<RecallBotResponse> => {
  const webhookUrl = `${env.publicBaseUrl.replace(/\/$/, "")}/webhook`;

  const { data } = await recallClient.post<RecallBotResponse>("/bot", {
    meeting_url: meetingUrl,
    recording_config: {
      transcript: {
        provider: {
          recallai_streaming: {
            language_code: "en",
          },
        },
        diarization: {
          use_separate_streams_when_available: true,
        },
      },
    },
    realtime_endpoints: [
      {
        type: "webhook",
        url: webhookUrl,
      },
    ],
  });

  return data;
};
