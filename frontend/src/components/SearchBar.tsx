import React, { useEffect, useState } from "react";
import styled from "styled-components";

interface ISearchBarProps {
  handleMessages: (query: string, who: "bot" | "user") => void;
  handleStream: (text: string) => void;
}

const SearchBar: React.FC<ISearchBarProps> = ({
  handleMessages,
  handleStream,
}) => {
  const PUBLIC_URL = process.env.PUBLIC_URL;
  const sendButton = `${PUBLIC_URL}/icon.svg`;

  const [input, setInput] = useState<string>("");
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState<string>("");

  useEffect(() => {
    if (response) {
      handleStream(response);
    }
  }, [response]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInput(event.target.value);
    setQuery(event.target.value);
  };

  const streamResponse = async (
    reader: ReadableStreamDefaultReader<Uint8Array>,
    decoder: TextDecoder
  ) => {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const text = decoder.decode(value);
      setResponse((prev) => prev + text);
    }
  };

  const sendServerRequest = async (query: string) => {
    const response = await fetch("/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response;
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      handleMessages(input, "user");
      setInput("");
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const response = await sendServerRequest(query);
      if (response.body) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        await streamResponse(reader, decoder);
      }
      setQuery("");
      setResponse("");
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
          onChange={handleInputChange}
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
