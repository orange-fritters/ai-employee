/**
 * Handles the click event for the Buttons.
 * @param {Function} dispatch - The dispatch function from the useDispatch hook to use Redux.
 * @returns {Promise<void>} - A Promise that resolves when the function is finished executing.
 */
import { useDispatch } from "react-redux";

import store from "../redux/store";
import { selectRecommendations } from "../redux/selectors";
import { pushResponse } from "../redux/message.slice";
import {
  updateRecommendation,
  updateRecommendationState,
  IRecElement,
} from "../redux/recommendation.slice";
import { dMessages, dSearch } from "../redux/defaultMessages";



/**
 * 1. Change the global recommendationState to "search".
 * 2. Push the default messages for searching to the chat history.
 */
const handleSearchButton = async (dispatch: ReturnType<typeof useDispatch>) => {
  dispatch(
    updateRecommendationState({ recommendationState: { now: "search" } })
  );
  dispatch(pushResponse({ ...dSearch[0] }));
  dispatch(pushResponse({ ...dSearch[1] }));
};

/**
 * 1. Change the global recommendationState to "recommendation".
 * 2. Push the default messages for announcing the recommendation to the chat history.
 * 3. If there are recommendations, **push recommendations as message** to the chat history too.
 */
const handleRecommendationButton = async (
  dispatch: ReturnType<typeof useDispatch>
) => {
  const state = store.getState();
  const recommendations: IRecElement[] = selectRecommendations(state);

  if (recommendations.length > 0) {
    dispatch(
      updateRecommendationState({
        recommendationState: { now: "recommendation" },
      })
    );
    dispatch(
      pushResponse({
        sender: "bot",
        text:
          "4가지 제도를 추가로 추천해드릴게요!\n더 알아보고 싶은 제도를 선택해주세요.",
        type: "default",
        loading: false,
      })
    );
    dispatch(
      pushResponse({
        sender: "bot",
        text: "",
        type: "recommendation",
        loading: false,
        recArr: recommendations,
      })
    );
  } else {
    dispatch(
      pushResponse({
        sender: "bot",
        text: "추천할 서비스가 없습니다. 처음으로 돌아가주세요",
        type: "response",
        loading: false,
      })
    );
  }
};

export {
  handleSearchButton,
  handleRecommendationButton
};
