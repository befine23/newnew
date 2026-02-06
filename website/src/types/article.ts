export interface Article {
  source: string;
  title: string;
  title_zh?: string;
  url: string;
  description: string;
  description_zh?: string;
  content?: string;
  content_zh?: string;
  scraped_at: string;
  published_date: string;
}
