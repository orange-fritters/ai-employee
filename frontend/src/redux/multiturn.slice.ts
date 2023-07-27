import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export const multiturnSlicer = createSlice({
  name: "multiturn",
  initialState: {
    multiturns: [],
  },
  reducers: {
    handlemultiturn: (state, action: PayloadAction) => {
      console.log(state.multiturns);
    },
    clearMultiturn: (state) => {
      state.multiturns = [];
    },
  },
});

export const {} = multiturnSlicer.actions;
export default multiturnSlicer.reducer;
