import {
  BooleanFilterType,
  NumericFilterType,
  StringFilterType,
} from "@libs/types";

export type FilterSet = Set<BooleanFilterType>;
export type FilterMap = Map<NumericFilterType, number>;
export type SearchMap = Map<StringFilterType, string>;
