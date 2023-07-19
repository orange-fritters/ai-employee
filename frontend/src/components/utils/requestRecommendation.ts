import { useDispatch } from "react-redux";
import { handleRecommendation } from "../../redux/recommendation.slicer";
import { handleResponse } from "../../redux/message.slice";

export const requestRecommendation = async (input: string) => {
  const response = await fetch("/recommendation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: input }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};

export const getRecommendation = async (
  input: string,
  dispatch: ReturnType<typeof useDispatch>
) => {
  const response = await requestRecommendation(input);
  const data = await response.json();

  const converted = JSON.parse(data);
  const first = converted[0];
  console.log(converted);
  console.log(first);

  dispatch(handleRecommendation({ recommendationResponse: converted }));
  dispatch(
    handleResponse({
      sender: "bot",
      text: `${first.title}은 어때요? \n ${first.title}에 대해 물어봐주세요!`,
      type: "response",
      loading: false,
    })
  );
};
