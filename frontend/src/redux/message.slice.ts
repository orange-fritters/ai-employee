import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IMessage } from "../components/Message";
import { IRecElement } from "./recommendation.slicer";

export const dMessages: IMessage[] = [
  {
    sender: "bot",
    text: "무엇을 도와드릴까요? 당신에게 가장 적절한 복지 서비스를 찾아드려요!",
    type: "default",
    loading: false,
  },
  {
    sender: "bot",
    text:
      "EX. 저는 직장을 다니고 있어요, 그런데 아이 돌보기와 일상 생활을 균형잡기 힘들어요",
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
    handleResponse: (
      state,
      action: PayloadAction<{
        text: string;
        sender: "bot" | "user";
        loading: boolean;
        type?: "default" | "response" | "recommendation";
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
  handleResponse,
  handleStream,
} = messageSlice.actions;
export default messageSlice.reducer;
