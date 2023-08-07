import { useDispatch, useSelector } from "react-redux";

import { deleteLoading, pushResponse } from "../../redux/message.slice";
import {
  updateRecommendation,
  updateRecommendationState,
  IRecElement,
} from "../../redux/recommendation.slice";
import { dMessages, dMultiturn, dSearch } from "../../redux/defaultMessages";
import { updateMultiturnState } from "../../redux/multiturn.slice";

const handleHomeButton = async (dispatch: ReturnType<typeof useDispatch>) => {
  dispatch(
    updateRecommendationState({ recommendationState: { now: "search" } })
  );
  dispatch(pushResponse({ ...dMessages[0] }));
  dispatch(pushResponse({ ...dMessages[1] }));
  dispatch(updateRecommendation({ recommendationResponse: [] }));
};

const handleSearchButton = async (dispatch: ReturnType<typeof useDispatch>) => {
  dispatch(
    updateRecommendationState({ recommendationState: { now: "search" } })
  );
  dispatch(pushResponse({ ...dSearch[0] }));
  dispatch(pushResponse({ ...dSearch[1] }));
};

const handleRecommendationButton = async (
  recommendations: IRecElement[],
  dispatch: ReturnType<typeof useDispatch>
) => {
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

const handleMultiturnButton = async (
  dispatch: ReturnType<typeof useDispatch>
) => {
  dispatch(
    updateRecommendationState({
      recommendationState: { now: "multiturn" },
    })
  );
  dispatch(updateMultiturnState({ multiturnState: { phase: "init" } }));
  dispatch(
    pushResponse({
      text: "",
      sender: "bot",
      loading: true,
      type: "default",
    })
  );

  await new Promise((resolve) => setTimeout(resolve, 500));
  dispatch(deleteLoading());
  dispatch(pushResponse({ ...dMultiturn[0] }));

  // await new Promise((resolve) => setTimeout(resolve, 1000));
  // const response = await requestMultiturn("");
  // if (response.body) {
  //   const reader = response.body.getReader();
  //   const decoder = new TextDecoder("utf-8");
  //   await streamResponse(dispatch, reader, decoder);
  // }
};

export {
  handleHomeButton,
  handleSearchButton,
  handleRecommendationButton,
  handleMultiturnButton,
};
