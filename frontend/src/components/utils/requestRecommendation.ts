import { useDispatch } from "react-redux";
import { handleRecommendation } from "../../redux/recommendation.slice";
import { deleteLoading, handleResponse } from "../../redux/message.slice";
import { requestSummary } from "./requestSummary";

export const requestRecommendation = async (input: string) => {
  const response = await fetch("/api/recommendation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: input }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  const converted = JSON.parse(data);
  return converted;
};

export const getRecommendation = async (
  input: string,
  dispatch: ReturnType<typeof useDispatch>
) => {
  const converted = await requestRecommendation(input);
  dispatch(deleteLoading());
  const first = converted[0];
  dispatch(handleRecommendation({ recommendationResponse: converted }));
  const summary = await requestSummary(first.title);

  dispatch(
    handleResponse({
      sender: "bot",
      text: `${first.title}은 어때요?\n\n${summary}\n\n${first.title}에 대해 궁금한 점을 물어봐주세요! 대답해드릴게요!`,
      type: "response",
      loading: false,
    })
  );
};

export const getRetrieval = async (
  input: string,
  dispatch: ReturnType<typeof useDispatch>
) => {
  const converted = await requestRecommendation(input);
  dispatch(handleRecommendation({ recommendationResponse: converted }));
  const output = `${converted[0].title}
  ${converted[1].title}
  ${converted[2].title}
  ${converted[3].title}
  ${converted[4].title}
  를 찾았습니다!`;
  dispatch(
    handleResponse({
      sender: "bot",
      text: output,
      type: "default",
      loading: false,
    })
  );
  dispatch(deleteLoading());
  return converted;
};
