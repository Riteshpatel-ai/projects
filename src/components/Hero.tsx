import { Button } from "@/components/ui/button";
import { ArrowRight, Mail, Brain, TrendingUp, Zap } from "lucide-react";
import heroImage from "@/assets/hero-bg.jpg";

const Hero = () => {
  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-subtle">
      {/* Animated background */}
      <div className="absolute inset-0 overflow-hidden">
        <img 
          src={heroImage} 
          alt="MedMail Intelligence Platform" 
          className="w-full h-full object-cover opacity-20"
        />
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-accent/10" />
      </div>

      {/* Content */}
      <div className="relative container mx-auto px-6 pt-32 pb-24">
        <div className="max-w-4xl mx-auto text-center space-y-8 animate-fade-in">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 bg-card border border-primary/20 rounded-full px-4 py-2 shadow-md">
            <Zap className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium">From Inbox to Intelligence</span>
          </div>

          {/* Main heading */}
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
            <span className="bg-clip-text text-transparent bg-gradient-primary">
              MedMail Intelligence
            </span>
            <br />
            <span className="text-foreground">Platform</span>
          </h1>

          {/* Subheading */}
          <p className="text-xl md:text-2xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Transform hospital email chaos into actionable insights with AI-powered automation, analysis, and intelligent workflow management.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <Button variant="hero" size="lg" className="group">
              Get Started
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="outline" size="lg">
              Watch Demo
            </Button>
          </div>

          {/* Feature highlights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-12">
            <FeatureCard
              icon={<Mail className="w-6 h-6" />}
              title="Smart Email Processing"
              description="AI categorization and extraction from all hospital communications"
            />
            <FeatureCard
              icon={<Brain className="w-6 h-6" />}
              title="Intelligent Insights"
              description="Natural language queries and contextual analytics"
            />
            <FeatureCard
              icon={<TrendingUp className="w-6 h-6" />}
              title="Real-time Analytics"
              description="Live dashboards with actionable trends and alerts"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

const FeatureCard = ({ icon, title, description }: FeatureCardProps) => {
  return (
    <div className="group bg-card border border-border hover:border-primary/40 rounded-xl p-6 shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      <div className="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center text-primary-foreground mb-4 group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-muted-foreground text-sm">{description}</p>
    </div>
  );
};

export default Hero;
