import React, { useState } from "react";
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

const Message = ({ sender, text, type, loading, recArr }: IMessage) => {
  const dispatch = useDispatch();
  const first = useSelector(selectFirstTitle);
  const getCurrTime = () => {
    const date = new Date();
    const hour = date.getHours();
    const minutes = date.getMinutes();
    const formattedTime = `${hour < 10 ? "0" + hour : hour}:${
      minutes < 10 ? "0" + minutes : minutes
    }`;
    return formattedTime;
  };
  const handleRecClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
    const titleClicked = event.currentTarget.textContent;
    if (recArr && titleClicked) {
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

      // const response = await requestQuery(
      //   `${titleClicked}의 대상과 내용에 대해 쉬운 말로 세 문장 이내로 요약하시오.
      //   - 마침표 이후에는 \n을 사용하시오.
      //   - 오로지 요약문만 출력하시오.
      //   - 문의 방법은 절대 포함하지 마시오.
      //   - 존댓말을 사용하시오 (습니다. 입니다. ~입니다.)
      //   `,
      //   titleClicked
      // );
      // if (response.body) {
      //   const reader = response.body.getReader();
      //   const decoder = new TextDecoder("utf-8");
      //   await streamResponse(dispatch, reader, decoder);
      // }
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

  const handleRefClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
    // frontend/public/title_id.json
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

  switch (type) {
    case "time":
      return <S.TimeBox>{getCurrTime()}</S.TimeBox>;
    case "recommendation":
      return (
        <S.RecResponse>
          {recArr ? (
            recArr
              .slice(1)
              .map((rec) => (
                <S.Recommendation onClick={handleRecClick}>
                  {rec.title}
                </S.Recommendation>
              ))
          ) : (
            <S.SingleResponse sender={sender} type={type}>
              <S.MessageBox sender={sender} type={type}>
                추천할 서비스가 없습니다.
              </S.MessageBox>
            </S.SingleResponse>
          )}
        </S.RecResponse>
      );
    case "response":
      return (
        <S.SingleResponse sender={sender} type={type}>
          <S.MessageBox sender={sender} type={type}>
            {text.split("\n").map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
            {<S.FloatingButton onClick={handleRefClick}>문서</S.FloatingButton>}
          </S.MessageBox>
          {!loading && (
            <S.ButtonBox loading={loading} type={type}>
              <Button type="home" loading={loading} />
              <Button type="recommendation" loading={loading} />
            </S.ButtonBox>
          )}
        </S.SingleResponse>
      );
    case "initial":
      return (
        <S.SingleResponse sender={sender} type={type}>
          <S.MessageBox sender={sender} type={type}>
            {text.split("\n").map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
          </S.MessageBox>
          {!loading && (
            <S.InitButtonBox loading={loading} type={type}>
              <Button type="search" loading={loading} />
              <Button type="multiturn" loading={loading} />
            </S.InitButtonBox>
          )}
        </S.SingleResponse>
      );

    case "search":
      return (
        <S.SingleResponse sender={sender} type={type}>
          <S.MessageBox sender={sender} type={type}>
            {text.split("\n").map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
          </S.MessageBox>
          {!loading && (
            <S.SearchButtonBox loading={loading} type={type}>
              <Button type="home" loading={loading} />
            </S.SearchButtonBox>
          )}
        </S.SingleResponse>
      );

    default:
      return loading ? (
        <S.SingleResponse sender={sender} type={type}>
          <S.LoadingBox>
            <SyncLoader color="#A9A9A9" />
          </S.LoadingBox>
        </S.SingleResponse>
      ) : text ? (
        <S.SingleResponse sender={sender} type={type}>
          <S.MessageBox sender={sender} type={type}>
            {text.split("\n").map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
          </S.MessageBox>
        </S.SingleResponse>
      ) : (
        <></>
      );
  }
};

export default Message;
