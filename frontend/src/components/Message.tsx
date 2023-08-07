import React from "react";
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
 * 1. default
 *  - any text "무엇을 도와드릴까요? 당신에게 가장 적절한 복지 서비스를 찾아드려요!"
 *  - No button
 *
 * 2. response
 *  - "서비스에 대한 요약 블라블라 "
 *  - html 포함
 *  - 버튼
 *   - 다른 제도 추천 받기 --> 클릭하면, 3.
 *   - 처음으로 돌아가기
 *
 * 3. recommendation
 *  - "3가지 제도를 추천해드려요! 더 알아보고 싶은 제도를 선택해주세요."
 *  - 버튼
 *   - 각 제도 바로가기 --> 클릭하면, 2
 *   - 처음으로 돌아가기
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

const TimeMessage = (props: IMessage) => {
  const getCurrTime = () => {
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

const RecommendationMessage = (props: IMessage) => {
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
          // text: `${titleClicked}은 어때요?`
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
