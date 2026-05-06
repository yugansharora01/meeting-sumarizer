import cors from "cors";
import express from "express";
import { env } from "./config/env";
import { meetingRouter } from "./routes/meeting.routes";
import { webhookRouter } from "./routes/webhook.routes";

const app = express();

app.use(cors());
app.use(express.json({ limit: "2mb" }));

app.get("/health", (_req, res) => {
  res.json({ success: true, message: "Meeting summarizer API is running" });
});

app.use(meetingRouter);
app.use(webhookRouter);

app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `Route not found: ${req.method} ${req.path}`,
  });
});

app.listen(env.port, () => {
  console.log(`Meeting summarizer API listening on port ${env.port}`);
});
