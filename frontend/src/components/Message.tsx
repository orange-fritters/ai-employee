import styled, { keyframes } from "styled-components";
import Button from "./Button";
import React from "react";
import {
  IRecElement,
  handleState,
  swapRank,
} from "../redux/recommendation.slicer";
import { useDispatch, useSelector } from "react-redux";
import { requestQuery } from "./utils/requestQuery";
import { streamResponse } from "./utils/streamResponse";
import { handleResponse } from "../redux/message.slice";
import { requestSummary } from "./utils/requestSummary";

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
  type: "default" | "response" | "recommendation";
  loading: boolean;
  recArr?: IRecElement[];
}

const Message = ({ sender, text, type, loading, recArr }: IMessage) => {
  const dispatch = useDispatch();
  const handleRecClick = async (event: React.MouseEvent<HTMLButtonElement>) => {
    const titleClicked = event.currentTarget.textContent;
    if (recArr && titleClicked) {
      dispatch(
        handleResponse({
          sender: "user",
          loading: false,
          text: `${titleClicked}에 대해 더 자세하게 알려줘!`,
        })
      );
      dispatch(swapRank({ titleClicked }));

      const summary = await requestSummary(titleClicked);
      dispatch(
        handleResponse({
          sender: "bot",
          text: `${titleClicked}은 어때요?`,
          type: "default",
          loading: false,
        })
      );
      dispatch(
        handleResponse({
          sender: "bot",
          text: `${summary}`,
          type: "default",
          loading: false,
        })
      );
      dispatch(
        handleResponse({
          sender: "bot",
          text: `${titleClicked}에 대해 궁금한 점을 물어봐주세요! 대답해드릴게요!`,
          type: "response",
          loading: false,
        })
      );

      // const response = await requestQuery(
      //   `${titleClicked}에 대해 요약해줘.`,
      //   titleClicked
      // );
      // if (response.body) {
      //   const reader = response.body.getReader();
      //   const decoder = new TextDecoder("utf-8");
      //   await streamResponse(dispatch, reader, decoder);
      // }
    } else {
      dispatch(
        handleResponse({
          sender: "bot",
          loading: false,
          text: "가장 최근의 더보기를 눌러주세요!",
        })
      );
    }

    dispatch(handleState({ recommendationState: { now: "asking" } }));
  };

  if (type === "recommendation") {
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
  } else if (type === "response") {
    return (
      <SingleResponse sender={sender} type={type}>
        <MessageBox sender={sender} type={type}>
          {text}
        </MessageBox>
        {!loading && (
          <ButtonBox loading={loading} type={type}>
            <Button type="home" loading={loading} />
            <Button type="recommendation" loading={loading} />
          </ButtonBox>
        )}
      </SingleResponse>
    );
  } else {
    return (
      <SingleResponse sender={sender} type={type}>
        <MessageBox sender={sender} type={type}>
          {text}
        </MessageBox>
      </SingleResponse>
    );
  }
};

export default Message;

const MessageBox = styled.div<{
  sender: "user" | "bot";
  type: "default" | "response" | "recommendation";
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

const slideInFromLeft = keyframes`
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(0);
  }
`;

const ButtonBox = styled.div<{
  type: "default" | "response" | "recommendation";
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

const SingleResponse = styled.div<{
  type: "default" | "response" | "recommendation";
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
  grid-template-rows: 1fr 1fr 1fr 1fr;
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
