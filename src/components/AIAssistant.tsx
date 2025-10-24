import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Brain, Send, Sparkles, MessageSquare, Loader2, AlertCircle } from "lucide-react";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { queryApi } from "@/api/query";
import type { QueryResponse } from "@/types";

interface Message {
  id: number;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

const AIAssistant = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: "assistant",
      content: "Hello! I'm your AI assistant for MedMail Intelligence. Ask me anything about your hospital emails, analytics, or specific data points. For example, you can ask:\n\n• \"Show unprocessed diagnostic results from last week\"\n• \"How many pending insurance claims?\"\n• \"Which doctor gets the most patient emails?\"",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [inputValue, setInputValue] = useState("");

  // API mutation for querying
  const queryMutation = useMutation({
    mutationFn: (query: string) => queryApi.query(query),
    onSuccess: (data: QueryResponse, query: string) => {
      const aiResponse: Message = {
        id: messages.length + 1,
        role: "assistant",
        content: formatQueryResponse(data, query),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, aiResponse]);
    },
    onError: (error: any) => {
      const errorMessage: Message = {
        id: messages.length + 1,
        role: "assistant",
        content: `❌ Sorry, I encountered an error: ${error.response?.data?.detail || error.message || 'Unknown error'}. Please try again.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    },
  });

  const suggestedQueries = [
    "Show urgent emails from today",
    "Pending insurance claims this month",
    "Most active departments by email volume",
    "Emails requiring follow-up",
  ];

  const formatQueryResponse = (data: QueryResponse, query: string): string => {
    if (data.results_count === 0) {
      return `I couldn't find any emails matching: "${query}"\n\nTry:\n• Using different keywords\n• Broadening your search criteria\n• Checking if emails are synced`;
    }

    let response = `Found ${data.results_count} email${data.results_count > 1 ? 's' : ''} matching your query "${query}":\n\n`;
    
    // Show top 5 results
    const topResults = data.results.slice(0, 5);
    topResults.forEach((email, index) => {
      response += `${index + 1}. **${email.subject}**\n`;
      response += `   From: ${email.sender}\n`;
      response += `   Category: ${email.category} | Priority: ${email.priority}\n`;
      response += `   Date: ${new Date(email.timestamp).toLocaleDateString()}\n`;
      if (email.summary) {
        response += `   Summary: ${email.summary.slice(0, 100)}...\n`;
      }
      response += `\n`;
    });

    if (data.results_count > 5) {
      response += `...and ${data.results_count - 5} more results.\n`;
    }

    response += `\n⏱️ Query executed in ${data.execution_time}s`;
    return response;
  };

  const handleSendMessage = () => {
    if (!inputValue.trim() || queryMutation.isPending) return;

    const userMessage: Message = {
      id: messages.length + 1,
      role: "user",
      content: inputValue,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages([...messages, userMessage]);

    // Call real API
    queryMutation.mutate(inputValue);

    setInputValue("");
  };

  const handleSuggestedQuery = (query: string) => {
    setInputValue(query);
  };

  return (
    <div className="min-h-screen bg-background py-12">
      <div className="container mx-auto px-6 max-w-5xl">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center">
              <Brain className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <h2 className="text-3xl font-bold">AI Query Assistant</h2>
              <p className="text-muted-foreground">Natural language email intelligence</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Chat Interface */}
          <Card className="lg:col-span-2 border-border">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="w-5 h-5" />
                Conversation
              </CardTitle>
              <CardDescription>
                Ask questions in natural language about your hospital emails
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <ScrollArea className="h-[500px] pr-4">
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg p-4 ${
                          message.role === "user"
                            ? "bg-primary text-primary-foreground"
                            : "bg-muted"
                        }`}
                      >
                        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                        <p
                          className={`text-xs mt-2 ${
                            message.role === "user" ? "text-primary-foreground/70" : "text-muted-foreground"
                          }`}
                        >
                          {message.timestamp}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </ScrollArea>

              {queryMutation.isError && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>
                    Error: {queryMutation.error?.response?.data?.detail || 'Failed to query emails'}
                  </AlertDescription>
                </Alert>
              )}

              <div className="flex gap-2">
                <Input
                  placeholder="Ask about emails, analytics, or specific data..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && !queryMutation.isPending && handleSendMessage()}
                  className="flex-1"
                  disabled={queryMutation.isPending}
                />
                <Button 
                  onClick={handleSendMessage} 
                  variant="default"
                  disabled={queryMutation.isPending || !inputValue.trim()}
                >
                  {queryMutation.isPending ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Send className="w-4 h-4" />
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Suggested Queries */}
          <div className="space-y-6">
            <Card className="border-border">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Sparkles className="w-5 h-5" />
                  Suggested Queries
                </CardTitle>
                <CardDescription>Quick insights</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {suggestedQueries.map((query, index) => (
                  <button
                    key={index}
                    onClick={() => handleSuggestedQuery(query)}
                    className="w-full text-left p-3 bg-muted hover:bg-muted/80 rounded-lg transition-colors text-sm"
                  >
                    {query}
                  </button>
                ))}
              </CardContent>
            </Card>

            <Card className="border-border">
              <CardHeader>
                <CardTitle className="text-lg">Capabilities</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Badge variant="secondary" className="mr-2 mb-2">Email Search</Badge>
                <Badge variant="secondary" className="mr-2 mb-2">Analytics</Badge>
                <Badge variant="secondary" className="mr-2 mb-2">Trends</Badge>
                <Badge variant="secondary" className="mr-2 mb-2">Summaries</Badge>
                <Badge variant="secondary" className="mr-2 mb-2">Data Extraction</Badge>
                <Badge variant="secondary" className="mr-2 mb-2">Predictions</Badge>
              </CardContent>
            </Card>

            <Card className="border-border bg-gradient-subtle">
              <CardContent className="pt-6">
                <div className="flex items-start gap-3">
                  <Brain className="w-8 h-8 text-primary flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold mb-1">Powered by AI</p>
                    <p className="text-xs text-muted-foreground">
                      Using advanced language models and RAG technology for accurate, context-aware responses.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
