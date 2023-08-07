import {
  selectMultiturnHistory,
  selectRecommendations,
} from "../../../redux/selectors";
import store from "../../../redux/store";

const requestMultiturnRecommend = async () => {
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

const requestMultiturnDecision = async () => {
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

const requestMultiturnQuestion = async () => {
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

const requestMultiturnAnswer = async () => {
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
