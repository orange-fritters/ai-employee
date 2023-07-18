import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IMessage } from "../components/Message";

const IMessages: IMessage[] = [
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
    messages: IMessages,
  },
  reducers: {
    handleResponse: (
      state,
      action: PayloadAction<{
        text: string;
        who: "bot" | "user";
        loading: boolean;
      }>
    ) => {
      state.messages = [
        ...state.messages,
        {
          sender: action.payload.who,
          text: action.payload.text,
          type: "default",
          loading: action.payload.loading,
        },
      ];
      console.log(state.messages);
    },
    handleStream: (
      state,
      action: PayloadAction<{ text: string; loading: boolean }>
    ) => {
      const text = action.payload.text;
      if (
        state.messages.length > 0 &&
        state.messages[state.messages.length - 1].sender === "bot"
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
      console.log(state.messages);
    },
  },
});

export const { handleResponse, handleStream } = messageSlice.actions;
export default messageSlice.reducer;
