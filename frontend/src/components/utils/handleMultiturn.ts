import { useDispatch } from "react-redux";
import {
  incrementId,
  pushMultiturn,
  updateMultiturnState,
} from "../../redux/multiturn.slice";
import store from "../../redux/store";
import {
  requestMultiturnAnswer,
  requestMultiturnDecision,
  requestMultiturnQuestion,
  requestMultiturnRecommend,
} from "./requests/requestMultiTurn";
import {
  dMessages,
  deleteLoading,
  initMessage,
  pushResponse,
} from "../../redux/message.slice";
import {
  updateRecommendation,
  updateRecommendationState,
} from "../../redux/recommendation.slice";
import { convertToJSON } from "./decoder";
import {
  selectFirstRecommendation,
  selectMultiturnID,
  selectMultiturnPhase,
} from "../../redux/selectors";
import { requestQuery } from "./requests/requestQuery";
import { streamResponse } from "./requests/streamResponse";
import { requestRecommendation } from "./requests/requestRecommendation";

export const handleMultiturn = async (
  input: string,
  dispatch: ReturnType<typeof useDispatch>
) => {
  const state = store.getState();
  const phase = selectMultiturnPhase(state);
  // "init" | "insufficient" | "done"
  if (phase === "init") {
    const id = selectMultiturnID(state) + 1;
    dispatch(incrementId());

    dispatch(pushMultiturn({ content: input, role: "user", id: id }));
    const response = await requestRecommendation(input);
    const converted = await convertToJSON(response);
    dispatch(updateRecommendation({ recommendationResponse: converted }));
    const responseDecision = await requestMultiturnDecision();
    const convertedDecision: boolean = await convertToJSON(responseDecision);
    if (convertedDecision) {
      // sufficient
      const responseAnswer = await requestMultiturnAnswer();
      const convertedAnswer = await convertToJSON(responseAnswer);
      dispatch(
        pushMultiturn({ content: convertedAnswer, role: "bot", id: id })
      );
      dispatch(
        pushResponse({
          text: convertedAnswer,
          sender: "bot",
          loading: false,
        })
      );
      dispatch(deleteLoading());
      dispatch(updateMultiturnState({ multiturnState: { phase: "done" } }));
    } else {
      // insufficient
      const id = selectMultiturnID(state);
      const responseQuestion = await requestMultiturnQuestion();
      const convertedQuestion = await convertToJSON(responseQuestion);
      dispatch(
        pushMultiturn({ content: convertedQuestion, role: "bot", id: id })
      );
      dispatch(
        pushResponse({
          text: convertedQuestion,
          sender: "bot",
          loading: false,
        })
      );
      dispatch(deleteLoading());
      dispatch(
        updateMultiturnState({ multiturnState: { phase: "insufficient" } })
      );
    }
  } else if (phase === "insufficient") {
    const id = selectMultiturnID(state);
    dispatch(pushMultiturn({ content: input, role: "user", id: id }));
    const response = await requestMultiturnRecommend();
    const converted = await convertToJSON(response);
    dispatch(updateRecommendation({ recommendationResponse: converted }));
    const responseDecision = await requestMultiturnDecision();
    const convertedDecision: boolean = await convertToJSON(responseDecision);
    if (convertedDecision) {
      // sufficient
      const responseAnswer = await requestMultiturnAnswer();
      const convertedAnswer = await convertToJSON(responseAnswer);
      dispatch(
        pushMultiturn({ content: convertedAnswer, role: "bot", id: id })
      );
      dispatch(deleteLoading());
      dispatch(
        pushResponse({
          text: convertedAnswer,
          sender: "bot",
          loading: false,
          type: "response",
          recArr: converted,
        })
      );
      dispatch(updateMultiturnState({ multiturnState: { phase: "done" } }));
    } else {
      // insufficient
      const responseQuestion = await requestMultiturnQuestion();
      const convertedQuestion = await convertToJSON(responseQuestion);
      dispatch(
        pushMultiturn({ content: convertedQuestion, role: "bot", id: id })
      );
      dispatch(
        pushResponse({
          text: convertedQuestion,
          sender: "bot",
          loading: false,
        })
      );
      dispatch(deleteLoading());
      dispatch(
        updateMultiturnState({ multiturnState: { phase: "insufficient" } })
      );
    }
  } else {
    // phase === "done"
    dispatch(
      updateRecommendationState({ recommendationState: { now: "asking" } })
    );
    try {
      const rec = selectFirstRecommendation(state);
      if (rec !== undefined && rec !== null) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        const response = await requestQuery(input, rec.title);
        if (response.body) {
          const reader = response.body.getReader();
          const decoder = new TextDecoder("utf-8");
          await streamResponse(dispatch, reader, decoder);
        }
      } else {
        dispatch(
          pushResponse({
            text: "오류가 발생하였습니다. 처음으로 돌아갑니다.",
            sender: "bot",
            loading: false,
          })
        );
        dispatch(
          updateRecommendationState({
            recommendationState: { now: "home" },
          })
        );
        dispatch(initMessage);
        dispatch(pushResponse({ ...dMessages[0] }));
        dispatch(pushResponse({ ...dMessages[1] }));
        dispatch(updateRecommendation({ recommendationResponse: [] }));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }
};
