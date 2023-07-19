import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface IRecState {
  now: "home" | "asking" | "recommendation";
}
export interface IRecElement {
  rank: number;
  title: string;
}

const RecList: IRecElement[] = [];
const RecState: IRecState = {
  now: "home",
};

export const recommendationSlice = createSlice({
  name: "recommendation",
  initialState: {
    recommendations: RecList,
    now: RecState,
  },
  reducers: {
    handleRecommendation: (
      state,
      action: PayloadAction<{
        recommendationResponse: IRecElement[];
      }>
    ) => {
      state.recommendations = action.payload.recommendationResponse;
      console.log(state.recommendations);
    },
    handleState: (
      state,
      action: PayloadAction<{
        recommendationState: IRecState;
      }>
    ) => {
      state.now = action.payload.recommendationState;
      console.log(state.now);
    },
  },
});

export const {
  handleRecommendation,
  handleState,
} = recommendationSlice.actions;
export default recommendationSlice.reducer;
