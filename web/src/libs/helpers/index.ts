import dayjs from "dayjs";

export function decodeUnicode(input: string) {
  const tempDiv = document.createElement("div");

  tempDiv.innerHTML = input;

  return tempDiv.textContent || tempDiv.innerText || "";
}

export function formatDuration(time_ms: number) {
  const minutes = Math.floor(time_ms / 60000);
  const seconds = ((time_ms % 60000) / 1000).toFixed(0);

  return `${minutes}:${parseInt(seconds) < 10 ? "0" : ""}${seconds}`;
}

export function translateDuration(duration_ms: number | string) {
  const ms = parseInt(duration_ms as string);
  const minutes = Math.floor(ms / 60000);
  const seconds = ((ms % 60000) / 1000).toFixed(0);

  return `${minutes}:${+seconds < 10 ? "0" : ""}${seconds}`;
}

/**
 * Human Readable format for the last played date
 *
 * Ex. 2024-10-18 16:47:26 CDT -> (assuming the current timezone is the same)
 * 2 days ago
 */
export function humanReadableDate(date: string) {
  const parsed = dayjs(date, "YYYY-MM-DD HH:mm:ss z");

  const now = dayjs();

  const diff = now.diff(parsed, "day");

  if (diff === 0) {
    return `Earlier Today`;
  } else if (diff === 1) {
    return `Yesterday`;
  }

  return `${diff} days ago`;
}

export function titleCase(str: string) {
  return str[0].toUpperCase() + str.slice(1);
}

export function formatHeader(header: string) {
  if (header === "duration_ms") {
    return "Duration (ms)";
  }

  if (header === "time_signature") {
    return "Time Signature";
  }

  if (header === "id") {
    return "ID";
  }

  return titleCase(header);
}
