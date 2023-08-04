import styled, { keyframes } from "styled-components";
import Button from "./Button";
import React, { useState } from "react";
import {
  IRecElement,
  updateRecommendationState,
  swapRank,
} from "../redux/recommendation.slice";
import { useDispatch } from "react-redux";
import { pushResponse } from "../redux/message.slice";
import { requestSummary } from "./utils/requests/requestSummary";
import { useSelector } from "react-redux";
import { selectFirstTitle } from "../redux/selectors";
import { SyncLoader } from "react-spinners";

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
      return <TimeBox>{getCurrTime()}</TimeBox>;
    case "recommendation":
      return (
        <RecResponse>
          {recArr ? (
            recArr
              .slice(1)
              .map((rec) => (
                <Recommendation onClick={handleRecClick}>
                  {rec.title}
                </Recommendation>
              ))
          ) : (
            <SingleResponse sender={sender} type={type}>
              <MessageBox sender={sender} type={type}>
                추천할 서비스가 없습니다.
              </MessageBox>
            </SingleResponse>
          )}
        </RecResponse>
      );
    case "response":
      return (
        <SingleResponse sender={sender} type={type}>
          <MessageBox sender={sender} type={type}>
            {text.split("\n").map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
            {<FloatingButton onClick={handleRefClick}>문서</FloatingButton>}
          </MessageBox>
          {!loading && (
            <ButtonBox loading={loading} type={type}>
              <Button type="home" loading={loading} />
              <Button type="recommendation" loading={loading} />
            </ButtonBox>
          )}
        </SingleResponse>
      );
    case "initial":
      return (
        <SingleResponse sender={sender} type={type}>
          <MessageBox sender={sender} type={type}>
            {text.split("\n").map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
          </MessageBox>
          {!loading && (
            <InitButtonBox loading={loading} type={type}>
              <Button type="search" loading={loading} />
              <Button type="multiturn" loading={loading} />
            </InitButtonBox>
          )}
        </SingleResponse>
      );

    case "search":
      return (
        <SingleResponse sender={sender} type={type}>
          <MessageBox sender={sender} type={type}>
            {text.split("\n").map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
          </MessageBox>
          {!loading && (
            <SearchButtonBox loading={loading} type={type}>
              <Button type="home" loading={loading} />
            </SearchButtonBox>
          )}
        </SingleResponse>
      );

    default:
      return loading ? (
        <SingleResponse sender={sender} type={type}>
          <LoadingBox>
            <SyncLoader color="#A9A9A9" />
          </LoadingBox>
        </SingleResponse>
      ) : text ? (
        <SingleResponse sender={sender} type={type}>
          <MessageBox sender={sender} type={type}>
            {text.split("\n").map((line, index) => (
              <span key={index}>
                {line}
                <br />
              </span>
            ))}
          </MessageBox>
        </SingleResponse>
      ) : (
        <></>
      );
  }
};

export default Message;

const TimeBox = styled.div`
  display: grid;

  justify-self: center;
  justify-content: center;
  align-items: center;
  align-self: center;

  height: 25px;
  width: 30%;
  margin-bottom: 10px;
  font-family: "Noto Sans KR", sans-serif;
  font-weight: 600;

  border-radius: 15px;
  background-color: white;
  box-shadow: 0 0 5px 2.5px rgba(0, 0, 0, 0.1);
`;

const MessageBox = styled.div<{
  sender: "user" | "bot";
  type: IMessage["type"];
}>`
  display: grid;
  grid-column: 1 / 3;
  position: relative;
  text-align: ${(props) => (props.sender === "bot" ? "left" : "right")};
  background-color: ${(props) =>
    props.sender === "bot" ? "#eeeeee" : "#0084ff"};
  color: ${(props) => (props.sender === "bot" ? "#000" : "#fff")};
  padding: 20px;
  border-radius: ${(props) =>
    props.sender === "bot" ? "0px 30px 30px 30px" : "30px 0px 30px 30px"};
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
`;

const LoadingBox = styled.div`
  display: flex;
  position: relative;
  justify-content: center;
  align-items: center;
  background-color: #eeeeee;
  color: #000;
  padding: 20px;
  border-radius: 0px 30px 30px 30px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  width: 100%;
`;

const slideInFromLeft = keyframes`
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(0);
  }
`;

const ButtonBox = styled.div<{
  type: IMessage["type"];
  loading: boolean;
}>`
  grid-column: 1 / 3;
  display: grid;
  grid-template-columns: 1fr 1fr;
  justify-items: center;
  position: relative;
  align-self: "flex-start";
  text-align: "left";
  background-color: #648fd9;
  color: "#000";
  max-width: ${(props) => (props.type === "default" ? "60%" : "100%")};
  margin-left: ${(props) => (props.type === "default" ? "25px" : "0px")};
  margin-right: 0px;
  padding: 5px;
  border-radius: 5px 17px 17px 17px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);

  height: ${(props) => (props.loading ? "0px" : "50px")};
  transition: height 1s ease-in-out;
  animation: ${slideInFromLeft} 1s ease-out;

  column-gap: 10px;
  padding: 10px;
`;

const InitButtonBox = styled(ButtonBox)`
  grid-template-columns: 1fr 1fr;
`;

const SearchButtonBox = styled(ButtonBox)`
  grid-template-columns: 1fr;
`;

const SingleResponse = styled.div<{
  type: IMessage["type"];
  sender: "user" | "bot";
}>`
  display: grid;
  max-width: 60%;
  grid-template-columns: ${(props) =>
    props.type === "default" ? "1fr" : "1fr 1fr"};
  margin-left: ${(props) => (props.sender === "bot" ? "25px" : "0px")};
  margin-right: ${(props) => (props.sender === "bot" ? "0px" : "25px")};
  align-self: ${(props) =>
    props.sender === "bot" ? "flex-start" : "flex-end"};
  grid-template-rows: auto;
  grid-column-gap: 12px;
  grid-row-gap: 15px;
  margin-left: 25px;
`;

const RecResponse = styled.div`
  display: grid;
  // grid-template-rows: 1fr 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  width: 55%;
  margin-left: 25px;
  margin-right: 0px;
  align-self: flex-start;
  grid-row-gap: 12px;
  padding: 2.5%;

  justify-items: center;
  position: relative;
  background-color: rgb(100, 143, 217);
  border-radius: 5px 17px 17px;
  box-shadow: rgba(0, 0, 0, 0.2) 0px 2px 4px;
  transition: height 1s ease-in-out 0s;
  animation: 1s ease-out 0s 1 normal none running bxdTFl;
`;

const Recommendation = styled.button`
  position: relative;
  align-self: "flex-start";
  text-align: "center";
  background-color: #6e9ef0;
  color: white;
  border: none;
  font-weight: 550;
  font-size: 16px;
  padding-top: 6.5px;
  padding-bottom: 6.5px;
  border-radius: 5px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  &:hover {
    background-color: #2162d1;
    color: rgb(255, 255, 255);
    cursor: pointer;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 2px 4px;
    font-weight: 600;
  }
  width: 100%;
`;

const popIn = keyframes`
  0% {
    transform: scale(0);
    opacity: 0;
  }
  80% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
  }
`;

const FloatingButton = styled.button`
  position: absolute;
  top: 0px;
  right: -50px;
  box-shadow: 0px 1.5px 3px rgba(0, 0, 0, 0.16),
    0px 1.5px 3px rgba(0, 0, 0, 0.23);
  background: #6a5acd;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;

  &:hover {
    background: #0073e6;
  }

  animation: ${popIn} 0.5s ease;
  animation-delay: 1s;
  animation-fill-mode: backwards;
`;
