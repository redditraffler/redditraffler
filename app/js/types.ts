export interface RaffleMetricsAPIResponse {
  num_total_verified_raffles: number;
  num_total_winners: number;
  num_total_subreddits: number;
  top_recent_subreddits: Array<{ subreddit: string; num_raffles: number }>;
}

export type RecentRafflesAPIResponse = Array<{
  created_at: number;
  submission_title: string;
  submission_id: string;
  subreddit: string;
  url_path: string;
}>;

export type GetUserSubmissionsAPIResponse = Array<{
  author: string;
  created_at_utc: number;
  id: string;
  subreddit: string;
  title: string;
  url: string;
}>;
