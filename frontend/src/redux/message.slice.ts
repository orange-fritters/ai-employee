import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IMessage } from "../components/Message";
import { IRecElement } from "./recommendation.slice";

export const dMessages: IMessage[] = [
  {
    sender: "bot",
    text: "",
    type: "time",
    loading: false,
  },
  {
    sender: "bot",
    text:
      "안녕하세요!\n저는 여러분의 복지 서비스를 도와드릴 AI 봇입니다. 원하시는 서비스를 선택해주세요.",
    type: "initial",
    loading: false,
  },
];

export const dSearch: IMessage[] = [
  {
    sender: "bot",
    text: "",
    type: "time",
    loading: false,
  },
  {
    sender: "bot",
    text:
      "복지 서비스에 대한 정보를 찾아드려요!\n원하시는 서비스에 대해 무엇이든 물어보세요.",
    type: "default",
    loading: false,
  },
];

export const dMultiturn: IMessage[] = [
  {
    sender: "bot",
    text:
      "당신의 상황에 알맞은 복지 서비스를 찾아줄게요!\n\nEX. 취직 준비에 도움을 받고 싶어요.",
    type: "default",
    loading: false,
  },
];

export const messageSlice = createSlice({
  name: "chat",
  initialState: {
    messages: dMessages,
  },
  reducers: {
    initMessage: (state, action: PayloadAction) => {
      state.messages = dMessages;
    },
    pushResponse: (
      state,
      action: PayloadAction<{
        text: string;
        sender: "bot" | "user";
        loading: boolean;
        type?: IMessage["type"];
        recArr?: IRecElement[];
      }>
    ) => {
      state.messages = [
        ...state.messages,
        {
          sender: action.payload.sender,
          text: action.payload.text,
          type: action.payload.type || "default",
          loading: action.payload.loading,
          recArr: action.payload.recArr || [],
        },
      ];
    },
    deleteLoading: (state) => {
      state.messages = state.messages.filter((elem) => !elem.loading);
    },
    handleStream: (
      state,
      action: PayloadAction<{ text: string; loading: boolean }>
    ) => {
      const text = action.payload.text;
      if (
        state.messages.length > 0 &&
        state.messages[state.messages.length - 1].sender === "bot" &&
        state.messages[state.messages.length - 1].type === "response"
      ) {
        state.messages[state.messages.length - 1].text += text;
        state.messages[state.messages.length - 1].loading =
          action.payload.loading;
      } else {
        state.messages.push({
          sender: "bot",
          text: text,
          type: "response",
          loading: action.payload.loading,
        });
      }
    },
  },
});

export const {
  initMessage,
  pushResponse,
  handleStream,
  deleteLoading,
} = messageSlice.actions;
export default messageSlice.reducer;
