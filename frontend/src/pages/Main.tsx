import React, { useState, useEffect, useRef } from "react";
import axios, { AxiosError, AxiosResponse } from "axios";
import styled from "styled-components";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import { Message, IMessage } from "../components/Message";

const ChatApp: React.FC = () => {
  const [messages, setMessages] = useState<IMessage[]>(defaultMessages);

  // Scroll to bottom part.
  const containerRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const container = containerRef.current;
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, [messages]);

  const handleResponse = (text: string, who: "bot" | "user") => {
    console.log(messages);
    setMessages((prev) => [...prev, { sender: who, text: text }]);
  };

  const handleStream = (text: string) => {
    if (messages[messages.length - 1].sender === "bot") {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          sender: "bot",
          text: text,
        },
      ]);
    } else {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: " ",
        },
      ]);
    }
  };

  return (
    <Background>
      <Container>
        <Header />
        <Window ref={containerRef}>
          {messages.map((message, i) => (
            <Message key={i} sender={message.sender}>
              {message.text}
            </Message>
          ))}
        </Window>
        <SearchBar
          handleMessages={handleResponse}
          handleStream={handleStream}
        />
      </Container>
    </Background>
  );
};

const defaultMessages: IMessage[] = [
  {
    sender: "bot",
    text:
      "무엇을 도와드릴까요? 당신에게 가장 적절한 복지 서비스를 찾아드려요! EX. 취업 예정인데 도와주세요!",
  },
  {
    sender: "user",
    text: "취업 예정인데 도와주세요!",
  },
  {
    sender: "bot",
    text:
      "취업을 위한 복지 서비스를 찾아드릴게요! \n - 실업 급여 \n - 국민연금 실업크레딧 \n - 건강보험 임의계속가입제도 \n - 국민취업지원제도 \n - 국민내일배움카드제 ",
  },
  {
    sender: "user",
    text: "국민내일배움카드제에 대해 알려주세요",
  },
  {
    sender: "bot",
    text: "무엇을 도와드릴까요?",
  },
];

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
