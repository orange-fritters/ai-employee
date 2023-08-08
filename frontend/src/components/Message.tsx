/**
 * This file contains the implementation of different message types used in the chatbot.
 * Each message type has its own component that renders the message in a specific way.
 * The message types are:
 * - Default: normal message
 * - Response: response with buttons
 * - Recommendation: message containing recommendation list
 * - Initial: initial message @file frontend/src/redux/defaultMessages.ts
 * - Search: response of the search query
 * - Time: bar showing time
 *
 * @packageDocumentation
 */
import React, { ReactElement } from "react";
import { useSelector, useDispatch } from "react-redux";
import { SyncLoader } from "react-spinners";

import Button from "./Button";
import * as S from "./styles/styles";

import {
  IRecElement,
  updateRecommendationState,
  swapRank,
} from "../redux/recommendation.slice";
import { pushResponse } from "../redux/message.slice";
import { requestSummary } from "./utils/requests/requestSummary";
import { selectFirstTitle } from "../redux/selectors";

/** Message type
 *
 * default: normal message
 * response: response with buttons
 * recommendation: message containing recommendation list
 * initial: initial message @file frontend/src/redux/defaultMessages.ts
 * search: response of the search query
 * time: bar showing time
 */

export interface IMessage {
  sender: "user" | "bot";
  text: string;
  type:
    | "default"
    | "response"
    | "recommendation"
    | "initial"
    | "search"
    | "time";
  loading: boolean;
  multiturn?: boolean;
  recArr?: IRecElement[];
}

const splitText = (text: string) => {
  return text.split("\n").map((line, index) => (
    <span key={index}>
      {line}
      <br />
    </span>
  ));
};

/**
 * Displays the current time in the format "hh:mm".
 * @param props An object of type `IMessage` that contains the message data.
 * @returns A `ReactElement` that displays the current time.
 */
const TimeMessage = (props: IMessage): ReactElement => {
  const getCurrTime = (): string => {
    // Get time in hh:mm format
    const date = new Date();
    return `${date
      .getHours()
      .toString()
      .padStart(2, "0")}:${date
      .getMinutes()
      .toString()
      .padStart(2, "0")}`;
  };
  return <S.TimeBox>{getCurrTime()}</S.TimeBox>;
};

/**
 * Response message for the recommendation button click
 * @param props An object of type `IMessage` that contains the message data.
 * @returns A `ReactElement` that displays the recommended services.
 */
const RecommendationMessage = (props: IMessage): ReactElement => {
  const dispatch = useDispatch();

  const handleRecClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
    const titleClicked = event.currentTarget.textContent;
    if (props.recArr && titleClicked) {
      dispatch(
        pushResponse({
          sender: "user",
          loading: false,
          text: `${titleClicked}에 대해 더 자세하게 알려줘!`,
        })
      );
      dispatch(swapRank({ titleClicked }));
      const summary = await requestSummary(titleClicked);
      dispatch(
        pushResponse({
          sender: "bot",
          text: `${titleClicked}은 어때요?\n\n${summary}\n\n${titleClicked}에 대해 궁금한 점을 물어봐주세요! 대답해드릴게요!`,
          type: "default",
          loading: false,
        })
      );
    } else {
      dispatch(
        pushResponse({
          sender: "bot",
          loading: false,
          text: "가장 최근의 더보기를 눌러주세요!",
        })
      );
    }
    dispatch(
      updateRecommendationState({ recommendationState: { now: "asking" } })
    );
  };

  return (
    <S.RecResponse>
      {props.recArr ? (
        props.recArr
          .slice(1)
          .map((rec) => (
            <S.Recommendation onClick={handleRecClick}>
              {rec.title}
            </S.Recommendation>
          ))
      ) : (
        <S.SingleResponse sender={props.sender} type={"recommendation"}>
          <S.MessageBox sender={props.sender} type={"recommendation"}>
            추천할 서비스가 없습니다.
          </S.MessageBox>
        </S.SingleResponse>
      )}
    </S.RecResponse>
  );
};

const ResponseMessage = (props: IMessage) => {
  const dispatch = useDispatch();
  const first = useSelector(selectFirstTitle);

  const handleRefClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
    if (first) {
      const response = await fetch(`${process.env.PUBLIC_URL}/title_id.json`);
      const titleId = await response.json();
      const id = titleId[first];
      window.open(`/api/articles/view/${id}`, "_blank");
    } else {
      dispatch(
        pushResponse({
          sender: "bot",
          loading: false,
          text: "오류가 발생하였습니다!",
        })
      );
    }
  };

  return (
    <S.SingleResponse sender={props.sender} type={props.type}>
      <S.MessageBox sender={props.sender} type={props.type}>
        {splitText(props.text)}
        {<S.FloatingButton onClick={handleRefClick}>문서</S.FloatingButton>}
      </S.MessageBox>
      {!props.loading && (
        <S.ButtonBox loading={props.loading} type={props.type}>
          <Button type="home" loading={props.loading} />
          <Button type="recommendation" loading={props.loading} />
        </S.ButtonBox>
      )}
    </S.SingleResponse>
  );
};

const SearchMessage = (props: IMessage) => {
  return (
    <S.SingleResponse sender={props.sender} type={props.type}>
      <S.MessageBox sender={props.sender} type={props.type}>
        {splitText(props.text)}
      </S.MessageBox>
      {!props.loading && (
        <S.SearchButtonBox loading={props.loading} type={props.type}>
          <Button type="home" loading={props.loading} />
        </S.SearchButtonBox>
      )}
    </S.SingleResponse>
  );
};

const InitialMessage = (props: IMessage) => {
  return (
    <S.SingleResponse sender={props.sender} type={props.type}>
      <S.MessageBox sender={props.sender} type={props.type}>
        {splitText(props.text)}
      </S.MessageBox>
      {!props.loading && (
        <S.InitButtonBox loading={props.loading} type={props.type}>
          <Button type="search" loading={props.loading} />
          <Button type="multiturn" loading={props.loading} />
        </S.InitButtonBox>
      )}
    </S.SingleResponse>
  );
};

const DefaultMessage = (props: IMessage) => {
  return props.loading ? (
    <S.SingleResponse sender={props.sender} type={props.type}>
      <S.LoadingBox>
        <SyncLoader color="#A9A9A9" />
      </S.LoadingBox>
    </S.SingleResponse>
  ) : props.text ? (
    <S.SingleResponse sender={props.sender} type={props.type}>
      <S.MessageBox sender={props.sender} type={props.type}>
        {splitText(props.text)}
      </S.MessageBox>
    </S.SingleResponse>
  ) : (
    <></>
  );
};

const Message = (props: IMessage) => {
  const componentMapping = {
    time: TimeMessage,
    recommendation: RecommendationMessage,
    response: ResponseMessage,
    initial: InitialMessage,
    search: SearchMessage,
    default: DefaultMessage,
  };

  const Component = componentMapping[props.type] || componentMapping.default;
  return <Component {...props} />;
};

export default Message;
