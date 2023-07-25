import React, { useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import { RootState } from "./redux/store";
import styled from "styled-components";

import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import Message from "./components/Message";
import { selectRecommendations } from "./redux/selectors";

const ChatApp: React.FC = () => {
  const messages = useSelector((state: RootState) => state.chat.messages);

  const containerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const container = containerRef.current;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, [messages]);

  const recommendations = useSelector(selectRecommendations);
  useEffect(() => {
    console.log(recommendations);
  }, [recommendations]);

  return (
    <Background>
      <Container>
        <Header />
        <Window ref={containerRef}>
          {messages.map((message) => (
            <Message
              sender={message.sender}
              text={message.text}
              type={message.type}
              loading={message.loading}
              recArr={message.recArr}
            />
          ))}
        </Window>
        <SearchBar />
      </Container>
    </Background>
  );
};

const Container = styled.div`
  width: 500px;
  height: 100vh;
`;

const Background = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  background-color: #d8d8d8;

  width: 100%;
  height: 100vh;

  ::-webkit-scrollbar {
    width: 10px;
    display: none;
  }
`;

const Window = styled.div`
  display: flex;
  flex-direction: column;
  background-color: white;

  width: 100%;
  height: 70vh;
  padding-top: 2.5vh;
  padding-bottom: 2.5vh;

  overflow-y: scroll;
  scroll-behavior: smooth;

  gap: 20px;
`;

export default ChatApp;
