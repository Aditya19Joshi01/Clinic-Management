export type UserRole = 'admin' | 'staff';

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  companyId: string;
  companyName: string;
  companyCode: string;
}

export interface Company {
  id: string;
  name: string;
  code: string;
  createdAt: Date;
}

export interface Patient {
  id: string;
  name: string;
  email: string;
  phone: string;
  dateOfBirth: string;
  address: string;
  companyId: string;
  createdAt: Date;
}

export interface Appointment {
  id: string;
  patientId: string;
  patientName: string;
  date: string;
  time: string;
  reason: string;
  status: 'scheduled' | 'completed' | 'cancelled';
  companyId: string;
  createdAt: Date;
}

export interface FollowUp {
  id: string;
  patientId: string;
  patientName: string;
  title: string;
  description: string;
  dueDate: string;
  status: 'open' | 'completed';
  companyId: string;
  createdAt: Date;
}

export interface StaffMember {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  companyId: string;
  joinedAt: Date;
}

export interface Note {
  id: string;
  patientId: string;
  content: string;
  createdBy: string;
  createdAt: Date;
}
