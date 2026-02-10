export interface Article {
  id: string;
  slug: string;
  source: string;
  title: string;
  title_zh?: string;
  url: string;
  description?: string;
  description_zh?: string;
  content?: string;
  content_zh?: string;
  summary_zh?: string;
  image_url?: string;
  scraped_at: string;
  published_date: string;
}
