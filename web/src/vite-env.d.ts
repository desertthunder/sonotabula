/// <reference types="vite/client" />
import "@tanstack/react-table"; //or vue, svelte, solid, qwik, etc.

declare module "@tanstack/react-table" {
  // eslint-disable-next-line
  interface ColumnMeta<TData extends RowData, TValue> {
    className?: string;
  }
}

interface ImportMetaEnv {
  readonly VITE_TOOLS: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
