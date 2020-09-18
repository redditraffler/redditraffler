export interface RaffleMetricsAPIResponse {
  num_total_verified_raffles: number;
  num_total_winners: number;
  num_total_subreddits: number;
  top_recent_subreddits: Array<{ subreddit: string; num_raffles: number }>;
}
