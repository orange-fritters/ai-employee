import styled, { keyframes } from "styled-components";
import Button from "./Button";
import React from "react";

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
}

const Message = ({ sender, text, type, loading }: IMessage) => {
  if (type === "recommendation") {
    return (
      <SingleResponse sender={sender} type={type}>
        <MessageBox sender={sender} type={type}>
          <Button type="home" loading={loading} />
        </MessageBox>
      </SingleResponse>
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
  background-color: #7478b0;
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
