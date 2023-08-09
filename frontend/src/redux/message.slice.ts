import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IRecElement } from "./recommendation.slice";
import { dMessages } from "./defaultMessages";
import { IMessage } from "../components/Message";

export const messageSlice = createSlice({
  name: "chat",
  initialState: {
    messages: dMessages,
  },
  reducers: {
    /**
     * initialize the message
     * @param state
     */
    initMessage: (state) => {
      state.messages = dMessages;
    },
    /**
     * Push the response message to the message list (state.messages)
     *
     * @param state
     * @param {PayloadAction<{text, sender, loading, type?, recArr?}>} action
     *
     * @description
     * A json object with the following keys should be passed as the payload:
     * - text: the text to be shown
     * - sender: "bot" or "user"
     * - loading: true or false (for the sync loading animation)
     * - type: "default" or "response"
     * - recArr: an array of IRecElement
     */
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

    /**
     * clear the loading animation
     */
    deleteLoading: (state) => {
      state.messages = state.messages.filter((elem) => !elem.loading);
    },

    /**
     * Handle word sent by FastAPI StreamResponse (word by word)
     * @param state
     * @param {PayloadAction<{text, loading}>} action
     *
     * @description
     * continuously add received word to the last message
     */
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
