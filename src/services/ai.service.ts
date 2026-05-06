import OpenAI from "openai";
import { env, requireEnv } from "../config/env";
import { TranscriptSegment } from "../types/meeting";

const formatTranscript = (segments: TranscriptSegment[]): string =>
  segments
    .map((segment) => {
      const speaker = segment.speaker?.trim() || "Unknown speaker";
      return `${speaker}: ${segment.text}`;
    })
    .join("\n");

export const generateMeetingSummary = async (segments: TranscriptSegment[]): Promise<string> => {
  requireEnv("OPENAI_API_KEY", env.openai.apiKey);

  const client = new OpenAI({
    apiKey: env.openai.apiKey,
  });

  const transcript = formatTranscript(segments);
  const response = await client.responses.create({
    model: env.openai.model,
    input: [
      {
        role: "system",
        content:
          "You are a precise meeting assistant. Produce clear summaries with decisions, action items, discussion points, and blockers.",
      },
      {
        role: "user",
        content: `Summarize this meeting into:

1. Key decisions
2. Action items with owners
3. Important discussion points
4. Risks or blockers

Transcript:
${transcript}`,
      },
    ],
  });

  return response.output_text;
};
