import {
  selectMultiturnHistory,
  selectRecommendations,
} from "../../../redux/selectors";
import store from "../../../redux/store";

/**
 * @returns {Promise<Response>} - The response object from the backend.
 * @description
 * This function requests the backend for a initial recommendation based on the user's abstract input.
 */
const requestMultiturnRecommend = async (): Promise<Response> => {
  const state = store.getState();
  const titles = selectRecommendations(state);
  const history = selectMultiturnHistory(state);

  const response = await fetch("/api/multi-turn/recommendation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      titles: titles,
      history: history,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};

/**
 * @returns {Promise<Response>} - The response object from the backend.
 * @description
 * This function requests the backend to decide whether the recommendation is sufficient.
 */
const requestMultiturnDecision = async (): Promise<Response> => {
  const state = store.getState();
  const titles = selectRecommendations(state);
  const history = selectMultiturnHistory(state);

  const response = await fetch("/api/multi-turn/decide-sufficiency", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      titles: titles,
      history: history,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};

/**
 *
 * @returns {Promise<Response>} - The response object from the backend.
 * @description
 * This function requests the backend to ask a question to the user to improve the recommendation.
 */
const requestMultiturnQuestion = async (): Promise<Response> => {
  const state = store.getState();
  const titles = selectRecommendations(state);
  const history = selectMultiturnHistory(state);

  const response = await fetch("/api/multi-turn/question", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      titles: titles,
      history: history,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};

/**
 * @returns {Promise<Response>} - The response object from the backend.
 * @description
 * This function requests the backend the final answer for the consulting.
 */
const requestMultiturnAnswer = async (): Promise<Response> => {
  const state = store.getState();
  const titles = selectRecommendations(state);
  const history = selectMultiturnHistory(state);

  const response = await fetch("/api/multi-turn/answer", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      titles: titles,
      history: history,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};

export {
  requestMultiturnRecommend,
  requestMultiturnDecision,
  requestMultiturnQuestion,
  requestMultiturnAnswer,
};
