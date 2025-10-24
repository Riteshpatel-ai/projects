/**
 * Email API Service
 */
import apiClient from './client';
import type { Email } from '@/types';

export const emailApi = {
  /**
   * Sync emails from Gmail
   */
  syncEmails: async (days: number = 7) => {
    const response = await apiClient.post('/emails/sync', null, {
      params: { days },
    });
    return response.data;
  },

  /**
   * Get emails with filters
   */
  getEmails: async (params?: {
    skip?: number;
    limit?: number;
    category?: string;
    priority?: 'high' | 'medium' | 'low';
    status?: 'unread' | 'pending' | 'processed' | 'archived';
    search?: string;
    date_from?: string;
    date_to?: string;
  }): Promise<Email[]> => {
    const response = await apiClient.get('/emails/', { params });
    return response.data;
  },

  /**
   * Get specific email by ID
   */
  getEmail: async (emailId: string): Promise<Email> => {
    const response = await apiClient.get(`/emails/${emailId}`);
    return response.data;
  },

  /**
   * Update email status
   */
  updateStatus: async (emailId: string, status: string) => {
    const response = await apiClient.patch(`/emails/${emailId}/status`, null, {
      params: { status },
    });
    return response.data;
  },

  /**
   * Delete email
   */
  deleteEmail: async (emailId: string) => {
    const response = await apiClient.delete(`/emails/${emailId}`);
    return response.data;
  },
};
