import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { useDispatch } from "react-redux";
import { handleResponse, handleStream } from "../redux/message.slice";

const SearchBar: React.FC = () => {
  const dispatch = useDispatch();
  const sendButton = `${process.env.PUBLIC_URL}/icon.svg`;

  const [input, setInput] = useState<string>("");

  const sendServerRequest = async () => {
    const response = await fetch("/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: input }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response;
  };

  const streamResponse = async (
    reader: ReadableStreamDefaultReader<Uint8Array>,
    decoder: TextDecoder
  ) => {
    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        dispatch(handleStream({ text: " ", loading: false }));
        break;
      }
      const text = decoder.decode(value);
      dispatch(handleStream({ text: text, loading: true }));
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      dispatch(handleResponse({ text: input, who: "user", loading: false }));
      setInput("");
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const response = await sendServerRequest();
      if (response.body) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        await streamResponse(reader, decoder);
      }
    } catch (error) {
      console.error("Error:", error);
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
  background-color: transparent;
  padding-left: 40px;
  &::placeholder {
    color: lightgray;
    font-size: 20px; /* Adjust the font size as needed */
    line-height: 1; /* Ensures vertical centering */
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
