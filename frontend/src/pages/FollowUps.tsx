import { useState, useMemo, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { AppLayout } from '@/components/layout/AppLayout';
import api from '@/lib/api';
import { FollowUp } from '@/types';
import { useToast } from '@/hooks/use-toast';
import { CheckSquare, Plus, AlertCircle, CheckCircle } from 'lucide-react';

export default function FollowUps() {
  const { toast } = useToast();
  const [followUps, setFollowUps] = useState<FollowUp[]>([]);
  const [patients, setPatients] = useState<any[]>([]); // simplified type for dropdown
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [isLoading, setIsLoading] = useState(true);

  // New follow-up form state
  const [newFollowUp, setNewFollowUp] = useState({
    patientId: '',
    title: '',
    description: '',
    dueDate: '',
  });

  const today = new Date().toISOString().split('T')[0];

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const [fuRes, patRes] = await Promise.all([
        api.get('/follow-ups/'),
        api.get('/patients/')
      ]);

      const mappedFollowUps = fuRes.data.map((f: any) => ({
        id: f.id,
        patientName: f.patient_name || f.patientName || 'Unknown',
        patientId: f.patient_id,
        title: f.title,
        status: f.status,
        dueDate: f.due_date,
        isCompleted: f.is_completed,
        companyId: f.company_id,
        description: f.description || '', // Assuming description serves as notes or vice versa if applicable
        createdAt: new Date(f.created_at || Date.now())
      }));

      const mappedPatients = patRes.data.map((p: any) => ({
        id: p.id,
        name: p.name
      }));

      setFollowUps(mappedFollowUps);
      setPatients(mappedPatients);
    } catch (error) {
      console.error("Failed to fetch data:", error);
      toast({ title: 'Error', description: 'Failed to load follow-ups', variant: 'destructive' });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredFollowUps = useMemo(() => {
    let filtered = [...followUps];
    if (filterStatus !== 'all') {
      filtered = filtered.filter((f) => f.status === filterStatus);
    }
    return filtered.sort((a, b) => {
      // Sort by status (open first) then by due date
      if (a.status !== b.status) {
        return a.status === 'open' ? -1 : 1;
      }
      return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
    });
  }, [followUps, filterStatus]);

  const handleCreateFollowUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFollowUp.patientId || !newFollowUp.title || !newFollowUp.dueDate) {
      toast({ title: 'Error', description: 'Please fill in all required fields', variant: 'destructive' });
      return;
    }

    try {
      const payload = {
        patient_id: newFollowUp.patientId,
        title: newFollowUp.title,
        description: newFollowUp.description,
        due_date: newFollowUp.dueDate, // Note: Backend expects due_date? Allowable name mismatch or strict? Backend schema says due_date. 
        // Backend Pydantic schema for FollowUpCreate usually maps snake_case. 
        // Let's check schema if needed, but assuming snake_case for input.
        priority: 'medium', // Default
        status: 'open',
        is_completed: false
      };

      // Ensure API expects camelCase or snake_case. Usually snake_case for Python backends.
      // Re-reading previous files, it seems I used snake_case for Appointment payload.
      // Wait, Pydantic handles JSON parsing. If I send due_date, Pydantic with alias generator or default will read it.
      // Let's stick to safe bets.

      const response = await api.post('/follow-ups/', {
        ...payload,
        due_date: newFollowUp.dueDate // Explicitly backend key
      });
      const f = response.data;
      const patient = patients.find(p => p.id === newFollowUp.patientId);

      const followUp: FollowUp = {
        id: f.id,
        patientName: patient?.name || 'Unknown',
        patientId: f.patient_id,
        status: f.status,
        dueDate: f.due_date,
        isCompleted: f.is_completed,
        companyId: f.company_id,
        description: f.description || '',
        createdAt: new Date(f.created_at || Date.now())
      };

      setFollowUps([...followUps, followUp]);
      setNewFollowUp({ patientId: '', title: '', description: '', dueDate: '' });
      setIsDialogOpen(false);
      toast({ title: 'Follow-up created', description: `Task added for ${patient?.name}.` });
    } catch (error) {
      console.error("Failed to create follow-up:", error);
      toast({ title: 'Error', description: 'Failed to create task', variant: 'destructive' });
    }
  };

  const handleToggleStatus = async (followUpId: string) => {
    const followUp = followUps.find(f => f.id === followUpId);
    if (!followUp) return;

    const newStatus = followUp.status === 'open' ? 'completed' : 'open';
    const isCompleted = newStatus === 'completed';

    try {
      // Optimistic update
      setFollowUps(followUps.map((f) =>
        f.id === followUpId ? { ...f, status: newStatus, isCompleted } : f
      ));

      await api.patch(`/follow-ups/${followUpId}`, { status: newStatus, is_completed: isCompleted });
      // No toast needed for simple toggle typically, or maybe a small one
    } catch (error) {
      console.error("Failed to update status:", error);
      toast({ title: 'Error', description: 'Failed to update status', variant: 'destructive' });
      fetchData(); // Revert
    }
  };

  const getStatusInfo = (followUp: FollowUp) => {
    if (followUp.status === 'completed') {
      return {
        color: 'bg-success/10 text-success border-success/20',
        icon: CheckCircle,
        label: 'Completed',
      };
    }
    const isOverdue = new Date(followUp.dueDate) < new Date(today);
    if (isOverdue) {
      return {
        color: 'bg-destructive/10 text-destructive border-destructive/20',
        icon: AlertCircle,
        label: 'Overdue',
      };
    }
    return {
      color: 'bg-warning/10 text-warning border-warning/20',
      icon: CheckSquare,
      label: 'Open',
    };
  };

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Follow-ups</h1>
            <p className="text-muted-foreground">Track patient tasks and reminders</p>
          </div>
          <div className="flex items-center gap-3">
            <Select value={filterStatus} onValueChange={setFilterStatus}>
              <SelectTrigger className="w-[140px]">
                <SelectValue placeholder="Filter" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All</SelectItem>
                <SelectItem value="open">Open</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
              </SelectContent>
            </Select>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button className="flex items-center gap-2">
                  <Plus className="h-4 w-4" />
                  New Task
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                  <DialogTitle>Create Follow-up Task</DialogTitle>
                  <DialogDescription>
                    Add a new task linked to a patient.
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleCreateFollowUp} className="space-y-4 mt-4">
                  <div className="space-y-2">
                    <Label>Patient *</Label>
                    <Select
                      value={newFollowUp.patientId}
                      onValueChange={(value) => setNewFollowUp({ ...newFollowUp, patientId: value })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select patient" />
                      </SelectTrigger>
                      <SelectContent>
                        {patients.map((patient) => (
                          <SelectItem key={patient.id} value={patient.id}>
                            {patient.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="title">Title *</Label>
                    <Input
                      id="title"
                      placeholder="e.g., Schedule blood work"
                      value={newFollowUp.title}
                      onChange={(e) => setNewFollowUp({ ...newFollowUp, title: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="description">Description</Label>
                    <Textarea
                      id="description"
                      placeholder="Additional details..."
                      value={newFollowUp.description}
                      onChange={(e) => setNewFollowUp({ ...newFollowUp, description: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="dueDate">Due Date *</Label>
                    <Input
                      id="dueDate"
                      type="date"
                      value={newFollowUp.dueDate}
                      onChange={(e) => setNewFollowUp({ ...newFollowUp, dueDate: e.target.value })}
                    />
                  </div>
                  <div className="flex justify-end gap-3 pt-4">
                    <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                      Cancel
                    </Button>
                    <Button type="submit" disabled={isLoading}>
                      {isLoading ? 'Creating...' : 'Create Task'}
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        {/* Follow-ups List */}
        {isLoading ? (
          <div className="text-center py-12 text-muted-foreground">Loading tasks...</div>
        ) : filteredFollowUps.length === 0 ? (
          <Card className="border-border">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <CheckSquare className="h-12 w-12 text-muted-foreground/50 mb-3" />
              <p className="text-muted-foreground">No follow-ups found</p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-3">
            {filteredFollowUps.map((followUp) => {
              const statusInfo = getStatusInfo(followUp);
              const StatusIcon = statusInfo.icon;

              return (
                <Card key={followUp.id} className="border-border">
                  <CardContent className="flex items-center justify-between p-4">
                    <div className="flex items-center gap-4">
                      <button
                        onClick={() => handleToggleStatus(followUp.id)}
                        className={`flex h-10 w-10 items-center justify-center rounded-full transition-colors ${followUp.status === 'completed'
                          ? 'bg-success/10 hover:bg-success/20'
                          : 'bg-muted hover:bg-muted/80'
                          }`}
                      >
                        <StatusIcon className={`h-5 w-5 ${followUp.status === 'completed' ? 'text-success' : 'text-muted-foreground'
                          }`} />
                      </button>
                      <div>
                        <div className="flex items-center gap-2">
                          <p className={`font-medium ${followUp.status === 'completed'
                            ? 'text-muted-foreground line-through'
                            : 'text-foreground'
                            }`}>
                            {followUp.title}
                          </p>
                          <Badge variant="outline" className={statusInfo.color}>
                            {statusInfo.label}
                          </Badge>
                        </div>
                        <p className="text-sm text-muted-foreground">{followUp.patientName}</p>
                        {followUp.description && (
                          <p className="text-sm text-muted-foreground mt-1">{followUp.description}</p>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-foreground">
                        {new Date(followUp.dueDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </AppLayout>
  );
}
