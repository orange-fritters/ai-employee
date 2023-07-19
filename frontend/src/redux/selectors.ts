import { RootState } from "./store"; // Import your RootState

// Selectors for recommendationSlice
export const selectRecommendations = (state: RootState) =>
  state.recommendation.recommendations;

export const selectFirstRecommendation = (state: RootState) =>
  state.recommendation.recommendations.find((elem) => elem.rank === 1);

export const selectMessages = (state: RootState) => state.chat.messages;

export const selectNow = (state: RootState) => state.recommendation.now;

// from chat, find the most recent type default and sender user message
export const findQuery = (state: RootState) => {
  const reversedMessages = state.chat.messages.slice().reverse();
  const recentMessage = reversedMessages.find(
    (elem) => elem.type === "default" && elem.sender === "user"
  );

  return recentMessage ? recentMessage.text : undefined;
};
