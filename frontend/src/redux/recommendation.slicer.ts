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
    swapRank: (
      state,
      action: PayloadAction<{
        titleClicked: string;
      }>
    ) => {
      const { titleClicked } = action.payload;

      if (!titleClicked) {
        console.log("swapRank: invalid title");
        return;
      }

      const currFirstItem = state.recommendations.find(
        (elem) => elem.rank === 1
      );
      const clickedItem = state.recommendations.find(
        (elem) => elem.title === titleClicked
      );

      if (!currFirstItem || !clickedItem) {
        console.log("swapRank: invalid item");
        return;
      }

      const rankCandidate = clickedItem.rank;

      currFirstItem.rank = rankCandidate;
      clickedItem.rank = 1;

      state.recommendations.sort((a, b) => a.rank - b.rank);
      console.log("swapped successful", state.recommendations);
    },
  },
});

export const {
  handleRecommendation,
  handleState,
  swapRank,
} = recommendationSlice.actions;
export default recommendationSlice.reducer;
