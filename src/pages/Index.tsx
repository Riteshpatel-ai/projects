import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { LayoutDashboard, BarChart3, Brain, Home } from "lucide-react";
import Hero from "@/components/Hero";
import Dashboard from "@/components/Dashboard";
import Analytics from "@/components/Analytics";
import AIAssistant from "@/components/AIAssistant";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Tabs defaultValue="home" className="w-full">
        {/* Navigation */}
        <div className="sticky top-0 z-50 bg-card/95 backdrop-blur-sm border-b border-border shadow-sm">
          <div className="container mx-auto px-6">
            <div className="flex items-center justify-between py-4">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center">
                  <span className="text-primary-foreground font-bold text-lg">M</span>
                </div>
                <span className="font-bold text-xl">MedMail</span>
              </div>
              
              <TabsList className="bg-muted">
                <TabsTrigger value="home" className="gap-2">
                  <Home className="w-4 h-4" />
                  Home
                </TabsTrigger>
                <TabsTrigger value="dashboard" className="gap-2">
                  <LayoutDashboard className="w-4 h-4" />
                  Dashboard
                </TabsTrigger>
                <TabsTrigger value="analytics" className="gap-2">
                  <BarChart3 className="w-4 h-4" />
                  Analytics
                </TabsTrigger>
                <TabsTrigger value="assistant" className="gap-2">
                  <Brain className="w-4 h-4" />
                  AI Assistant
                </TabsTrigger>
              </TabsList>
            </div>
          </div>
        </div>

        {/* Content */}
        <TabsContent value="home" className="m-0">
          <Hero />
        </TabsContent>

        <TabsContent value="dashboard" className="m-0">
          <Dashboard />
        </TabsContent>

        <TabsContent value="analytics" className="m-0">
          <Analytics />
        </TabsContent>

        <TabsContent value="assistant" className="m-0">
          <AIAssistant />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Index;
