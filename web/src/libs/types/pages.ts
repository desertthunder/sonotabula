export type Feature = {
  title: string;
  description: string;
  icon: string;
};

export type BrowserContext = {
  setTitle: (title: string) => void;
  setDescription: (description: string) => void;
};
