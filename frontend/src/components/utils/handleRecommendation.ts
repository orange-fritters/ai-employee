import { useDispatch } from "react-redux";
import { updateRecommendation } from "../../redux/recommendation.slice";
import { deleteLoading, pushResponse } from "../../redux/message.slice";
import { requestSummary } from "./requests/requestSummary";
import { requestRecommendation } from "./requests/requestRecommendation";
import { convertToJSON } from "./decoder";

const getRecommendation = async (
  input: string,
  dispatch: ReturnType<typeof useDispatch>
) => {
  const response = await requestRecommendation(input);
  const converted = await convertToJSON(response);
  dispatch(deleteLoading());
  const first = converted[0];
  dispatch(updateRecommendation({ recommendationResponse: converted }));
  const summary = await requestSummary(first.title);

  dispatch(
    pushResponse({
      sender: "bot",
      text: `${first.title}은 어때요?\n\n${summary}\n\n${first.title}에 대해 궁금한 점을 물어봐주세요! 대답해드릴게요!`,
      type: "response",
      loading: false,
    })
  );
};

const getRetrieval = async (
  input: string,
  dispatch: ReturnType<typeof useDispatch>
) => {
  const response = await requestRecommendation(input);
  const converted = await convertToJSON(response);
  dispatch(updateRecommendation({ recommendationResponse: converted }));
  const output = `${converted[0].title}
    ${converted[1].title}
    ${converted[2].title}
    ${converted[3].title}
    ${converted[4].title}
    를 찾았습니다!`;

  dispatch(
    pushResponse({
      sender: "bot",
      text: output,
      type: "default",
      loading: false,
    })
  );
  dispatch(deleteLoading());
  return converted;
};

export { getRecommendation, getRetrieval };
