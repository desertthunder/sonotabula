export function decodeUnicode(input: string) {
  const tempDiv = document.createElement("div");

  tempDiv.innerHTML = input;

  return tempDiv.textContent || tempDiv.innerText || "";
}
