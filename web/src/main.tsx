import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "@fontsource-variable/inter";
import "@fontsource-variable/karla";
import "@fontsource-variable/dm-sans";
import "./styles/base.css";

export function main() {
  const root = document.getElementById("root");

  if (!root) {
    throw new Error("Root element not found");
  }

  ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}

main();
