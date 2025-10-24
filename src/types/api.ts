/**
 * API Response Type Definitions
 */

export interface ApiResponse<T> {
  data?: T;
  message?: string;
  error?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

export interface ApiError {
  detail: string;
  message?: string;
  status_code?: number;
}

// Analytics Types
export interface CategoryStat {
  category: string;
  count: number;
  percentage: number;
  color?: string;
}

export interface TrendData {
  date: string;
  count: number;
  label?: string;
}

export interface AnalyticsOverview {
  total_emails: number;
  unprocessed_count: number;
  processed_today: number;
  high_priority_count: number;
  avg_response_time: number;
  categories: CategoryStat[];
}

export interface SenderStat {
  sender: string;
  count: number;
  avg_response_time?: string;
}

export interface DepartmentStat {
  department: string;
  email_count: number;
  avg_response_time: string;
}

// Query Types
export interface QueryResult {
  id: string;
  sender: string;
  subject: string;
  timestamp: string;
  category: string;
  priority: string;
  summary: string;
}

export interface QueryResponse {
  query: string;
  results_count: number;
  execution_time: number;
  results: QueryResult[];
}
