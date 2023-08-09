import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface IMultiturn {
  id: number;
  message: {
    role: "bot" | "user";
    content: string;
  };
}

interface IMultiState {
  phase: "init" | "insufficient" | "done";
}

const dMultiTurn: IMultiturn[] = [];
const dMultiState: IMultiState = {
  phase: "init",
};

export const multiturnSlicer = createSlice({
  name: "multiturn",
  initialState: {
    multiturns: dMultiTurn, // arrays containing the history of chats to send to the backend
    id: 0,
    phase: dMultiState,
  },
  reducers: {
    /** update state to either "init" | "insufficient" | "done" */
    updateMultiturnState: (
      state,
      action: PayloadAction<{
        multiturnState: IMultiState;
      }>
    ) => {
      state.phase = action.payload.multiturnState;
    },

    /** push a multiturn to the multiturns array */
    pushMultiturn: (
      state,
      action: PayloadAction<{
        content: string;
        role: "bot" | "user";
        id: number;
      }>
    ) => {
      state.multiturns = [
        ...state.multiturns,
        {
          id: action.payload.id,
          message: {
            role: action.payload.role,
            content: action.payload.content,
          },
        },
      ];
    },

    /** clear the multiturns array */
    clearMultiturn: (state) => {
      state.multiturns = [];
    },

    /** increment the id */
    incrementId: (state) => {
      state.id = state.id + 1;
      console.log("incremented id");
    },
  },
});

export const {
  updateMultiturnState,
  pushMultiturn,
  clearMultiturn,
  incrementId,
} = multiturnSlicer.actions;
export default multiturnSlicer.reducer;
