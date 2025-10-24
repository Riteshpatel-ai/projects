import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  Mail, 
  Search, 
  Filter, 
  TrendingUp, 
  Clock, 
  CheckCircle2,
  AlertCircle,
  Users,
  FileText,
  DollarSign,
  Activity,
  Loader2,
  RefreshCw
} from "lucide-react";
import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { emailApi } from "@/api/emails";
import { analyticsApi } from "@/api/analytics";
import type { Email } from "@/types";
import { useToast } from "@/hooks/use-toast";

// Stats will be fetched from API

const Dashboard = () => {
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState("all");
  const [gmailConnected, setGmailConnected] = useState(true);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  // Fetch analytics data for stats
  const { data: analyticsData } = useQuery({
    queryKey: ['analytics-overview'],
    queryFn: () => analyticsApi.getOverview(),
    refetchInterval: 60000, // Refresh every minute
  });

  // Check Gmail connection on mount
  useEffect(() => {
    (async () => {
      try {
        const user = await import("@/api/auth").then(m => m.authApi.getCurrentUser());
        // Accept any property for now (TS ignore), or extend User type
        setGmailConnected(!!(user as any).gmail_access_token);
      } catch {
        setGmailConnected(false);
      }
    })();
  }, []);

  // Fetch emails
  const { data: emails = [], isLoading, error, refetch } = useQuery({
    queryKey: ['emails', activeTab, searchQuery],
    queryFn: () => emailApi.getEmails({
      status: activeTab === 'all' ? undefined : (activeTab as 'unread' | 'pending' | 'processed' | 'archived'),
      limit: 100
    }),
    refetchInterval: 10000, // Poll every 10 seconds for real-time updates
  });

  // Sync emails mutation
  const syncMutation = useMutation({
    mutationFn: () => emailApi.syncEmails(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['emails'] });
      toast({
        title: "Sync Complete",
        description: "Gmail emails synced successfully!",
      });
    },
    onError: (error: any) => {
      toast({
        title: "Sync Failed",
        description: error.response?.data?.detail || "Failed to sync emails",
        variant: "destructive",
      });
    },
  });

  // Select first email when data loads
  useEffect(() => {
    if (emails.length > 0 && !selectedEmail) {
      setSelectedEmail(emails[0]);
    }
  }, [emails, selectedEmail]);

  const getPriorityBadge = (priority: string) => {
    const variants: Record<string, "default" | "destructive" | "secondary"> = {
      high: "destructive",
      medium: "default",
      low: "secondary",
    };
    return variants[priority] || "default";
  };

  const getCategoryIcon = (category: string) => {
    const icons: Record<string, React.ReactNode> = {
      "Diagnostic Report": <FileText className="w-4 h-4" />,
      "Insurance Claim": <DollarSign className="w-4 h-4" />,
      "Patient Message": <Users className="w-4 h-4" />,
      "Billing": <Activity className="w-4 h-4" />,
    };
    return icons[category] || <Mail className="w-4 h-4" />;
  };

  // Dynamic stats from analytics API
  const stats = analyticsData ? [
    { label: "Total Emails", value: analyticsData.total_emails.toLocaleString(), change: "+12%", icon: Mail, color: "text-primary" },
    { label: "Unprocessed", value: analyticsData.unprocessed_count.toLocaleString(), change: "-8%", icon: Clock, color: "text-warning" },
    { label: "Processed Today", value: analyticsData.processed_today.toLocaleString(), change: "+24%", icon: CheckCircle2, color: "text-success" },
    { label: "High Priority", value: analyticsData.high_priority_count.toLocaleString(), change: "+3", icon: AlertCircle, color: "text-destructive" },
  ] : [];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-primary">
                Email Intelligence Dashboard
              </h2>
              <p className="text-sm text-muted-foreground mt-1">
                AI-powered email analysis and management
              </p>
            </div>
            {!gmailConnected ? (
              <Button
                variant="hero"
                onClick={async () => {
                  try {
                    const url = await import("@/api/auth").then(m => m.authApi.getGmailAuthUrl());
                    window.location.href = url;
                  } catch (err) {
                    toast({ title: 'Gmail Connect Failed', description: 'Could not get authorization URL', variant: 'destructive' });
                  }
                }}
              >
                <Mail className="w-4 h-4" />
                Connect Gmail
              </Button>
            ) : (
              <Button variant="hero" onClick={() => syncMutation.mutate()} disabled={syncMutation.isPending}>
                <Mail className="w-4 h-4" />
                {syncMutation.isPending ? 'Syncing...' : 'Sync Inbox'}
              </Button>
            )}
          </div>
        </div>
      </header>

      <div className="container mx-auto px-6 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.length > 0 ? stats.map((stat, index) => (
            <Card key={index} className="border-border hover:border-primary/40 transition-all duration-200 hover:shadow-lg">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
                    <p className="text-3xl font-bold mt-2">{stat.value}</p>
                    <div className="flex items-center gap-1 mt-2">
                      <TrendingUp className="w-4 h-4 text-success" />
                      <span className="text-sm text-success font-medium">{stat.change}</span>
                    </div>
                  </div>
                  <div className={`w-12 h-12 rounded-lg bg-gradient-primary flex items-center justify-center ${stat.color}`}>
                    <stat.icon className="w-6 h-6 text-primary-foreground" />
                  </div>
                </div>
              </CardContent>
            </Card>
          )) : (
            // Loading skeleton
            Array.from({ length: 4 }).map((_, i) => (
              <Card key={i} className="border-border">
                <CardContent className="pt-6">
                  <div className="animate-pulse">
                    <div className="h-4 bg-muted rounded w-24 mb-2"></div>
                    <div className="h-8 bg-muted rounded w-32 mb-2"></div>
                    <div className="h-4 bg-muted rounded w-16"></div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Main Content Area */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Email List */}
          <Card className="lg:col-span-2 border-border">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Email Inbox</CardTitle>
                  <CardDescription>AI-categorized hospital communications</CardDescription>
                </div>
                <div className="flex gap-2">
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => syncMutation.mutate()}
                    disabled={syncMutation.isPending}
                  >
                    {syncMutation.isPending ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <RefreshCw className="w-4 h-4" />
                    )}
                    <span className="ml-2">Sync Emails</span>
                  </Button>
                </div>
              </div>
              <div className="relative mt-4">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Search emails..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="all">All</TabsTrigger>
                  <TabsTrigger value="unread">Unread</TabsTrigger>
                  <TabsTrigger value="pending">Pending</TabsTrigger>
                  <TabsTrigger value="processed">Processed</TabsTrigger>
                </TabsList>
                <TabsContent value={activeTab} className="space-y-3 mt-6">
                  {isLoading ? (
                    <div className="flex justify-center items-center py-8">
                      <Loader2 className="w-6 h-6 animate-spin" />
                      <span className="ml-2">Loading emails...</span>
                    </div>
                  ) : error ? (
                    <Alert variant="destructive">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>Failed to load emails. Please try again.</AlertDescription>
                    </Alert>
                  ) : emails.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      No emails found. Click "Sync Emails" to fetch from Gmail.
                    </div>
                  ) : (
                    emails.map((email) => (
                      <div
                        key={email.id}
                        onClick={() => setSelectedEmail(email)}
                        className={`p-4 border border-border rounded-lg cursor-pointer transition-all duration-200 hover:border-primary/40 hover:shadow-md ${
                          selectedEmail?.id === email.id ? "border-primary bg-primary/5" : "bg-card"
                        }`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center text-primary-foreground">
                            {getCategoryIcon(email.category || 'Other')}
                          </div>
                          <div>
                            <p className="font-semibold text-sm">{email.sender}</p>
                            <p className="text-xs text-muted-foreground">
                              {new Date(email.timestamp).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                        <Badge variant={getPriorityBadge(email.priority || 'medium')}>
                          {email.priority || 'medium'}
                        </Badge>
                      </div>
                      <p className="text-sm font-medium mb-1">{email.subject}</p>
                      <div className="flex items-center gap-2">
                        <Badge variant="secondary" className="text-xs">
                          {email.category || 'Uncategorized'}
                        </Badge>
                        <Badge variant="outline" className="text-xs">
                          {email.status}
                        </Badge>
                      </div>
                    </div>
                  ))
                  )}
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          {/* Email Detail Panel */}
          <Card className="border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Extracted Data
              </CardTitle>
              <CardDescription>AI-powered information extraction</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {selectedEmail ? (
                <>
                  <div>
                    <h4 className="text-sm font-semibold mb-3 text-muted-foreground">Email Details</h4>
                    <div className="space-y-3">
                      <DataField label="Category" value={selectedEmail.category || 'Uncategorized'} />
                      <DataField label="Priority" value={selectedEmail.priority || 'medium'} />
                      <DataField label="Status" value={selectedEmail.status} />
                      <DataField label="Date" value={new Date(selectedEmail.timestamp).toLocaleString()} />
                    </div>
                  </div>

                  {selectedEmail.entities && Object.keys(selectedEmail.entities).length > 0 && (
                    <div className="pt-4 border-t border-border">
                      <h4 className="text-sm font-semibold mb-3 text-muted-foreground">Extracted Information</h4>
                      <div className="space-y-3">
                        {Object.entries(selectedEmail.entities).map(([key, value]) => (
                          <DataField 
                            key={key} 
                            label={key.replace(/([A-Z_])/g, ' $1').trim()} 
                            value={String(value || 'N/A')} 
                          />
                        ))}
                      </div>
                    </div>
                  )}

                  {selectedEmail.summary && (
                    <div className="pt-4 border-t border-border">
                      <h4 className="text-sm font-semibold mb-3 text-muted-foreground">Summary</h4>
                      <p className="text-sm text-muted-foreground">{selectedEmail.summary}</p>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  Select an email to view details
                </div>
              )}

              <div className="pt-4 space-y-2">
                <Button
                  variant="default"
                  className="w-full"
                  disabled={!selectedEmail || selectedEmail.status === 'processed'}
                  onClick={async () => {
                    if (!selectedEmail) return;
                    try {
                      await emailApi.updateStatus(selectedEmail.id, 'processed');
                      toast({ title: 'Marked as Processed', description: 'Email status updated.' });
                      refetch();
                    } catch (err) {
                      toast({ title: 'Error', description: 'Failed to update status', variant: 'destructive' });
                    }
                  }}
                >
                  <CheckCircle2 className="w-4 h-4" />
                  Mark as Processed
                </Button>
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => toast({ title: 'Not implemented', description: 'Generate Response coming soon!' })}
                >
                  Generate Response
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

interface DataFieldProps {
  label: string;
  value: string;
}

const DataField = ({ label, value }: DataFieldProps) => {
  return (
    <div className="flex justify-between items-center py-2 px-3 bg-muted rounded-lg">
      <span className="text-xs font-medium text-muted-foreground capitalize">{label}</span>
      <span className="text-sm font-semibold">{value}</span>
    </div>
  );
};

export default Dashboard;
