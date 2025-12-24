import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { User, UserRole } from '@/types';
import api from '@/lib/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  registerCompany: (companyName: string, adminName: string, email: string, password: string) => Promise<void>;
  registerStaff: (companyCode: string, name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const stored = localStorage.getItem('clinic_user');
    return stored ? JSON.parse(stored) : null;
  });

  const handleAuthResponse = (response: any) => {
    // Backend returns JSON body: { access_token, user: { ... } }
    const rootData = response.data;
    const userData = rootData.user || rootData; // Fallback for safety
    const token = response.headers['authorization']?.replace('Bearer ', '') || rootData.access_token;

    if (token) {
      localStorage.setItem('clinic_token', token);
    }

    if (!userData || !userData.id) {
      console.error("Invalid user data received:", rootData);
      return;
    }

    // Map snake_case from backend to camelCase for frontend
    const mappedUser: User = {
      id: userData.id,
      email: userData.email,
      name: userData.name,
      role: userData.role,
      companyId: userData.company_id,
      companyName: userData.company_name
    };

    console.log("Mapped user:", mappedUser);
    setUser(mappedUser);
    localStorage.setItem('clinic_user', JSON.stringify(mappedUser));
  };

  const login = useCallback(async (email: string, password: string) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      handleAuthResponse(response);
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  }, []);

  const registerCompany = useCallback(async (companyName: string, adminName: string, email: string, password: string) => {
    try {
      const response = await api.post('/auth/register/company', {
        companyName,
        adminName,
        email,
        password
      });
      handleAuthResponse(response);
    } catch (error) {
      console.error("Company registration failed:", error);
      throw error;
    }
  }, []);

  const registerStaff = useCallback(async (companyCode: string, name: string, email: string, password: string) => {
    try {
      const response = await api.post('/auth/register/staff', {
        companyCode,
        name,
        email,
        password
      });
      handleAuthResponse(response);
    } catch (error) {
      console.error("Staff registration failed:", error);
      throw error;
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout');
    } catch (e) {
      console.error("Logout error (ignoring):", e);
    } finally {
      setUser(null);
      localStorage.removeItem('clinic_user');
      localStorage.removeItem('clinic_token');
    }
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
