import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface IMultiturn {
  text: string;
  sender: "bot" | "user";
  id: number;
}

const dMultiTurn: IMultiturn[] = [];

export const multiturnSlicer = createSlice({
  name: "multiturn",
  initialState: {
    multiturns: dMultiTurn,
    id: 0,
  },
  reducers: {
    pushMultiturn: (
      state,
      action: PayloadAction<{
        text: string;
        sender: "bot" | "user";
        id: number;
      }>
    ) => {
      state.multiturns = [
        ...state.multiturns,
        {
          sender: action.payload.sender,
          text: action.payload.text,
          id: action.payload.id,
        },
      ];
    },
    clearMultiturn: (state) => {
      state.multiturns = [];
    },
    incrementId: (state) => {
      state.id += 1;
    },
  },
});

export const {} = multiturnSlicer.actions;
export default multiturnSlicer.reducer;
