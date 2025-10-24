/**
 * RAG Query API Service
 */
import apiClient from './client';

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

export const queryApi = {
  /**
   * Perform natural language query
   */
  query: async (queryText: string): Promise<QueryResponse> => {
    const response = await apiClient.post('/query/', {
      query: queryText,
    });
    return response.data;
  },

  /**
   * Rebuild RAG index
   */
  rebuildIndex: async () => {
    const response = await apiClient.post('/query/rebuild-index');
    return response.data;
  },

  /**
   * Get query history
   */
  getHistory: async (limit: number = 20) => {
    const response = await apiClient.get('/query/history', {
      params: { limit },
    });
    return response.data;
  },
};
