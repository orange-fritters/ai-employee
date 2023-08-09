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
import { dMessages } from "../../redux/defaultMessages";

/**
 * Guide message, initial recommendation, and branch according to response.
 *
 * @param input input at the beginning of the conversation, submitted to the SearchBar
 * @param state store state
 * @param dispatch useDispatch from react-redux
 *
 * @description
 * This function is used to process the initial phase of the multiturn recommendation.
 *   1. Add user input to the multiturn chat history
 *   2. Recieve recommendation from the backend
 *   3. Add recommendation to the recommendation state
 *   4. Recieve decision from the backend (whether the conversation is sufficient)
 *   5. Branch to either sufficient or insufficient response
 */
const processInitPhase = async (
  input: string,
  state: ReturnType<typeof store.getState>,
  dispatch: ReturnType<typeof useDispatch>
): Promise<void> => {
  const id = selectMultiturnID(state) + 1;
  dispatch(incrementId());
  dispatch(pushMultiturn({ content: input, role: "user", id: id }));

  const response = await requestRecommendation(input);
  const converted = await convertToJSON(response);
  dispatch(updateRecommendation({ recommendationResponse: converted }));

  const responseDecision = await requestMultiturnDecision();
  const convertedDecision: boolean = await convertToJSON(responseDecision);

  if (convertedDecision) {
    await handleSufficientResponse(id, dispatch);
  } else {
    await handleInsufficientResponse(id, dispatch);
  }
};

/**
 * Get and render the answer from the backend.
 *
 * @param id the multiturn id
 * @param dispatch useDispatch from react-redux
 * @param recommendation the recommendation array
 *
 * @description
 * 1. get the answer based on current conversation from the backend
 * 2. render answer to the web page
 * 3. update the multiturn state to done
 */
const handleSufficientResponse = async (
  id: number,
  dispatch: ReturnType<typeof useDispatch>,
  recommendation?: any
): Promise<void> => {
  const responseAnswer = await requestMultiturnAnswer();
  const convertedAnswer = await convertToJSON(responseAnswer);

  dispatch(pushMultiturn({ content: convertedAnswer, role: "bot", id: id }));
  dispatch(deleteLoading());
  dispatch(
    pushResponse({
      text: convertedAnswer,
      sender: "bot",
      loading: false,
      type: recommendation ? "response" : undefined,
      recArr: recommendation || undefined,
    })
  );
  dispatch(updateMultiturnState({ multiturnState: { phase: "done" } }));
};

/**
 * Get and render the question from the backend.
 *
 * @param id the multiturn id
 * @param dispatch useDispatch from react-redux
 *
 * @description
 * 1. get the question based on current conversation from the backend.
 * 2. render question to the web page
 * 3. update the multiturn state to insufficient
 */
const handleInsufficientResponse = async (
  id: number,
  dispatch: ReturnType<typeof useDispatch>
): Promise<void> => {
  const responseQuestion = await requestMultiturnQuestion();
  const convertedQuestion = await convertToJSON(responseQuestion);

  dispatch(pushMultiturn({ content: convertedQuestion, role: "bot", id: id }));
  dispatch(
    pushResponse({
      text: convertedQuestion,
      sender: "bot",
      loading: false,
    })
  );
  dispatch(deleteLoading());
  dispatch(updateMultiturnState({ multiturnState: { phase: "insufficient" } }));
};

/**
 * @param input input at the beginning of the conversation, submitted to the SearchBar
 * @param state store state
 * @param dispatch useDispatch from react-redux
 *
 * @description
 * 1. Add user input to the multiturn chat history
 * 2. Since, we asked a question, we get new recommendation based on the updated conversation
 * 3. Again, we get the decision from the backend (whether the conversation is sufficient)
 * 3. Branch to either sufficient or insufficient response
 */
const processInsufficientPhase = async (
  input: string,
  state: any,
  dispatch: ReturnType<typeof useDispatch>
): Promise<void> => {
  const id = selectMultiturnID(state);
  dispatch(pushMultiturn({ content: input, role: "user", id: id }));

  const response = await requestMultiturnRecommend();
  const converted = await convertToJSON(response);
  dispatch(updateRecommendation({ recommendationResponse: converted }));

  const responseDecision = await requestMultiturnDecision();
  const convertedDecision: boolean = await convertToJSON(responseDecision);

  if (convertedDecision) {
    await handleSufficientResponse(id, dispatch, converted);
  } else {
    await handleInsufficientResponse(id, dispatch);
  }
};

/**
 * Function handles afterward situation of the multiturn conversation.
 * @param input input at the beginning of the conversation, submitted to the SearchBar
 * @param state store state
 * @param dispatch useDispatch from react-redux
 *
 * @description
 * 1. User can now ask questions to the bot based on the specific document recommended.
 * 2. The bot will answer the question based on the document.
 */
const processDonePhase = async (
  input: string,
  state: any,
  dispatch: ReturnType<typeof useDispatch>
): Promise<void> => {
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
};

/**
 * Function handling the multiturn phase overall.
 *
 * @param input input submitted to the SearchBar
 * @param dispatch useDispatch from react-redux
 */
const handleMultiturn = async (
  input: string,
  dispatch: ReturnType<typeof useDispatch>
) => {
  const state = store.getState();
  const phase = selectMultiturnPhase(state);

  switch (phase) {
    case "init":
      await processInitPhase(input, state, dispatch);
      break;
    case "insufficient":
      await processInsufficientPhase(input, state, dispatch);
      break;
    default:
      await processDonePhase(input, state, dispatch);
      break;
  }
};

export { handleMultiturn };
