import React, { useState } from "react";
import styled from "styled-components";
import { useDispatch } from "react-redux";
import { initMessage, dMessages, handleResponse } from "../redux/message.slice";
import { requestQuery } from "./utils/requestQuery";
import { streamResponse } from "./utils/streamResponse";
import { useSelector } from "react-redux";
import { RootState } from "../redux/store";
import { getRecommendation } from "./utils/requestRecommendation";
import {
  handleRecommendation,
  handleState,
} from "../redux/recommendation.slicer";
import { selectFirstRecommendation } from "../redux/selectors";

const SearchBar: React.FC = () => {
  const dispatch = useDispatch();
  const [input, setInput] = useState<string>("");
  const state = useSelector((state: RootState) => state.recommendation.now);
  const rec = useSelector(selectFirstRecommendation);
  const sendButton = `${process.env.PUBLIC_URL}/icon.svg`;

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (state.now === "home") {
      getRecommendation(input, dispatch);
      dispatch(handleResponse({ text: input, sender: "user", loading: false }));
      setInput("");
      dispatch(handleState({ recommendationState: { now: "asking" } }));
    } else if (state.now == "asking") {
      try {
        dispatch(
          handleResponse({ text: input, sender: "user", loading: false })
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
            handleResponse({
              text: "오류가 발생하였습니다. 처음으로 돌아갑니다.",
              sender: "bot",
              loading: false,
            })
          );
          dispatch(handleState({ recommendationState: { now: "home" } }));
          dispatch(initMessage);
          dispatch(handleResponse({ ...dMessages[0] }));
          dispatch(handleResponse({ ...dMessages[1] }));
          dispatch(handleRecommendation({ recommendationResponse: [] }));
        }
      } catch (error) {
        console.error("Error:", error);
      }
    } else {
      dispatch(
        handleResponse({
          text: "원하시는 제도를 선택해주세요.",
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
