export type BrowserContext = {
  setTitle: (title: string) => void;
  setDescription: (description: string) => void;
};

export type Pagination = {
  total: number;
  per_page: number;
  page: number;
  num_pages: number;
};
