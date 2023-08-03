import { RootState } from "./store";

export const selectRecommendations = (state: RootState) =>
  state.recommendation.recommendations;

export const selectFirstRecommendation = (state: RootState) => {
  const firstRecommendation = state.recommendation.recommendations.find(
    (elem) => elem.rank === 1
  );
  return firstRecommendation || null; // Return null if no first recommendation found
};

export const selectFirstTitle = (state: RootState) => {
  const firstRecommendation = state.recommendation.recommendations.find(
    (elem) => elem.rank === 1
  );
  return firstRecommendation ? firstRecommendation.title : null; // Return null if no first recommendation found
};

export const selectLastMessage = (state: RootState) =>
  state.chat.messages[state.chat.messages.length - 1];

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

export const selectID = (state: RootState) => state.multiturn.id;

export const selectRecTitles = (state: RootState) => {
  const titles = state.recommendation.recommendations.map((elem) => elem.title);
  return titles ? titles : undefined;
};

export const selectUserMessages = (state: RootState) => {
  const userMessages = state.chat.messages.filter(
    (elem) => elem.sender === "user"
  );
  const context = userMessages.map((elem) => elem.text);
  return context ? context : undefined;
};
