/**
 * Email Type Definitions
 */

export interface Email {
  id: string;
  gmail_id?: string;
  sender: string;
  recipient?: string;
  subject: string;
  timestamp: string;
  category?: string;
  priority?: 'high' | 'medium' | 'low';
  summary?: string;
  content?: string;
  status: 'unread' | 'pending' | 'processed' | 'archived';
  entities?: EmailEntities;
  attachments?: Attachment[];
  confidence_score?: number;
  created_at?: string;
  updated_at?: string;
}

export interface EmailEntities {
  patient_name?: string;
  doctor_name?: string;
  department?: string;
  amount?: string;
  date?: string;
  diagnosis?: string;
  claim_id?: string;
  appointment_date?: string;
  [key: string]: string | undefined;
}

export interface Attachment {
  filename: string;
  mime_type: string;
  size: number;
  content_summary?: string;
}

export interface EmailFilters {
  skip?: number;
  limit?: number;
  category?: string;
  priority?: 'high' | 'medium' | 'low';
  status?: 'unread' | 'pending' | 'processed' | 'archived';
  search?: string;
  date_from?: string;
  date_to?: string;
}
