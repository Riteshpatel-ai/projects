/**
 * Analytics API Service
 */
import apiClient from './client';

export interface CategoryStat {
  category: string;
  count: number;
  percentage: number;
}

export interface TrendData {
  date: string;
  count: number;
}

export interface AnalyticsOverview {
  total_emails: number;
  unprocessed_count: number;
  processed_today: number;
  high_priority_count: number;
  avg_response_time: number;
  categories: CategoryStat[];
}

export const analyticsApi = {
  /**
   * Get analytics overview
   */
  getOverview: async (): Promise<AnalyticsOverview> => {
    const response = await apiClient.get('/analytics/overview');
    return response.data;
  },

  /**
   * Get category distribution
   */
  getCategoryDistribution: async (days: number = 30) => {
    const response = await apiClient.get('/analytics/categories', {
      params: { days },
    });
    return response.data;
  },

  /**
   * Get email trends
   */
  getTrends: async (days: number = 7): Promise<TrendData[]> => {
    const response = await apiClient.get('/analytics/trends', {
      params: { days },
    });
    return response.data;
  },

  /**
   * Get top senders
   */
  getTopSenders: async (limit: number = 10) => {
    const response = await apiClient.get('/analytics/top-senders', {
      params: { limit },
    });
    return response.data;
  },

  /**
   * Get attachment statistics
   */
  getAttachmentStats: async () => {
    const response = await apiClient.get('/analytics/attachments');
    return response.data;
  },

  /**
   * Get department statistics
   */
  getDepartmentStats: async () => {
    const response = await apiClient.get('/analytics/departments');
    return response.data;
  },
};
