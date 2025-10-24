import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  BarChart3, 
  PieChart, 
  TrendingUp, 
  Calendar,
  Clock,
  Users,
  AlertTriangle,
  Mail
} from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { analyticsApi } from "@/api/analytics";
import { Loader2 } from "lucide-react";

const Analytics = () => {
  // Fetch real analytics data
  const { data: overview, isLoading: overviewLoading } = useQuery({
    queryKey: ['analytics-overview'],
    queryFn: () => analyticsApi.getOverview(),
  });

  const { data: trends, isLoading: trendsLoading } = useQuery({
    queryKey: ['analytics-trends'],
    queryFn: () => analyticsApi.getTrends(7),
  });

  const { data: departments, isLoading: departmentsLoading } = useQuery({
    queryKey: ['analytics-departments'],
    queryFn: () => analyticsApi.getDepartmentStats(),
  });

  // Transform data for display
  const categoryData = overview?.categories.map((cat, index) => ({
    category: cat.category,
    count: cat.count,
    percentage: cat.percentage,
    color: ["bg-primary", "bg-accent", "bg-secondary", "bg-info"][index % 4] as string,
  })) || [];

  const trendData = trends?.map((t, index) => ({
    day: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][index % 7],
    emails: t.count,
  })) || [];

  const departmentData = departments?.map((dept) => ({
    name: dept.department,
    emails: dept.email_count,
    avgResponse: dept.avg_response_time,
  })) || [];

  return (
    <div className="min-h-screen bg-background py-12">
      <div className="container mx-auto px-6">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2">Analytics & Insights</h2>
          <p className="text-muted-foreground">
            Comprehensive email intelligence and trend analysis
          </p>
        </div>

        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">
              <BarChart3 className="w-4 h-4 mr-2" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="categories">
              <PieChart className="w-4 h-4 mr-2" />
              Categories
            </TabsTrigger>
            <TabsTrigger value="trends">
              <TrendingUp className="w-4 h-4 mr-2" />
              Trends
            </TabsTrigger>
            <TabsTrigger value="departments">
              <Users className="w-4 h-4 mr-2" />
              Departments
            </TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {overviewLoading ? (
                Array.from({ length: 3 }).map((_, i) => (
                  <Card key={i} className="border-border">
                    <CardContent className="pt-6">
                      <div className="animate-pulse">
                        <div className="h-4 bg-muted rounded w-24 mb-2"></div>
                        <div className="h-8 bg-muted rounded w-32 mb-2"></div>
                      </div>
                    </CardContent>
                  </Card>
                ))
              ) : overview ? (
                <>
                  <MetricCard
                    icon={<Mail className="w-6 h-6" />}
                    title="Total Volume"
                    value={overview.total_emails.toLocaleString()}
                    subtitle="Last 30 days"
                    trend="+12.5%"
                  />
                  <MetricCard
                    icon={<Clock className="w-6 h-6" />}
                    title="Avg Response Time"
                    value={`${overview.avg_response_time.toFixed(1)}h`}
                    subtitle="Processing time"
                    trend="-18%"
                  />
                  <MetricCard
                    icon={<AlertTriangle className="w-6 h-6" />}
                    title="High Priority"
                    value={overview.high_priority_count.toString()}
                    subtitle="Requires attention"
                    trend="+3"
                  />
                </>
              ) : null}
            </div>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5" />
                  7-Day Email Volume
                </CardTitle>
                <CardDescription>Daily email traffic analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {trendData.map((day) => (
                    <div key={day.day} className="flex items-center gap-4">
                      <span className="text-sm font-medium w-12">{day.day}</span>
                      <div className="flex-1 h-10 bg-muted rounded-lg overflow-hidden">
                        <div
                          className="h-full bg-gradient-primary flex items-center justify-end pr-3 text-primary-foreground text-sm font-semibold transition-all duration-500"
                          style={{ width: `${(day.emails / 510) * 100}%` }}
                        >
                          {day.emails}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="categories" className="space-y-6">
            <Card className="border-border">
              <CardHeader>
                <CardTitle>Email Distribution by Category</CardTitle>
                <CardDescription>AI categorization breakdown</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {categoryData.map((item) => (
                  <div key={item.category} className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="font-medium">{item.category}</span>
                      <div className="flex items-center gap-3">
                        <span className="text-muted-foreground">{item.count} emails</span>
                        <span className="font-semibold">{item.percentage}%</span>
                      </div>
                    </div>
                    <div className="h-3 bg-muted rounded-full overflow-hidden">
                      <div
                        className={`h-full ${item.color} transition-all duration-500`}
                        style={{ width: `${item.percentage}%` }}
                      />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="trends" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card className="border-border">
                <CardHeader>
                  <CardTitle className="text-lg">Peak Hours</CardTitle>
                  <CardDescription>Most active email times</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <TimeSlot time="9:00 AM - 11:00 AM" emails={456} percentage={85} />
                    <TimeSlot time="2:00 PM - 4:00 PM" emails={389} percentage={72} />
                    <TimeSlot time="11:00 AM - 1:00 PM" emails={312} percentage={58} />
                  </div>
                </CardContent>
              </Card>

              <Card className="border-border">
                <CardHeader>
                  <CardTitle className="text-lg">Growth Metrics</CardTitle>
                  <CardDescription>Month-over-month comparison</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <GrowthItem label="Email Volume" value="+12.5%" positive />
                    <GrowthItem label="Response Time" value="-18%" positive />
                    <GrowthItem label="Pending Items" value="+5%" positive={false} />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="departments" className="space-y-6">
            <Card className="border-border">
              <CardHeader>
                <CardTitle>Department Performance</CardTitle>
                <CardDescription>Email volume and response metrics by department</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {departmentData.map((dept) => (
                    <div
                      key={dept.name}
                      className="flex items-center justify-between p-4 bg-muted rounded-lg hover:bg-muted/80 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center text-primary-foreground font-bold">
                          {dept.name.slice(0, 2)}
                        </div>
                        <div>
                          <p className="font-semibold">{dept.name}</p>
                          <p className="text-sm text-muted-foreground">{dept.emails} emails</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-muted-foreground">Avg Response</p>
                        <p className="font-semibold">{dept.avgResponse}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

interface MetricCardProps {
  icon: React.ReactNode;
  title: string;
  value: string;
  subtitle: string;
  trend: string;
}

const MetricCard = ({ icon, title, value, subtitle, trend }: MetricCardProps) => {
  return (
    <Card className="border-border hover:border-primary/40 transition-all duration-200">
      <CardContent className="pt-6">
        <div className="flex items-start justify-between mb-4">
          <div className="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center text-primary-foreground">
            {icon}
          </div>
          <span className={`text-sm font-semibold px-2 py-1 rounded ${trend.startsWith('+') ? 'text-success bg-success/10' : 'text-muted-foreground bg-muted'}`}>
            {trend}
          </span>
        </div>
        <h3 className="text-sm font-medium text-muted-foreground mb-1">{title}</h3>
        <p className="text-3xl font-bold mb-1">{value}</p>
        <p className="text-xs text-muted-foreground">{subtitle}</p>
      </CardContent>
    </Card>
  );
};

interface TimeSlotProps {
  time: string;
  emails: number;
  percentage: number;
}

const TimeSlot = ({ time, emails, percentage }: TimeSlotProps) => {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <span>{time}</span>
        <span className="font-semibold">{emails} emails</span>
      </div>
      <div className="h-2 bg-muted rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-primary transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

interface GrowthItemProps {
  label: string;
  value: string;
  positive: boolean;
}

const GrowthItem = ({ label, value, positive }: GrowthItemProps) => {
  return (
    <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
      <span className="text-sm font-medium">{label}</span>
      <span className={`text-lg font-bold ${positive ? 'text-success' : 'text-warning'}`}>
        {value}
      </span>
    </div>
  );
};

export default Analytics;
