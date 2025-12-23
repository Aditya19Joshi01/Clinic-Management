import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { User, UserRole } from '@/types';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  registerCompany: (companyName: string, adminName: string, email: string, password: string) => Promise<void>;
  registerStaff: (companyCode: string, name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Mock data for demo purposes
const mockCompanies = new Map([
  ['CLINIC001', { id: '1', name: 'City Health Clinic', code: 'CLINIC001' }],
]);

const mockUsers = new Map([
  ['admin@cityhealth.com', { id: '1', email: 'admin@cityhealth.com', password: 'admin123', name: 'Dr. Sarah Johnson', role: 'admin' as UserRole, companyId: '1', companyName: 'City Health Clinic' }],
  ['staff@cityhealth.com', { id: '2', email: 'staff@cityhealth.com', password: 'staff123', name: 'John Smith', role: 'staff' as UserRole, companyId: '1', companyName: 'City Health Clinic' }],
]);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem('clinic_user');
    return stored ? JSON.parse(stored) : null;
  });

  const login = useCallback(async (email: string, password: string) => {
    const mockUser = mockUsers.get(email);
    if (!mockUser || mockUser.password !== password) {
      throw new Error('Invalid email or password');
    }
    const { password: _, ...userWithoutPassword } = mockUser;
    setUser(userWithoutPassword);
    localStorage.setItem('clinic_user', JSON.stringify(userWithoutPassword));
  }, []);

  const registerCompany = useCallback(async (companyName: string, adminName: string, email: string, password: string) => {
    if (mockUsers.has(email)) {
      throw new Error('Email already registered');
    }
    const companyId = `company_${Date.now()}`;
    const companyCode = `CLINIC${String(mockCompanies.size + 1).padStart(3, '0')}`;
    
    const newUser: User = {
      id: `user_${Date.now()}`,
      email,
      name: adminName,
      role: 'admin',
      companyId,
      companyName,
    };
    
    mockCompanies.set(companyCode, { id: companyId, name: companyName, code: companyCode });
    mockUsers.set(email, { ...newUser, password });
    
    setUser(newUser);
    localStorage.setItem('clinic_user', JSON.stringify(newUser));
  }, []);

  const registerStaff = useCallback(async (companyCode: string, name: string, email: string, password: string) => {
    if (mockUsers.has(email)) {
      throw new Error('Email already registered');
    }
    const company = mockCompanies.get(companyCode);
    if (!company) {
      throw new Error('Invalid company code');
    }
    
    const newUser: User = {
      id: `user_${Date.now()}`,
      email,
      name,
      role: 'staff',
      companyId: company.id,
      companyName: company.name,
    };
    
    mockUsers.set(email, { ...newUser, password });
    
    setUser(newUser);
    localStorage.setItem('clinic_user', JSON.stringify(newUser));
  }, []);

  const logout = useCallback(() => {
    setUser(null);
    localStorage.removeItem('clinic_user');
  }, []);

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, registerCompany, registerStaff, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
