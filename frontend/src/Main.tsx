import React, { useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import { RootState } from "./redux/store";

import * as S from "./components/styles/styles";

import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import Message from "./components/Message";

/**
 * ChatApp component that renders the chat window
 * Selects messages from the store and renders them
 * @returns ChatApp component
 */
const ChatApp: React.FC = () => {
  const messages = useSelector((state: RootState) => state.chat.messages);

  const containerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const container = containerRef.current;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, [messages]);

  return (
    <S.Background>
      <S.Container>
        <Header />
        <S.Window ref={containerRef}>
          {messages.map((message) => (
            <Message {...message} />
          ))}
        </S.Window>
        <SearchBar />
      </S.Container>
    </S.Background>
  );
};

export default ChatApp;
