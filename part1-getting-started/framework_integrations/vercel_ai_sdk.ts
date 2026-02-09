/**
 * Vercel AI SDK Integration with Helicone
 *
 * This example demonstrates:
 * - Using Helicone with Vercel AI SDK
 * - Streaming responses with observability
 * - Per-request header configuration
 * - Caching for improved performance
 *
 * Part of the Helicone tutorial series: https://zubairashfaque.github.io/
 */

import { createOpenAI } from "@ai-sdk/openai";
import { generateText, streamText } from "ai";

// Create OpenAI client with Helicone
const openai = createOpenAI({
  baseURL: "https://oai.helicone.ai/v1",
  headers: {
    "Helicone-Auth": `Bearer ${process.env.HELICONE_API_KEY}`,
    "Helicone-Cache-Enabled": "true", // Enable response caching
    "Helicone-Property-Framework": "vercel-ai-sdk",
  },
});

/**
 * Simple text generation with Helicone
 */
async function simpleGeneration() {
  console.log("Simple Text Generation with Helicone");
  console.log("=".repeat(60));
  console.log();

  const { text } = await generateText({
    model: openai("gpt-4o-mini"),
    prompt: "Explain the symptoms of Type 2 diabetes in 2 sentences.",
  });

  console.log("Response:", text);
  console.log();
  console.log("✅ Request logged to Helicone");
  console.log("   View at: https://helicone.ai/dashboard");
  console.log();
}

/**
 * Streaming response with Helicone
 */
async function streamingExample() {
  console.log("Streaming Response with Helicone");
  console.log("=".repeat(60));
  console.log();

  const result = await streamText({
    model: openai("gpt-4o-mini"),
    prompt: "List 5 common symptoms of hypertension.",
  });

  console.log("Streaming response:");

  // Stream the text chunks
  for await (const textPart of result.textStream) {
    process.stdout.write(textPart);
  }

  console.log("\n");
  console.log("✅ Streaming request logged to Helicone");
  console.log("   Time to First Token (TTFT) captured automatically");
  console.log();
}

/**
 * Medical chat assistant with user tracking
 */
async function medicalChatWithTracking() {
  console.log("Medical Chat with User Tracking");
  console.log("=".repeat(60));
  console.log();

  // Create client with per-user headers
  const userTrackedOpenAI = createOpenAI({
    baseURL: "https://oai.helicone.ai/v1",
    headers: {
      "Helicone-Auth": `Bearer ${process.env.HELICONE_API_KEY}`,
      "Helicone-User-Id": "patient-7829",
      "Helicone-Property-Department": "cardiology",
      "Helicone-Session-Id": "vercel-chat-001",
    },
  });

  const { text } = await generateText({
    model: userTrackedOpenAI("gpt-4o-mini"),
    prompt: "What lifestyle changes help manage high blood pressure?",
  });

  console.log("Response:", text);
  console.log();
  console.log("✅ Request logged with user tracking");
  console.log("   User ID: patient-7829");
  console.log("   Department: cardiology");
  console.log("   Session ID: vercel-chat-001");
  console.log();
  console.log("View per-user analytics in Helicone dashboard");
  console.log();
}

/**
 * Main function to run all examples
 */
async function main() {
  console.log("Vercel AI SDK + Helicone Examples");
  console.log("=".repeat(60));
  console.log();

  try {
    // Run examples
    await simpleGeneration();
    await streamingExample();
    await medicalChatWithTracking();

    console.log("=".repeat(60));
    console.log("✅ All examples completed!");
    console.log();
    console.log("Key Features Demonstrated:");
    console.log("  • Basic text generation with Helicone");
    console.log("  • Streaming responses with TTFT tracking");
    console.log("  • User tracking and custom properties");
    console.log("  • Session grouping for multi-turn conversations");
    console.log();
    console.log("View all requests at:");
    console.log("https://helicone.ai/dashboard");
    console.log();

  } catch (error) {
    console.error("❌ Error:", error.message);
    console.log();
    console.log("Make sure you have:");
    console.log("  • HELICONE_API_KEY set in .env");
    console.log("  • OPENAI_API_KEY configured in Helicone dashboard");
    process.exit(1);
  }
}

// Check for API key
if (!process.env.HELICONE_API_KEY) {
  console.error("❌ Error: HELICONE_API_KEY not found");
  console.log("Please create a .env file with your Helicone API key");
  process.exit(1);
}

// Run examples
main();
