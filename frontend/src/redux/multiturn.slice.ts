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
    multiturns: dMultiTurn,
    id: 0,
    phase: dMultiState,
  },
  reducers: {
    updateMultiturnState: (
      state,
      action: PayloadAction<{
        multiturnState: IMultiState;
      }>
    ) => {
      state.phase = action.payload.multiturnState;
    },
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
    clearMultiturn: (state) => {
      state.multiturns = [];
    },
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
