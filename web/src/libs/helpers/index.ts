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
