import React from "react";
import styled from "styled-components";
import { useDispatch, useSelector } from "react-redux";
import {
  handleRecommendation,
  handleState,
} from "../redux/recommendation.slice";
import { dMessages, dSearch, handleResponse } from "../redux/message.slice";
import { RootState } from "../redux/store";

interface IButton {
  type: "home" | "recommendation" | "multiturn" | "search";
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
        dispatch(handleState({ recommendationState: { now: "search" } }));
        dispatch(handleResponse({ ...dMessages[0] }));
        dispatch(handleResponse({ ...dMessages[1] }));
        dispatch(handleRecommendation({ recommendationResponse: [] }));
        break;
      case "search":
        dispatch(handleState({ recommendationState: { now: "search" } }));
        dispatch(handleResponse({ ...dSearch[0] }));
        dispatch(handleResponse({ ...dSearch[1] }));
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
      case "multiturn":
        dispatch(handleState({ recommendationState: { now: "multiturn" } }));
        // await new Promise((resolve) => setTimeout(resolve, 1000));
        // const response = await requestMultiturn("");
        // if (response.body) {
        //   const reader = response.body.getReader();
        //   const decoder = new TextDecoder("utf-8");
        //   await streamResponse(dispatch, reader, decoder);
        // }
        console.log("multiturn");
        break;
    }
  };

  const getText = () => {
    switch (type) {
      case "home":
        return "처음";
      case "recommendation":
        return "추천";
      case "multiturn":
        return "추천받기";
      case "search":
        return "문의하기";
      default:
        return "";
    }
  };

  return (
    <StyledButton onClick={handleClick} type={type} loading={loading}>
      {getText()}
    </StyledButton>
  );
};

export default Button;

const StyledButton = styled.button<{
  type: IButton["type"];
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
