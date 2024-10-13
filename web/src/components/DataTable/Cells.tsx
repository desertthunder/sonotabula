import { isBooleanObject, isNumberObject, isStringObject } from "util/types";

interface Props {
  value: string | number | boolean;
}

export function Cell({ value }: Props) {
  if (isBooleanObject(value)) {
    return null;
  } else if (isStringObject(value) || isNumberObject(value)) {
    return <p>{value}</p>;
  } else {
    return <p>{value}</p>;
  }
}
