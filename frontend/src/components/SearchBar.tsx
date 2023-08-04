import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../redux/store";
import styled from "styled-components";

import { requestQuery } from "./utils/requests/requestQuery";
import { streamResponse } from "./utils/requests/streamResponse";
import { requestSearch } from "./utils/requests/requestSearch";
import { getRecommendation, getRetrieval } from "./utils/handleRecommendation";

import {
  updateRecommendation,
  updateRecommendationState,
} from "../redux/recommendation.slice";
import { initMessage, dMessages, pushResponse } from "../redux/message.slice";
import {
  selectFirstRecommendation,
  selectMultiturnPhase,
} from "../redux/selectors";
import { handleMultiturn } from "./utils/handleMultiturn";

const SearchBar: React.FC = () => {
  const dispatch = useDispatch();
  const [input, setInput] = useState<string>("");
  const state = useSelector((state: RootState) => state.recommendation.now);
  const rec = useSelector(selectFirstRecommendation);
  const sendButton = `${process.env.PUBLIC_URL}/icon.svg`;

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    switch (state.now) {
      case "home":
        getRecommendation(input, dispatch);
        dispatch(pushResponse({ text: input, sender: "user", loading: false }));
        setInput("");
        dispatch(
          pushResponse({
            text: "",
            sender: "bot",
            loading: true,
            type: "default",
          })
        );
        dispatch(
          updateRecommendationState({ recommendationState: { now: "asking" } })
        );
        break;

      case "search":
        const query = input;
        setInput("");
        dispatch(pushResponse({ text: query, sender: "user", loading: false }));
        dispatch(
          pushResponse({
            text: "",
            sender: "bot",
            loading: true,
            type: "default",
          })
        );
        const titles = await getRetrieval(query, dispatch);
        try {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          const response = await requestSearch(input, titles);
          if (response.body) {
            dispatch(pushResponse({ text: "", sender: "bot", loading: false }));
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            await streamResponse(dispatch, reader, decoder);
          }
        } catch (error) {
          dispatch(
            pushResponse({
              text: "오류가 발생하였습니다. 처음으로 돌아갑니다.",
              sender: "bot",
              loading: false,
            })
          );
        }

        dispatch(
          updateRecommendationState({ recommendationState: { now: "asking" } })
        );
        break;

      case "asking":
        try {
          dispatch(
            pushResponse({ text: input, sender: "user", loading: false })
          );
          setInput("");
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
            dispatch(pushResponse({ ...dMessages[0] }));
            dispatch(pushResponse({ ...dMessages[1] }));
            dispatch(updateRecommendation({ recommendationResponse: [] }));
          }
        } catch (error) {
          console.error("Error:", error);
        }
        break;

      case "multiturn":
        const question = input;
        setInput("");
        handleMultiturn(question, dispatch);
        dispatch(
          pushResponse({ text: question, sender: "user", loading: false })
        );
        dispatch(
          pushResponse({
            text: "",
            sender: "bot",
            loading: true,
            type: "default",
          })
        );
        break;

      default:
        dispatch(
          pushResponse({
            text: "새로고침해주세요.",
            sender: "bot",
            loading: false,
          })
        );
    }
  };

  return (
    <BackGround onSubmit={handleSubmit}>
      <SearchBarBox>
        <SearchInput
          placeholder="   질문을 입력해주세요."
          type="text"
          value={input}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setInput(e.target.value)
          }
        />
        <SmallSendButton type="submit">
          <img src={sendButton} />
        </SmallSendButton>
      </SearchBarBox>
    </BackGround>
  );
};

export default SearchBar;

const BackGround = styled.form`
  background-color: white;
  width: 100%;
  height: 15vh;

  display: flex;
  align-items: center;
  justify-content: center;
`;

const SearchBarBox = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;

  background-color: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);

  width: 80%;
  height: 90%;

  border-radius: 25px;

  color: black;
`;

const SearchInput = styled.input`
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  height: 20px;
  background-color: transparent;
  padding-left: 40px;
  &::placeholder {
    color: lightgray;
    font-size: 20px;
    line-height: 1;
  }
`;

const SmallSendButton = styled.button`
  background-color: transparent;
  border: none;

  img {
    width: 50px;
    height: 50px;
    background-size: cover;
    cursor: pointer;
    border: none;
    margin-right: 10px;
  }
`;
