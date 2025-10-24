/**
 * Main API exports
 */
export { apiClient } from './client';
export { authApi } from './auth';
export { emailApi } from './emails';
export { analyticsApi } from './analytics';
export { queryApi } from './query';

export type { Email } from './emails';
export type { User, LoginCredentials, RegisterData } from './auth';
export type { AnalyticsOverview, CategoryStat, TrendData } from './analytics';
export type { QueryResponse, QueryResult } from './query';
