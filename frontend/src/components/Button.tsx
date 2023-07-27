import React from "react";
import styled from "styled-components";
import { useDispatch, useSelector } from "react-redux";
import {
  handleRecommendation,
  handleState,
} from "../redux/recommendation.slicer";
import { dMessages, handleResponse } from "../redux/message.slice";
import { RootState } from "../redux/store";
import { requestMultiturn } from "./utils/requestMultiTurn";
import { streamResponse } from "./utils/streamResponse";

interface IButton {
  type: "home" | "recommendation" | "more";
  loading: boolean;
  text?: string;
}

const Button = ({ type, loading }: IButton) => {
  const dispatch = useDispatch();
  const recommendations = useSelector(
    (state: RootState) => state.recommendation.recommendations
  );

  const handleClick = async () => {
    switch (type) {
      case "home":
        dispatch(handleState({ recommendationState: { now: "home" } }));
        dispatch(handleResponse({ ...dMessages[0] }));
        dispatch(handleResponse({ ...dMessages[1] }));
        dispatch(handleRecommendation({ recommendationResponse: [] }));
        break;
      case "recommendation":
        if (recommendations.length > 0) {
          dispatch(
            handleState({ recommendationState: { now: "recommendation" } })
          );

          dispatch(
            handleResponse({
              sender: "bot",
              text:
                // "2가지 제도를 추가로 추천해드릴게요!\n더 알아보고 싶은 제도를 선택해주세요.",
                "4가지 제도를 추가로 추천해드릴게요!\n더 알아보고 싶은 제도를 선택해주세요.",
              type: "default",
              loading: false,
            })
          );
          dispatch(
            handleResponse({
              sender: "bot",
              text: "",
              type: "recommendation",
              loading: false,
              recArr: recommendations,
            })
          );
        } else {
          dispatch(
            handleResponse({
              sender: "bot",
              text: "추천할 서비스가 없습니다. 처음으로 돌아가주세요",
              type: "response",
              loading: false,
            })
          );
        }
        break;
      case "more":
        dispatch(handleState({ recommendationState: { now: "home" } }));
        await new Promise((resolve) => setTimeout(resolve, 1000));
        const response = await requestMultiturn("");
        if (response.body) {
          const reader = response.body.getReader();
          const decoder = new TextDecoder("utf-8");
          await streamResponse(dispatch, reader, decoder);
        }
        break;
    }
  };

  return (
    <StyledButton onClick={handleClick} type={type} loading={loading}>
      {type === "home" ? "처음" : type === "recommendation" ? "추천" : "문답"}
    </StyledButton>
  );
};

export default Button;

const StyledButton = styled.button<{
  type: "home" | "recommendation" | "more";
  loading: boolean;
}>`
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
  border-radius: 15px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  &:hover {
    background-color: #2162d1;
    color: rgb(255, 255, 255);
    cursor: pointer;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 2px 4px;
    font-weight: 600;
  }
  width: -webkit-fill-available;
`;
